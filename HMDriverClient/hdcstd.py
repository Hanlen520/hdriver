# -*- coding: utf-8 -*-

import logging
import os
import re
import subprocess
import traceback
from HMDriverClient.exception import *


class HDC(object):
    def __init__(self, serial):
        self.serial = serial
        self.cmd_prefix = ['hdc', "-t", serial]

    def run_cmd(self, cmd):
        cmd = f"hdc -t {self.serial} {cmd}"
        out = os.popen(cmd).read()
        return out

    def shell(self, params, is_wait=True):
        """
        run an hdc command and return the output
        :return: output of hdc command or pid of the command process
        @param params: arguments to run in hdc, str or list
        @param is_wait: 是否等待执行结果
        """
        if isinstance(params, str) or isinstance(params, str):
            params = params.split()
        if not isinstance(params, list):
            msg = "invalid arguments: %s\nshould be list or str, %s given" % (params, type(params))
            logging.error(msg)
            raise HDCException(msg)

        args = self.cmd_prefix
        args += params
        logging.debug(f'=====run command:{args}')
        if is_wait:
            r = subprocess.check_output(args).strip()
            if not isinstance(r, str):
                r = r.decode()
            logging.debug(f'return:{r}')
            return r
        else:
            return subprocess.Popen(args, shell=True)

    def is_online(self):
        """
        check if the device is online
        :return: True or False
        """
        out = os.popen('hdc list targets').read()
        if '[Empty]' in out:
            return False
        res = re.search('%s\n' % self.serial, out)
        if res is None:
            return False
        return True

    def get_pid(self, pkg):
        """
        get the pid of a process by package name
        :param pkg: package name
        :return: pid or -1 if not found
        """
        def match(cmd):
            outputs = self.run_cmd(cmd)
            logging.info('get_pid outputs===' + outputs)
            pattern = rf'shell\s+(\d+)\s+.*\s+{pkg.strip()}'
            m = re.findall(pattern, outputs.strip())
            if m:
                return m
            else:
                return -1
        try:
            cmd_list = [f"shell \"ps -ef | grep {pkg}|grep -v grep\"", f"shell \"ps | grep {pkg}|grep -v grep\""]
            for cmd in cmd_list:
                pid = match(cmd)
                if pid != -1:
                    return pid
            return -1
        except Exception as e:
            logging.error(str(e))
            return -1

    def start_app(self, package, ability):
        """
        start an app by package name
        :param package: package name of the app
        :param ability: ability name of the app
        """
        try:
            cmd = f"shell aa start -a {ability} -b {package} -D"
            self.run_cmd(cmd)
        except Exception as e:
            logging.error(traceback.format_exc())

    def stop_app(self, package):
        """
        stop an app by package name
        :param package: package name of the app
        """
        try:
            cmd = f"shell aa force-stop {package}"
            self.run_cmd(cmd)
        except Exception as e:
            logging.error(traceback.format_exc())

    def install_app(self, path):
        """
        install an app by path
        :param path: path of the app to install
        """
        cmd = f"install {path}"
        output = self.run_cmd(cmd)
        if 'successfully' in output:
            return True
        return False

    def uninstall_app(self, package):
        """
        uninstall an app by package name
        :param package: package name of the app to uninstall
        """
        cmd = f"uninstall {package}"
        output = self.run_cmd(cmd)
        if 'successfully' in output:
            return True
        return False
