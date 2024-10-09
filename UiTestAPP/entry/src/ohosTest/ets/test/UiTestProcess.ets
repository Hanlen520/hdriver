import {
    Component,
    Driver,
    UiWindow,
    ON,
    MatchPattern,
    DisplayRotation,
    ResizeDirection,
    UiDirection,
    MouseButton,
    WindowMode,
    PointerMatrix,
    On
} from '@ohos.UiTest';
import request from '@ohos.request';
import { BusinessError } from '@ohos.base';
import AbilityDelegatorRegistry from '@ohos.app.ability.abilityDelegatorRegistry';

let abilityDelegator: AbilityDelegatorRegistry.AbilityDelegator;
abilityDelegator = AbilityDelegatorRegistry.getAbilityDelegator();

let driver: Driver = Driver.create();
let eleMap: Map<string, Component> = new Map<string, Component>();
let windowMap: Map<string, UiWindow> = new Map<string, UiWindow>();

export async function pressHome() {
    await driver.pressHome();
    await commonWaitIdle();
}

export function myPrint(message: string) {
    console.info("UiTestCase: " + message);
}

export function sleep(time: number) {
    return new Promise<void>((resolve: Function) => setTimeout(resolve, time));
}

async function execShell(cmd: string) {
    abilityDelegator.executeShellCommand(cmd, (err: BusinessError, data: AbilityDelegatorRegistry.ShellCmdResult) => {
        console.info('UiTestCase: executeShellCommand callback: ' + data.stdResult);
    });
}

async function getProperty(eleGet: Component|UiWindow, property: string): Promise<string> {
    let retProperty: string;
    let info: Map<string, string> = new Map<string, string>();
    if (eleGet instanceof Component) {
        info['id'] = await eleGet.getId();
        info['text'] = await eleGet.getText();
        info['type'] = await eleGet.getType();
        info['description'] = await eleGet.getDescription();
        info['bounds'] = await eleGet.getBounds();
        info['boundsCenter'] = await eleGet.getBoundsCenter();
        info['isClickable'] = await eleGet.isClickable();
        info['isLongClickable'] = await eleGet.isLongClickable();
        info['isScrollable'] = await eleGet.isScrollable();
        info['isEnabled'] = await eleGet.isEnabled();
        info['isFocused'] = await eleGet.isFocused();
        info['isSelected'] = await eleGet.isSelected();
        info['isChecked'] = await eleGet.isChecked();
        info['isCheckable'] = await eleGet.isCheckable();
    }
    else{
        info['bundleName'] = await eleGet.getBundleName();
        info['bounds'] = await eleGet.getBounds();
        info['title'] = await eleGet.getTitle();
        info['windowMode'] = await eleGet.getWindowMode();
        info['isFocused'] = await eleGet.isFocused();
        info['isActived'] = await eleGet.isActived();
        info['isActive'] = await eleGet.isActive();
    }
    if (property == 'info') {
        retProperty = JSON.stringify(info);
    }
    else {
        retProperty = info[property]
        if (!retProperty) {
            retProperty = `unknown property: ${property}`;
        }
    }
    return retProperty;
}

async function doOperate(eleOperate: Component, operate: string, extend: string): Promise<string> {
    let ret: string = "";
    switch (operate) {
        case "click":
            await eleOperate.click();
            eleMap = new Map<string, Component>();
            break;
        case "doubleClick":
            await eleOperate.doubleClick();
            eleMap = new Map<string, Component>();
            break;
        case "longClick":
            await eleOperate.longClick();
            eleMap = new Map<string, Component>();
            break;
        case "input":
            await eleOperate.inputText(extend);
            break;
        case "clear":
            await eleOperate.clearText();
            break;
        case "scrollToTop":
            await eleOperate.scrollToTop(parseFloat(extend));
            break;
        case "scrollToBottom":
            await eleOperate.scrollToBottom(parseFloat(extend));
            break;
        case "dragTo":
            let ele:Component = eleMap[extend]
            if (!ele){
                ret = `no element: ${extend}`;
            }else{
                await eleOperate.dragTo(ele);
            }
            break;
        case "pinchOut":
            await eleOperate.pinchOut(parseFloat(extend));
            break;
        case "pinchIn":
            await eleOperate.pinchIn(parseFloat(extend));
            break;
        default:
            ret = `unknown operate: ${operate}`;
    }
    await commonWaitIdle();
    return ret;
}

async function generateOn(by:string, data:string, findby: On|null): Promise<On|null>{
    if (findby){
        switch (by) {
            case "id":
                findby = findby.id(data);
                break;
            case "text":
                findby = findby.text(data);
                break;
            case "type":
                findby = findby.type(data);
                break;
            case "description":
                findby = findby.description(data);
                break;
            case "clickable":
                findby = findby.clickable(Boolean(data));
                break;
            case "longClickable":
                findby = findby.longClickable(Boolean(data));
                break;
            case "scrollable":
                findby = findby.scrollable(Boolean(data));
                break;
            case "enabled":
                let enabled = Boolean(data);
                findby = findby.enabled(enabled);
                break;
            case "focused":
                findby = findby.focused(Boolean(data));
                break;
            case "selected":
                findby = findby.selected(Boolean(data));
                break;
            case "checked":
                findby = findby.checked(Boolean(data));
                break;
            case "checkable":
                findby = findby.checkable(Boolean(data));
                break;
            case "isBefore":
                let other: Map<string,string> = data['params']
                let beforeOn:On|null  = await generateOn(other['by'], other['data'], null)
                findby = findby.isBefore(beforeOn);
                break;
            case "isAfter":
                let after: Map<string,string> = data['params']
                let afterOn:On|null  = await generateOn(after['by'], after['data'], null)
                findby = findby.isAfter(afterOn);
                break;
        }
    }
    else{
        switch (by) {
            case "id":
                findby = ON.id(data);
                break;
            case "text":
                findby = ON.text(data);
                break;
            case "type":
                findby = ON.type(data);
                break;
            case "description":
                findby = ON.description(data);
                break;
            case "clickable":
                findby = ON.clickable(Boolean(data));
                break;
            case "longClickable":
                findby = ON.longClickable(Boolean(data));
                break;
            case "scrollable":
                findby = ON.scrollable(Boolean(data));
                break;
            case "enabled":
                let enabled = Boolean(data);
                findby = ON.enabled(enabled);
                break;
            case "focused":
                findby = ON.focused(Boolean(data));
                break;
            case "selected":
                findby = ON.selected(Boolean(data));
                break;
            case "checked":
                findby = ON.checked(Boolean(data));
                break;
            case "checkable":
                findby = ON.checkable(Boolean(data));
                break;
            case "isBefore":
                let other: Map<string,string> = data['params']
                let beforeOn:On|null = await generateOn(other['by'], other['data'], null)
                findby = ON.isBefore(beforeOn);
                break;
            case "isAfter":
                let after: Map<string,string> = data['params']
                let afterOn:On|null  = await generateOn(after['by'], after['data'], null)
                findby = ON.isAfter(afterOn);
                break;
        }
    }
    return findby;
}

async function getOn(params:Map<string,string>): Promise<On | null> {
    let by: string = params['by']
    let data: string = params['data']
    let other: Map<string,string> = params['params']
    myPrint("== find element On: "+ JSON.stringify(params));
    let curOn: On|null = await generateOn(by, data, null)
    if (other){
        Object.keys(other).forEach( async (key) =>{
            curOn = await generateOn(key, other[key], curOn)
        })
    }
    return curOn;
}

async function commonWaitIdle() {
    myPrint(`before waitIdle}`);
    let waitIdle = await driver.waitForIdle(2000, 5000);
    myPrint(`waitIdle: ${waitIdle}`);
}

async function checkParams(params:Map<string,string>, key: string): Promise<request.RequestData[]>{
    let retData:request.RequestData[] = []
    if (params[key] == undefined) {
        return retData.concat([{ name: "ret", value: "error" }, {
            name: "description",
            value: `msg must include parameter '${key}'`
        }]);
    }
    return retData
}

async function clickHandler(msg: Map<string, string>, key: string): Promise<request.RequestData[]>{
    let retData:request.RequestData[] = []
    retData = await checkParams(msg, 'x')
    if (retData.length > 0){
        return retData;
    }
    retData = await checkParams(msg, 'y')
    if (retData.length > 0){
        return retData;
    }
    let x: string = msg["x"];
    let y: string = msg["y"];
    switch(key){
        case "click":
            await driver.click(Number(x), Number(y));
            break;
        case "doubleClick":
            await driver.doubleClick(Number(x), Number(y));
            break;
        case "longClick":
            await driver.longClick(Number(x), Number(y));
            break;
    }
    eleMap = new Map<string, Component>();
    await commonWaitIdle();
    return retData.concat([{ name: "data", value: "ok" }])
}


// export async function action(context: Context, msg:Map<string, string>): Promise<request.RequestData[]> {
export async function action(msg: Map<string, string>): Promise<request.RequestData[]> {
    // myPrint("action start");
    let sendData: request.RequestData[] = [];
    try {
        // myPrint(`msg: ${JSON.stringify(msg)}`);
        if (msg["uuid"] == undefined) {
            return sendData.concat([{ name: "ret", value: "error" }, {
                name: "description",
                value: "msg must include parameter 'uuid'"
            }]);
        }
        const uuid: string = msg["uuid"];
        sendData.push({ name: "uuid", value: uuid });
        if (msg["action"] == undefined) {
            return [{ name: "ret", value: "error" }, {
                name: "description",
                value: "msg must include parameter 'action'"
            }];
        }
        const action: string = msg["action"];
        // myPrint(`action: ${action}. uuid: ${uuid}`)

        switch (action) {
            case "find":
                // 单控件查找
                let retData = await checkParams(msg, 'by')
                if (retData.length > 0){
                    return sendData.concat(retData);
                }
                retData = await checkParams(msg, 'data')
                if (retData.length > 0){
                    return sendData.concat(retData);
                }
                let curOn: On | null = await getOn(msg)
                if (curOn == null) {
                    return sendData.concat([{ name: "ret", value: "error" }, {
                        name: "description",
                        value: `unknown by: ${msg["by"]}`
                    }]);
                }
                let ele: Component;
                if (msg["timeout_s"] == undefined || msg["timeout_s"] == "0") {
                    ele = await driver.findComponent(curOn!);
                } else {
                    ele = await driver.waitForComponent(curOn!, Number(msg["timeout_s"]) * 1000);
                }
                if (ele == null) {
                    return sendData.concat([{ name: "ret", value: "error" }, {
                        name: "description",
                        value: `no ele: ${msg["by"]} ${msg["data"]}`
                    }]);
                }
                eleMap[uuid] = ele;
                sendData.push({ name: "euid", value: uuid });
                let info = await getProperty(ele, 'info');
                sendData.push({ name: 'property', value: info });
                return sendData;
                break;
            case "finds":
                // 多控件查找
                retData = await checkParams(msg, 'by')
                if (retData.length > 0){
                    return sendData.concat(retData);
                }
                retData = await checkParams(msg, 'data')
                if (retData.length > 0){
                    return sendData.concat(retData);
                }
                let curOnFinds: On | null = await getOn(msg)
                if (curOnFinds == null) {
                    return sendData.concat([{ name: "ret", value: "error" }, {
                        name: "description",
                        value: `unknown by: ${msg["by"]}`
                    }]);
                }
                let eleArray: Component[] = await driver.findComponents(curOnFinds!);
                if (eleArray == null) {
                    return sendData.concat([{ name: "data", value: "[]" }]);
                }
                let eleMapArray: Map<string, string>[] = [];
                for (let ii = 0; ii < eleArray.length; ii++) {
                    let tmpEuid = `${uuid}${ii}`;
                    eleMap[tmpEuid] = eleArray[ii];
                    let tmpE: Map<string, string> = new Map<string, string>();
                    tmpE["euid"] = tmpEuid;
                    eleMapArray.push(tmpE)
                }
                for (let eleIndex = 0; eleIndex < eleArray.length; eleIndex++) {
                    let info = await getProperty(eleArray[eleIndex], 'info');
                    eleMapArray[eleIndex]['property'] = info;
                }
                if (eleMapArray.length == 0) {
                    return sendData.concat([{ name: "ret", value: "error" }, {
                        name: "description",
                        value: `no ele: ${msg["by"]} ${msg["data"]}`
                    }]);
                }
                return sendData.concat([{ name: "data", value: JSON.stringify(eleMapArray) }]);
                break;
            case "get":
                // 控件属性获取
                retData = await checkParams(msg, 'euid')
                if (retData.length > 0){
                    return sendData.concat(retData);
                }
                retData = await checkParams(msg, 'property')
                if (retData.length > 0){
                    return sendData.concat(retData);
                }
                let euidGet: string = msg["euid"];
                let property: string = msg["property"];
                let eleGet: Component = eleMap[euidGet];
                if (eleGet == undefined) {
                    return sendData.concat([{ name: "ret", value: "error" }, {
                        name: "description",
                        value: `get ele failed by euid '${euidGet}', before get property`
                    }]);
                }
                let retProperty: string = await getProperty(eleGet, property);
                if (retProperty.startsWith("unknown property")) {
                    return sendData.concat([{ name: "ret", value: "error" }, {
                        name: "description",
                        value: `unknown property: ${property}`
                    }]);
                }
                return sendData.concat([{ name: "data", value: retProperty }])
            case "operate":
                // 控件元素操作
                retData = await checkParams(msg, 'euid')
                if (retData.length > 0){
                    return sendData.concat(retData);
                }
                retData = await checkParams(msg, 'operate')
                if (retData.length > 0){
                    return sendData.concat(retData);
                }
                let euidOperate: string = msg["euid"];
                let operate: string = msg["operate"];
                let eleOperate: Component = eleMap[euidOperate];
                if (eleOperate == undefined) {
                    return sendData.concat([{ name: "ret", value: "error" }, {
                        name: "description",
                        value: `get ele failed by euid '${euidOperate}, before operate'`
                    }]);
                }
                let inputText = "";
                if (operate == "input") {
                    if (msg["text"] == undefined) {
                        return sendData.concat([{ name: "ret", value: "error" }, {
                            name: "description",
                            value: "msg must include parameter 'text'"
                        }]);
                    }
                    inputText = msg["text"];
                }
                else{
                    inputText = msg["param"]
                }
                if (operate == "scrollSearch"){
                    // 滑动查找目标控件
                    let params:Map<string, string> = JSON.parse(inputText);
                    let curOn: On | null = await getOn(params)
                    if (curOn == null) {
                        return sendData.concat([{ name: "ret", value: "error" }, {
                            name: "description",
                            value: `unknown by: ${params["by"]}`
                        }]);
                    }
                    let ele: Component = await eleOperate.scrollSearch(curOn)
                    if (ele == null) {
                        return sendData.concat([{ name: "ret", value: "error" }, {
                            name: "description",
                            value: `no ele: ${params["by"]} ${params["data"]}`
                        }]);
                    }
                    eleMap[uuid] = ele;
                    sendData.push({ name: "euid", value: uuid });
                    let info = await getProperty(ele, 'info');
                    sendData.push({ name: 'property', value: info });
                }
                else{
                    let retOperate: string = await doOperate(eleOperate, operate, inputText);
                    if (retOperate) {
                        return sendData.concat([{ name: "ret", value: "error" }, {
                            name: "description",
                            value: retOperate
                        }]);
                    }
                    return sendData.concat([{ name: "data", value: "ok" }])
                }
            case "click":
            case "doubleClick":
            case "longClick":
                // 单击、双击、长按
                retData = await clickHandler(msg, action)
                return sendData.concat(retData)
            case "swipe":
            case "drag":
                // 滑动、拖动
                if (msg["startx"] == undefined || msg["starty"] == undefined || msg["endx"] == undefined || msg["endy"] == undefined || msg["speed"] == undefined) {
                    return sendData.concat([{ name: "ret", value: "error" }, {
                        name: "description",
                        value: "msg must include parameters 'startx' 'starty' 'endx' 'endy' 'speed'"
                    }]);
                }
                let startx: number = Number(msg["startx"]);
                let starty: number = Number(msg["starty"]);
                let endx: number = Number(msg["endx"]);
                let endy: number = Number(msg["endy"]);
                let speed: number = Number(msg["speed"]);
                if (action == "swipe") {
                    await driver.swipe(startx, starty, endx, endy, speed);
                }
                else{
                    await driver.drag(startx, starty, endx, endy, speed);
                }
                eleMap = new Map<string, Component>();
                await commonWaitIdle();
                return sendData.concat([{ name: "data", value: "ok" }])
            case "fling":
                retData = await checkParams(msg, 'direction')
                if (retData.length > 0){
                    return retData;
                }
                retData = await checkParams(msg, 'speed')
                if (retData.length > 0){
                    return retData;
                }
                let direction: UiDirection = Number(msg["direction"]);
                speed = Number(msg["speed"]);
                await driver.fling(direction, speed);
                eleMap = new Map<string, Component>();
                await commonWaitIdle();
                return sendData.concat([{ name: "data", value: "ok" }])
            case "home":
                await driver.pressHome();
                eleMap = new Map<string, Component>();
                await commonWaitIdle();
                return sendData.concat([{ name: "data", value: "ok" }])
            case "back":
                await driver.pressBack();
                eleMap = new Map<string, Component>();
                await commonWaitIdle();
                return sendData.concat([{ name: "data", value: "ok" }])
            case "keyEvent":
                retData = await checkParams(msg, 'key')
                if (retData.length > 0){
                    return sendData.concat(retData);
                }
                let key1: number = msg['key1'] ? Number(msg['key1']) : 0;
                let key2: number = msg['key2'] ? Number(msg['key2']) : 0;
                if (key1 == 0){
                    // 单个按键事件
                    await driver.triggerKey(Number(msg['key']))
                }else{
                    // 组合按键事件
                    await driver.triggerCombineKeys(msg['key'], key1, key2)
                }
                eleMap = new Map<string, Component>();
                await commonWaitIdle();
                return sendData.concat([{ name: "data", value: "ok" }])
            case "setRotation":
                retData =  await checkParams(msg, 'rotation')
                if (retData.length > 0){
                    return sendData.concat(retData);
                }
                await driver.setDisplayRotationEnabled(true);
                await driver.setDisplayRotation(Number(msg['rotation']));
                let rotation = await driver.getDisplayRotation();
                await commonWaitIdle();
                return sendData.concat([{ name: "data", value: rotation.toString() }])
            case "getRotation":
                let curRote = await driver.getDisplayRotation();
                await commonWaitIdle();
                return sendData.concat([{ name: "data", value: curRote.toString() }])
            case "currentBundle":
                let window = await driver.findWindow({ actived: true });
                let name = await window.getBundleName();
                return sendData.concat([{ name: "data", value: name }])
            case "screenSize":
                let screenSize = await driver.getDisplaySize();
                return sendData.concat([{ name: "data", value: JSON.stringify(screenSize) }])
            case "wakeup":
                await driver.wakeUpDisplay()
                return sendData.concat([{ name: "data", value: "ok" }])
            case "app":
                retData = await checkParams(msg, 'cmd')
                if (retData.length > 0){
                    return sendData.concat(retData);
                }
                retData = await checkParams(msg, 'bundle')
                if (retData.length > 0){
                    return sendData.concat(retData);
                }
                let cmd: string = msg["cmd"];
                let bundle: string = msg["bundle"];
                if (msg["ability"] == undefined && cmd == "start") {
                    return sendData.concat([{ name: "ret", value: "error" }, {
                        name: "description",
                        value: "msg must include parameter 'ability'"
                    }]);
                }
                let ability: string = msg["ability"];
                let shellCmd: string;
                switch (cmd) {
                    case "start":
                        shellCmd = `aa start -b ${bundle} -a ${ability}`;
                        break;
                    case "stop":
                        shellCmd = `aa force-stop ${bundle}`;
                        break;
                    default:
                        return sendData.concat([{ name: "ret", value: "error" }, {
                            name: "description",
                            value: `unknown app cmd: ${cmd}`
                        }]);
                }
                await execShell(shellCmd);
                let appWaitIdle = await driver.waitForIdle(5000, 8000);
                myPrint(`appWaitIdle: ${appWaitIdle}`);
                eleMap = new Map<string, Component>();
                return sendData.concat([{ name: "data", value: "ok" }])
            case "window":
                retData = await checkParams(msg, 'operate')
                if (retData.length > 0){
                    return sendData.concat(retData);
                }
                if (msg['operate'] == 'find'){
                    // 查找window
                    retData = await checkParams(msg, 'filter')
                    if (retData.length > 0){
                        return sendData.concat(retData);
                    }
                    let window = await driver.findWindow(msg['filter'])
                    windowMap[uuid] = window;
                    sendData.push({ name: "euid", value: uuid });
                    let info = await getProperty(window, 'info');
                    sendData.push({ name: 'property', value: info });
                    return sendData;
                }
                else {
                    let wuidGet: string = msg["wuid"];
                    let winGet: UiWindow = windowMap[wuidGet];
                    if (winGet == undefined) {
                        return sendData.concat([{ name: "ret", value: "error" }, {
                            name: "description",
                            value: `get window failed by euid '${wuidGet}', before get property`
                        }]);
                    }
                    if (msg['operate'] == 'get') {
                        // 获取窗口属性
                        retData = await checkParams(msg, 'property')
                        if (retData.length > 0) {
                            return sendData.concat(retData);
                        }
                        let property: string = msg["property"];
                        let retProperty: string = await getProperty(winGet, property);
                        if (retProperty.startsWith("unknown property")) {
                            return sendData.concat([{ name: "ret", value: "error" }, {
                                name: "description",
                                value: `unknown property: ${property}`
                            }]);
                        }
                        return sendData.concat([{ name: "data", value: retProperty }])
                    }
                    else if (msg['oprate'] == 'action') {
                        retData = await checkParams(msg, 'func')
                        if (retData.length > 0) {
                            return sendData.concat(retData);
                        }
                        let func: string = msg['func']
                        switch (func) {
                            case "focus":
                                await winGet.focus()
                                return sendData.concat([{ name: "data", value: "ok" }])
                            case "moveTo":
                                let x:number = Number(msg['x'])
                                let y:number = Number(msg['y'])
                                await winGet.moveTo(x, y)
                                return sendData.concat([{ name: "data", value: "ok" }])
                            case "maximize":
                                await winGet.maximize()
                                return sendData.concat([{ name: "data", value: "ok" }])
                            case "minimize":
                                await winGet.minimize()
                                return sendData.concat([{ name: "data", value: "ok" }])
                            case "resume":
                                await winGet.resume()
                                return sendData.concat([{ name: "data", value: "ok" }])
                            case "close":
                                await winGet.close()
                                return sendData.concat([{ name: "data", value: "ok" }])
                            default:
                                return sendData.concat([{ name: "ret", value: "error" }, {
                                    name: "description",
                                    value: `unknown action: ${func}`
                                }]);
                        }
                    }
                }
            default:
                return sendData.concat([{ name: "ret", value: "error" }, {
                    name: "description",
                    value: `unknown action: ${action}`
                }]);
        }
    } catch (err) {
        console.error(`UiTestCase: action: ${msg}. err: ${err}`);
        return sendData.concat([{ name: "ret", value: "error" }, {
            name: "description",
            value: `unknown error: ${err}`
        }]);
    }
}
