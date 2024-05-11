# -*- coding: utf-8 -*-

import logging


class MatchPattern:
    EQUALS = 0
    CONTAINS = 1
    STARTS_WITH = 2
    ENDS_WITH = 3


class ElementBy:
    id = "id"
    text = "text"
    type = "type"
    description = "description"
    clickable = "clickable"
    longClickable = "longClickable"
    scrollable = "scrollable"
    enabled = "enabled"
    focused = "focused"
    selected = "selected"
    checked = "checked"
    checkable = "checkable"
    isBefore = "isBefore"
    isAfter = "isAfter"


class ElementAttribute:
    id = "id"
    text = "text"
    type = "type"
    description = "description"
    bounds = "bounds"
    boundsCenter = "boundsCenter"
    isClickable = "isClickable"
    isLongClickable = "isLongClickable"
    isScrollable = "isScrollable"
    isEnabled = "isEnabled"
    isFocused = "isFocused"
    isSelected = "isSelected"
    isChecked = "isChecked"
    isCheckable = "isCheckable"


class ElementType:
    Text = "Text"
    TextInput = "TextInput"
    Button = "Button"
    Image = "Image"
    Column = "Column"
    Divider = "Divider"
    TabBar = "TabBar"
    Row = "Row"
    Stack = "Stack"
    XComponent = "XComponent"
    Flex = "Flex"
    Canvas = "Canvas"
    RelativeContainer = "RelativeContainer"
    ListItem = "ListItem"
    GridItem = "GridItem"
    Grid = "Grid"
    TabContent = "TabContent"
    Swiper = "Swiper"
    Tabs = "Tabs"


class ElementOperate:
    click = "click"
    doubleClick = "doubleClick"
    longClick = "longClick"
    clear = "clear"
    input = "input"
    scrollToTop = "scrollToTop"
    scrollToBottom = "scrollToBottom"
    dragTo = "dragTo"
    pinchOut = "pinchOut"
    pinchIn = "pinchIn"
    scrollSearch = "scrollSearch"


class Element(object):
    def __init__(self, client, euid: str, property):
        self._client = client
        self.euid = euid
        self._property = property

    def __repr__(self):
        return f'<Element(euid={self.euid}, id={self._property["id"]}, ' \
               f'text={self._property["text"]}, type={self._property["type"]}, ' \
               f'bounds={self._property["bounds"]}, bounds_center={self._property["boundsCenter"]})>'

    def __get(self, attribute):
        self._property = self.properties
        if attribute not in self._property:
            data = {"action": "get", "property": attribute, "euid": self.euid}
            self._property[attribute] = self._client.request(data)["data"]
        return self._property[attribute]

    @property
    def properties(self):
        if not self._property:
            self._property = self._client.request({"action": "get", "property": 'info', "euid": self.euid})["data"]
        return self._property

    @property
    def id(self):
        return self.__get(ElementAttribute.id)

    @property
    def text(self):
        return self.__get(ElementAttribute.text)

    @property
    def type(self):
        return self.__get(ElementAttribute.type)

    @property
    def bounds(self):
        return self.__get(ElementAttribute.bounds)

    @property
    def bounds_center(self):
        return self.__get(ElementAttribute.boundsCenter)

    @property
    def description(self):
        return self.__get(ElementAttribute.description)

    @property
    def isClickable(self):
        return self.__get(ElementAttribute.isClickable)

    @property
    def isLongClickable(self):
        return self.__get(ElementAttribute.isLongClickable)

    @property
    def isScrollable(self):
        return self.__get(ElementAttribute.isScrollable)

    @property
    def isEnabled(self):
        return self.__get(ElementAttribute.isEnabled)

    @property
    def isFocused(self):
        return self.__get(ElementAttribute.isFocused)

    @property
    def isSelected(self):
        return self.__get(ElementAttribute.isSelected)

    @property
    def isChecked(self):
        return self.__get(ElementAttribute.isChecked)

    @property
    def isCheckable(self):
        return self.__get(ElementAttribute.isCheckable)

    def __operate(self, operate, param: dict={}):
        data = {
            "action": "operate",
            "operate": operate,
            "euid": self.euid,
            **param
        }
        return self._client.request(data)["data"]

    def tap(self):
        return self.__operate(ElementOperate.click)

    def click(self):
        return self.tap()

    def double_click(self):
        return self.__operate(ElementOperate.doubleClick)

    def long_click(self):
        return self.__operate(ElementOperate.longClick)

    def input(self, text):
        return self.__operate(ElementOperate.input, {"text": text})

    def clear(self):
        return self.__operate(ElementOperate.clear)

    def scrollToTop(self, speed=1.0):
        return self.__operate(ElementOperate.scrollToTop, {"param": speed})

    def scrollToBottom(self, speed=1.0):
        return self.__operate(ElementOperate.scrollToBottom, {"param": speed})

    def dragTo(self, ele):
        return self.__operate(ElementOperate.dragTo, {"param": ele.euid})

    def pinchOut(self, scale=1.0):
        return self.__operate(ElementOperate.pinchOut, {"param": scale})

    def pinchIn(self, scale=1.0):
        return self.__operate(ElementOperate.pinchIn, {"param": scale})

    def scrollSearch(self, by: ElementBy, data: str):
        try:
            data = {
                "action": "operate",
                "operate": ElementOperate.scrollSearch,
                "euid": self.euid,
                "param": {"by": by, "data": data}
            }
            resp = self._client.request(data)
            return Element(self._client, resp["euid"], resp["property"])
        except Exception as e:
            logging.error(f"find element Error! {e}")
            return None



