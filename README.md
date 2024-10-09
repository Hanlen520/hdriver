# HMDriver


- HMDriver是一个鸿蒙系统UI测试的端到端测试方案，具备通用设备测试能力。
- HMDriver包括两部分UiTestAPP和HMDriverClient
- UiTestAPP基于鸿蒙系统提供的“@ohos.UiTest”模块,使用ArkTS语言开发的测试APP。其在鸿蒙端启动一个SocketServer，接收HMDriverClient的指令，执行元素查找、点击、滑动等操作，并返回结果。

![image](https://github.com/mrx1203/hmdriver/blob/main/run.png)

## 特点
 * 支持鸿蒙手机、Pad等其他设备
 * 通过USB与鸿蒙设备通信，不依赖网络，快捷高效
 * HMDriverClient端相比ArkTS语言更易用，降低了使用门槛
 * Socket长连接通信，高效率低延迟
 * UiTestAPP通过鸿蒙IDE编译安装到设备之后，通过HMDriverClient即可操作APP的启停和通信，易用

## 代码说明

1. 操作实现代码在UiTestAPP/entry/src/ohosTest/ets/test/UiTestProcess.ets文件
2. SocketServer代码在UiTestAPP/entry/src/ohosTest/ets/test/Ability.test.ets文件

## 使用说明

在创建HMDriver实例的时候，会自动安装UiTestAPP到设备上并启动，然后转发端口并进行连接
HMDriverClient基于Python3，使用举例如下：
```
from hmdriver import HMDriver
hdriver = HMDriver("127.0.0.1:5555")
# 启动app
hdriver.start_app(bundle, ability)

# 停止app
hdriver.stop_app(bundle)

# 获取屏幕尺寸：
hdriver.get_screen_size()
w, h = size_dict["width"], size_dict["height"]

# 滑动：
hdriver.swipe(w/2, h*0.8, w/2, h*0.2, 1)
hdriver.fling_up()      # 快速上滑
hdriver.fling_down()    # 快速下滑
hdriver.fling_left()    # 快速左滑
hdriver.fling_right()   # 快速右滑

# 按钮事件
# [键值码](https://developer.huawei.com/consumer/cn/doc/harmonyos-references-V2/js-apis-keycode-0000001544703985-V2)
hdriver.press_key(1) # 1 是home键的键值

# 根据坐标点击：
hdriver.click(w/2, h/2)
# 双击
hdriver.double_click(w/2, h/2)
# 长按
hdriver.long_click(w/2, h/2)

# 点亮屏幕
hdriver.wake_up()

# 回退：
hdriver.back()

# 返回桌面：
hdriver.home()

# 截图
# local_path参数不为空，则返回截图文件路径
# local_path参数为空，则返回截图的二进制数据
hdriver.get_screenshot_png(local_path=None)

# 元素查找：
ele = hdriver.find_element("text", "设置", timeout_s=15) # 通过文本查找
ele = hdriver.find_element_by_text("设置", timeout_s=15) # 通过文本查找
ele = hdriver.find_element_by_id("btn_setting", timeout_s=15) # 通过id查找
ele = hdriver.find_element_by_type("Button", timeout_s=15) # 通过控件类型查找
ele = hdriver.find_element_by_desc("设置", timeout_s=15) # 通过控件描述查找

# 复合条件查找，复合条件可通过params参数传递，params为字典，可添加多个
ele = hdriver.find_element_by_text("设置", params={"type": "Button"}, timeout_s=15) # 通过文本和控件类型查找

# 获取控件属性
info = ele.properties
text = ele.text
bounds = ele.bounds
# 控件操作
ele.click()
ele.double_click()
ele.long_click()
# 输入文本
ele.clear()
ele.input("test123")
# 滚动查找
ele2 = ele.scrollSearch("text", "设置")

```

## License

HMDriver is released under the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0).
