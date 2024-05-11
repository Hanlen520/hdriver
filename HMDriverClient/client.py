# -*- coding: utf-8 -*-
import json
import logging
import os
import socket
import struct
import time
import uuid

from HMDriverClient.hdcstd import HDC
from HMDriverClient.exception import *


def json_to_dict(data):
    # 递归转dict
    try:
        for key, value in data.items():
            try:
                data[key] = json.loads(value)
            except:
                pass
            data[key] = json_to_dict(data[key])
    except:
        pass
    if isinstance(data, list):
        for index in range(len(data)):
            try:
                data[index] = json.loads(data[index])
            except:
                pass
            data[index] = json_to_dict(data[index])
    return data


class Client(object):
    test_app_file = "entry-ohosTest-signed.hap"
    test_app_bundle = "com.harmony.uitest"
    socket_buffer_size = 1024
    find_timeout_s = 20

    def __init__(self, serial, local_port=29100):
        self.serial = serial
        self.hdc = HDC(serial)
        self.__used_ports = []
        self.server_port = 29100
        self.local_port = local_port
        self.start_test_runner()
        self.socket = self.connect_socket()

    def __del__(self):
        self.stop_test_runner()

    def __call__(self, *args, **kwargs):
        return self.request(kwargs)

    def get_random_port(self):
        """
        get a random port on host machine to establish connection
        :return: a port number
        """
        temp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        temp_sock.bind(("", 0))
        port = temp_sock.getsockname()[1]
        temp_sock.close()
        if port in self.__used_ports:
            return self.get_random_port()
        self.__used_ports.append(port)
        return port

    def stop_test_runner(self):
        logging.info("stop test runner")
        self.hdc.stop_app(self.test_app_bundle)
        # clear connection
        cmd = f"fport rm tcp:{self.local_port} tcp:{self.server_port}"
        out = self.hdc.run_cmd(cmd)
        logging.info(out)

    def start_test_runner(self):

        key_word = f"ActsAbilityTest#uiTestProcess{self.server_port}"
        pid = self.hdc.get_pid(key_word)
        if pid != -1:
            logging.info(f"{key_word} is running, pid is {pid}")
            return
        cmd_wait = f"shell \"netstat -anpl | grep -v unix | grep {self.local_port}\""
        out = self.hdc.run_cmd(cmd_wait).replace("grep: (standard input): Invalid argument", "").strip()
        if out:
            self.hdc.run_cmd(f"fport rm tcp:{self.local_port} tcp:{self.server_port}")
        # 启动
        cmd = f"shell aa test -b {self.test_app_bundle} -m entry_test " \
              f"-s unittest /ets/testrunner/OpenHarmonyTestRunner " \
              f"-s class ActsAbilityTest#uiTestProcess{self.server_port} -s timeout 86400000"
        self.hdc.shell(cmd, is_wait=False)

    def connect_socket(self, timeout=30):
        logging.info("start socket client init")
        st = time.time()
        while time.time() - st < timeout:
            try:
                cmd_list = [f"fport tcp:{self.local_port} tcp:{self.server_port}", "fport ls"]
                for cmd in cmd_list:
                    out = self.hdc.run_cmd(cmd)
                    logging.info(out)

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                l_onoff = 1
                l_linger = 0
                s.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', l_onoff, l_linger))
                s.connect(("127.0.0.1", self.local_port))
                s.send(b"hello")
                hello_msg = s.recv(self.socket_buffer_size)
                logging.info(f"socket client init ok. got hello message: {hello_msg}")
                return s
            except Exception as e:
                logging.exception(e)
                time.sleep(1)
        raise Exception(f"socket client init timeout after {timeout} seconds!")

    def reconnect_socket(self):
        self.stop_test_runner()
        self.start_test_runner()
        self.socket = self.connect_socket()

    def socket_send(self, msg_dict: dict):
        for retry in range(3):
            try:
                self.socket.send(json.dumps(msg_dict).encode("utf8"))
                break
            except Exception as e:
                logging.exception(e)
                self.reconnect_socket()

    def request(self, msg_data):
        start_time = time.time()
        logging.info(f"#### start request")
        re_dict = None
        for rr in range(2):
            tmp_uuid = str(uuid.uuid1()).replace("-", "")
            try:
                data_dict = msg_data
                data_dict["uuid"] = tmp_uuid
                logging.info(f"data_dict: {data_dict}")
                self.socket_send(data_dict)
                st = time.time()
                time_s = float(msg_data.get("time_s", 0))
                timeout_s = float(msg_data.get("timeout_s", 0))
                total_s = self.find_timeout_s + timeout_s + time_s
                while time.time() - st < total_s:
                    try:
                        re_bytes = self.socket.recv(self.socket_buffer_size)
                        logging.info(f"recv: {re_bytes}")
                    except Exception as e:
                        if e.__str__() == 'Resource temporarily unavailable':
                            time.sleep(0.1)
                        else:
                            logging.exception(e)
                            raise SocketError()
                    else:
                        re_str = re_bytes.decode("utf8")
                        if len(re_str) > 0:
                            re_dict = json.loads(re_str)
                            re_dict = json_to_dict(re_dict)
                            if tmp_uuid == re_dict.get("uuid", ""):
                                break
                else:
                    err_desc = f"wait for {total_s} seconds"
                    raise ElementFoundTimeout(err_desc)

                logging.info(f"re_dict: {re_dict}")
                del re_dict["uuid"]
                if re_dict.get("ret") == "error":
                    error_desc = re_dict.get("description", "")
                    if error_desc.startswith("no ele"):
                        raise ElementNotFoundError(error_desc)
                    else:
                        raise HDriverError(error_desc)
            except SocketError as se:
                logging.exception(se)
                self.reconnect_socket()
                continue
            except ElementFoundTimeout as ee:
                # logging.exception(ee)
                raise ee
            except ElementNotFoundError as fe:
                raise fe
            except HDriverError as he:
                raise he
            except Exception as e:
                logging.exception(e)
            else:
                pass
            finally:
                pass
            break
        used_time = time.time() - start_time
        logging.info(f"#### end request,after {used_time}s")
        return re_dict
