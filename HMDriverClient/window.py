# -*- coding: utf-8 -*-
import logging
import traceback


class WindowFilter:
    bundleName = "bundleName"
    title = "title"
    focused = "focused"
    actived = "actived"
    active = "active"


class WindowMode:
    FULLSCREEN = 0
    PRIMARY = 1
    SECONDARY = 2
    FLOATING = 3


class WindowAttribute:
    bundleName = "bundleName"
    bounds = "bounds"
    title = "title"
    windowMode = "windowMode"
    isFocused = "isFocused"
    isActived = "isActived"
    isActive = "isActive"


class UiWindow(object):
    def __init__(self, client, wuid: str, property):
        self._client = client
        self.wuid = wuid
        self._property = property

    def __repr__(self):
        return f'<UiWindow(wuid={self.wuid}, title={self._property["title"]}, ' \
               f'bundleName={self._property["bundleName"]}, windowMode={self._property["windowMode"]}, ' \
               f'bounds={self._property["bounds"]}, isFocused={self._property["isFocused"]},' \
               f'isActive={self._property["isActive"]})>'

    def __get(self, attribute):
        self._property = self.properties
        if attribute not in self._property:
            data = {
                "action": "window",
                "operate": "get",
                "property": attribute,
                "wuid": self.wuid
            }
            self._property[attribute] = self._client.request(data)["data"]
        return self._property[attribute]

    @property
    def properties(self):
        if not self._property:
            data = {
                "action": "window",
                "operate": "get",
                "property": 'info',
                "wuid": self.wuid
            }
            self._property = self._client.request(data)["data"]
        return self._property

    @property
    def title(self):
        """
        获取窗口标题
        :return:
        """
        return self.__get("title")

    @property
    def bundleName(self):
        """
        获取窗口所属应用名称
        :return:
        """
        return self.__get("bundleName")

    @property
    def bounds(self):
        """
        获取窗口大小和位置
        :return:
        """
        return self.__get("bounds")

    @property
    def windowMode(self):
        """
        获取窗口模式, 0: 全屏模式, 1: 主窗口模式, 2: 次窗口模式, 3: 浮动窗口模式
        :return:
        """
        return self.__get("windowMode")

    @property
    def isFocused(self):
        """
        获取窗口是否处于焦点状态
        :return:
        """
        return self.__get("isFocused")

    @property
    def isActived(self):
        """
        获取窗口是否处于激活状态
        :return:
        """
        return self.__get("isActived")

    @property
    def isActive(self):
        """
        获取窗口是否处于激活状态
        :return:
        """
        return self.__get("isActive")

    def __operate(self, operate, param: dict={}):
        data = {
            "action": "window",
            "operate": "action",
            "func": operate,
            "wuid": self.wuid,
            **param
        }
        self._client.request(data)

    def focus(self):
        """
        获取焦点
        :return:
        """
        self.__operate("focus")

    def moveTo(self, x: int, y: int):
        """
        移动窗口到指定位置
        :param x:
        :param y:
        :return:
        """
        self.__operate("moveTo", {'x': x, 'y': y})

    def maximize(self):
        """
        最大化窗口
        :return:
        """
        self.__operate("maximize")

    def minimize(self):
        """
        最小化窗口
        :return:
        """
        self.__operate("minimize")

    def resume(self):
        """
        恢复窗口
        :return:
        """
        self.__operate("resume")

    def close(self):
        """
        关闭窗口
        :return:
        """
        self.__operate("close")
