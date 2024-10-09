# -*- coding: utf-8 -*-
from HMDriverClient.element import *
from HMDriverClient.client import *
from HMDriverClient.hdcstd import *
from HMDriverClient.window import *

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class UiDirection:
    """
    UI方向枚举类，用于设置滑动方向
    """
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3


class DisplayRotation:
    """
    屏幕旋转枚举类，用于设置屏幕旋转角度
    """
    ROTATION_0 = 0
    ROTATION_90 = 1
    ROTATION_180 = 2
    ROTATION_270 = 3


class HMDriver(HDC):

    def __init__(self, device_id: str, app_bundle: str = "", app_ability: str = ""):
        super(HMDriver, self).__init__(device_id)
        self.device_id = device_id
        self.app_bundle = app_bundle
        self.app_ability = app_ability
        self.hdc = HDC(self.device_id)
        self.__setup()
        self.client = Client(self.device_id, local_port=29100)

    def __del__(self):
        self.stop()

    def __setup(self):
        # 当前文件所在路径
        dirname, filename = os.path.split(os.path.abspath(__file__))
        hap_list = [
            os.path.join(dirname, "hap", "entry-default-unsigned.hap"),
            os.path.join(dirname, "hap", "entry-ohosTest-unsigned.hap"),
        ]
        for hap in hap_list:
            if os.path.exists(hap):
                logging.info(f"install {hap}: {self.hdc.install_app(hap)}")

    def stop(self):
        if self.client:
            self.client.stop_test_runner()
            self.client = None

    def req(self, msg_data):
        try:
            resp = self.client.request(msg_data)
            return resp
        except Exception as e:
            logging.error(f"{traceback.format_exc()}")
            return None

    def find_element(self, by: str, data: str, params=None, timeout_s: int = 10):
        """
        查找控件
        :param by: ElementBy类型
        :param data: 对应by的取值
        :param params: 查找控件的其他限定条件，以字典形式传入{ElementBy.text: ""}
        :param timeout_s: 查找控件超时时间，单位秒
        :return: 控件对象，如果查找失败返回None
        示例:
        # 查找id为"btn_sign"且类型为Button的控件
        element = hdriver.find_element(ElementBy.id, "btn_sign", params={ElementBy.type: ElementType.Button})
        params还可以添加其他限定条件，比如:
        # 查找id为"btn_sign"且类型为Button，并且text为"设置"的控件
        element = hdriver.find_element(ElementBy.id, "btn_sign", params={ElementBy.type: ElementType.Button, ElementBy.text: "设置"})
        """
        try:
            msg_data = {
                "action": "find",
                "by": by,
                "data": data,
                "timeout_s": str(timeout_s),
                "params": params
            }
            resp = self.req(msg_data)
            return Element(self.client, resp["euid"], resp["property"])
        except Exception as e:
            logging.error(f"find element Error! {e}")
            return None

    def find_element_by_id(self, id: str, params=None, timeout_s: int = 10):
        """
        通过id查找控件
        :param id: 控件id
        :param params: 查找控件的其他限定条件，以字典形式传入
            比如: {"text": "设置"},查找控件id为{id},并且text为"设置"的控件
        :param timeout_s: 查找控件超时时间，单位秒
        :return: 控件对象，如果查找失败返回None
        """
        return self.find_element(ElementBy.id, id, params, timeout_s)

    def find_element_by_text(self, text: str, params=None, timeout_s: int = 10):
        """
        通过text查找控件
        :param text: 控件text
        :param params: 查找控件的其他限定条件，以字典形式传入
            比如: {"id": "btn_sign"},查找控件text为{text}，并且id为"btn_sign"的控件
        :param timeout_s: 查找控件超时时间，单位秒
        :return: 控件对象，如果查找失败返回None
        """
        return self.find_element(ElementBy.text, text, params, timeout_s)

    def find_element_by_desc(self, desc: str, params=None, timeout_s: int = 10):
        """
        通过description查找控件
        :param desc: 控件description
        :param params: 查找控件的其他限定条件，以字典形式传入
            比如: {"id": "btn_sign"},查找控件description为{desc}，并且id为"btn_sign"的控件
        :param timeout_s: 查找控件超时时间，单位秒
        :return: 控件对象，如果查找失败返回None
        """
        return self.find_element(ElementBy.description, desc, params, timeout_s)

    def find_element_by_type(self, typename: str, params=None, timeout_s: int = 10):
        """
        通过type查找控件
        :param typename: 控件type
        :param params: 查找控件的其他限定条件，以字典形式传入
            比如: {"id": "btn_sign"},查找控件type为{typename}，并且id为"btn_sign"的控件
        :param timeout_s: 查找控件超时时间，单位秒
        :return: 控件对象，如果查找失败返回None
        """
        return self.find_element(ElementBy.type, typename, params, timeout_s)

    def find_elements(self, by: str, data: str, params=None, timeout_s=20):
        """
        查找多个控件, 与find_element一样,只是该函数返回控件对象列表
        :param by: ElementBy类型
        :param data: 对应by的取值
        :param params: 查找控件的其他限定条件，以字典形式传入{ElementBy.text: ""}
        :param timeout_s: 查找控件超时时间，单位秒
        :return: 控件对象列表，如果查找失败返回None
        """
        try:
            msg_data = {
                "action": "finds",
                "by": by,
                "data": data,
                **params
            }
            st = time.perf_counter()
            ele_list = []
            while time.perf_counter() - st < timeout_s:
                try:
                    resp = self.req(msg_data)
                    ele_list = resp["data"]
                    if len(ele_list) > 0:
                        break
                except Exception as e:
                    logging.warning(f"find elements Error! {e}, retry again")
                time.sleep(1)
            if not ele_list:
                return None
            return [Element(self.client, ele["euid"], ele["property"]) for ele in ele_list]
        except Exception as e:
            logging.error(f"find elements Error! {e}")
            return None

    def find_elements_by_id(self, id: str, params=None, timeout_s: int = 10):
        """
        通过id查找控件
        :param id: 控件id
        :param params: 查找控件的其他限定条件，以字典形式传入
            比如: {"text": "设置"},查找控件id为{id},并且text为"设置"的控件
        :param timeout_s: 查找控件超时时间，单位秒
        :return: 控件对象列表，如果查找失败返回None
        """
        return self.find_elements(ElementBy.id, id, params, timeout_s)

    def find_elements_by_text(self, text: str, params=None, timeout_s: int = 10):
        """
        通过text查找控件
        :param text: 控件text
        :param params: 查找控件的其他限定条件，以字典形式传入
            比如: {"id": "btn_sign"},查找控件text为{text}，并且id为"btn_sign"的控件
        :param timeout_s: 查找控件超时时间，单位秒
        :return: 控件对象列表，如果查找失败返回None
        """
        return self.find_elements(ElementBy.text, text, params, timeout_s)

    def find_elements_by_desc(self, desc: str, params=None, timeout_s: int = 10):
        """
        通过description查找控件
        :param desc: 控件description
        :param params: 查找控件的其他限定条件，以字典形式传入
            比如: {"id": "btn_sign"},查找控件description为{desc}，并且id为"btn_sign"的控件
        :param timeout_s: 查找控件超时时间，单位秒
        :return: 控件对象列表，如果查找失败返回None
        """
        return self.find_elements(ElementBy.description, desc, params, timeout_s)

    def find_elements_by_type(self, typename: str, params=None, timeout_s: int = 10):
        """
        通过type查找控件
        :param typename: 控件type
        :param params: 查找控件的其他限定条件，以字典形式传入
            比如: {"id": "btn_sign"},查找控件type为{typename}，并且id为"btn_sign"的控件
        :param timeout_s: 查找控件超时时间，单位秒
        :return: 控件对象列表，如果查找失败返回None
        """
        return self.find_elements(ElementBy.type, typename, params, timeout_s)

    def find_window(self, filters):
        """
        查找窗口，返回窗口对象
        :param filters: 查找窗口的限定条件，以字典形式传入, 可用条件参考 WindowFilter
            比如: {"title": "登录"},查找窗口标题为"登录"的窗口
        :return: 窗口对象，如果查找失败返回None
        """
        try:
            data = {
                "action": "window",
                "operate": "find",
                "filter": filters
            }
            resp = self.req(data)
            return UiWindow(self.client, resp["euid"], resp["property"])
        except Exception as e:
            logging.error(f"find window Error! {e}")
            return None

    def find_window_by_title(self, title: str):
        """
        通过title查找窗口，返回窗口对象
        :param title: 窗口标题
        :return: 窗口对象，如果查找失败返回None
        """
        return self.find_window({WindowFilter.title: title})

    def find_window_by_bundlename(self, bundleName: str):
        """
        通过bundleName查找窗口，返回窗口对象
        :param bundleName: 窗口bundleName
        :return: 窗口对象，如果查找失败返回None
        """
        return self.find_window({WindowFilter.bundleName: bundleName})

    def find_window_by_focused(self):
        """
        查找当前焦点窗口，返回窗口对象
        :return: 窗口对象，如果查找失败返回None
        """
        return self.find_window({WindowFilter.focused: True})

    def click(self, x, y):
        """
        点击屏幕坐标(x, y)
        :param x: 横坐标
        :param y: 纵坐标
        :return: 点击成功返回True，否则返回False
        """
        resp = self.req({"action": "click", "x": str(x), "y": str(y)})
        return True if resp else False

    def double_click(self, x, y):
        """
        双击屏幕坐标(x, y)
        :param x: 横坐标
        :param y: 纵坐标
        :return: 点击成功返回True，否则返回False
        """
        resp = self.req({"action": "doubleClick", "x": str(x), "y": str(y)})
        return True if resp else False

    def long_click(self, x, y):
        """
        长按屏幕坐标(x, y)
        :param x: 横坐标
        :param y: 纵坐标
        :return: 点击成功返回True，否则返回False
        """
        resp = self.req({"action": "longClick", "x": str(x), "y": str(y)})
        return True if resp else False

    def swipe(self, startx, starty, endx, endy, time_s=1):
        """
        滑动屏幕，从(startx, starty)到(endx, endy)，滑动时间time_s
        :param startx: 起始横坐标
        :param starty: 起始纵坐标
        :param endx: 结束横坐标
        :param endy: 结束纵坐标
        :param time_s: 滑动时间，单位秒
        :return: 滑动成功返回True，否则返回False
        """
        # 滑动速率，范围：200-40000，不在范围内设为默认值为600，单位：像素点/秒
        speed = int(max(abs(startx - endx), abs(starty - endy)) / time_s)
        speed = 600 if speed < 200 else (600 if speed > 40000 else speed)
        data = {
            "action": "swipe",
            "startx": str(int(startx)),
            "starty": str(int(starty)),
            "endx": str(int(endx)),
            "endy": str(int(endy)),
            "speed": str(speed),
            "time_s": str(time_s)
        }
        resp = self.req(data)
        return True if resp else False

    def drag(self, startx, starty, endx, endy, time_s=1):
        """
        拖动屏幕，从(startx, starty)到(endx, endy)，滑动时间time_s
        :param startx: 起始横坐标
        :param starty: 起始纵坐标
        :param endx: 结束横坐标
        :param endy: 结束纵坐标
        :param time_s: 滑动时间，单位秒
        :return: 滑动成功返回True，否则返回False
        """
        # 滑动速率，范围：200-40000，不在范围内设为默认值为600，单位：像素点/秒
        speed = int(max(abs(startx - endx), abs(starty - endy)) / time_s)
        speed = 600 if speed < 200 else (600 if speed > 40000 else speed)
        data = {
            "action": "drag",
            "startx": str(int(startx)),
            "starty": str(int(starty)),
            "endx": str(int(endx)),
            "endy": str(int(endy)),
            "speed": str(speed),
            "time_s": str(time_s)
        }
        resp = self.req(data)
        return True if resp else False

    def fling(self, direction, speed=600):
        """
        快速滑动屏幕，方向direction，滑动速度speed
        :param direction: 滑动方向，枚举值：UiDirection.LEFT, UiDirection.RIGHT, UiDirection.UP, UiDirection.DOWN
        :param speed: 滑动速度，范围：200-40000，不在范围内设为默认值为600，单位：像素点/秒
        :return: 滑动成功返回True，否则返回False
        """
        # 滑动速率，范围：200-40000，不在范围内设为默认值为600，单位：像素点/秒
        speed = 600 if speed < 200 else (600 if speed > 40000 else speed)
        data = {
            "action": "fling",
            "direction": direction,
            "speed": speed
        }
        resp = self.req(data)
        return True if resp else False

    def fling_left(self):
        """
        快速向左滑动屏幕
        :return: 成功返回True，否则返回False
        """
        return self.fling(UiDirection.LEFT)

    def fling_right(self):
        """
        快速向右滑动屏幕
        :return: 成功返回True，否则返回False
        """
        return self.fling(UiDirection.RIGHT)

    def fling_up(self):
        """
        快速向上滑动屏幕
        :return: 成功返回True，否则返回False
        """
        return self.fling(UiDirection.UP)

    def fling_down(self):
        """
        快速向下滑动屏幕
        :return: 成功返回True，否则返回False
        """
        return self.fling(UiDirection.DOWN)

    def home(self):
        """
        回到桌面
        :return: 成功返回True，否则返回False
        """
        resp = self.req({"action": "home"})
        return True if resp else False

    def back(self):
        """
        返回上一页
        :return: 成功返回True，否则返回False
        """
        resp = self.req({"action": "back"})
        return True if resp else False

    def press_key(self, key_code: int, key2: int = 0, key3: int = 0):
        """
        按下按键
         键值参考：https://developer.huawei.com/consumer/cn/doc/harmonyos-references-V2/js-apis-keycode-0000001544703985-V2
        :param key_code: 按键码
        :param key2: 组合键
        :param key3: 组合键
        :return: 成功返回True，否则返回False
        """
        data = {
            "action": "keyEvent",
            "key": key_code,
            "key1": key2,
            "key2": key3
        }
        resp = self.req(data)
        return True if resp else False

    def set_rotation(self, rotation):
        """
        设置屏幕旋转角度
        :param rotation: 旋转角度，
            枚举值：DisplayRotation.ROTATION_0, DisplayRotation.ROTATION_90,
                    DisplayRotation.ROTATION_180, DisplayRotation.ROTATION_270
        :return: 成功返回True，否则返回False
        """
        data = {
            "action": "setRotation",
            "rotation": rotation
        }
        resp = self.req(data)
        return True if resp else False

    def get_rotation(self):
        """
        获取屏幕旋转角度
        :return: 返回当前屏幕旋转角度，枚举值：DisplayRotation.ROTATION_0, DisplayRotation.ROTATION_90,
                    DisplayRotation.ROTATION_180, DisplayRotation.ROTATION_270
        """
        resp = self.req({"action": "getRotation"})
        return resp["data"] if resp else False

    def wake_up(self):
        """
        点亮屏幕
        :return: 成功返回True，否则返回False
        """
        resp = self.req({"action": "wakeup"})
        return True if resp else False

    def get_screen_size(self):
        resp = self.req({"action": "screenSize"})["data"]
        return {"width": resp["x"], "height": resp["y"]}

    def get_current_bundle(self):
        return self.req({"action": "currentBundle"})["data"]

    def _get_screenshot_file(self, local_path=None):
        remote_path = "/data/local/tmp/aa.png"
        cap_cmd = f'hdc -t {self.device_id} shell "rm -rf {remote_path};sync;uitest screenCap -p {remote_path};sync"'
        cap_ret = os.popen(cap_cmd).read().strip()
        if not cap_ret.startswith("ScreenCap saved to"):
            raise Exception(f"screen shot failed! {cap_ret}")
        if not local_path:
            local_path = "aa.png"
        cmd = f"hdc -t {self.device_id} file recv {remote_path} {local_path}"
        # logging.info(f"recv: {cmd}")
        os.popen(cmd).read()
        st = time.time()
        while time.time() - st < 5 and not os.path.exists(local_path):
            time.sleep(0.1)
        os.sync()
        # 远程删除
        cmd = f"hdc -t {self.device_id} shell rm -rf {remote_path}"
        os.popen(cmd).read()
        return local_path

    def get_screenshot_png(self, local_path=None):
        png_path = self._get_screenshot_file(local_path)
        if not local_path:
            with open(png_path, "rb") as ff:
                png_bytes = ff.read()
            # 本地删除
            os.remove(png_path)
            return png_bytes
        return png_path


if __name__ == "__main__":
    hdriver = HMDriver("127.0.0.1:5555", "", "")
    # hdriver2 = HDriver("127.0.0.1:5555", "", "")
    # hdriver.home()
    time.sleep(3)
    ele = hdriver.find_elements("text", "设置", params={ElementBy.enabled: False})
    print(ele[0].properties)
    ele2 = hdriver.find_element("text", "图库")
    print(ele2.properties)
    ele[0].click()
    print(hdriver.get_screen_size())
    hdriver.swipe(200, 1500, 200, 500, 1)
    time.sleep(1)
    hdriver.fling_up()
    hdriver.fling_down()
    hdriver.fling_left()
    hdriver.fling_right()
    hdriver.press_key(1)
    time.sleep(1)
    hdriver.stop()
