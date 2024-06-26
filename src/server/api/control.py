from typing import Dict
from flask import Blueprint, request

from module.interface.info import ModuleName, moduleStatusMap
from module.interface.manager import MANAGER
from utils.config import CONFIG

from .result import Result, ErrorCode

control_api = Blueprint("control_api", __name__)

BOOTER = ModuleName.BOOTER.value


def check_module_can_control(name: str) -> bool:
    if MANAGER.module(name) is None:
        return Result.create(code=ErrorCode.ModuleNotFound)
    elif name == "booter" or name in MANAGER.info(BOOTER).sub:
        # 目前只有 booter 与其子模块才可以单独地启动的暂停
        return None
    else:
        return Result.create(code=ErrorCode.ModuleUncontrollable)


@control_api.route("/module/<regex('start|stop'):control>/<name>", methods=["POST"])
def start(name: str, control: str):
    # 验证启动模块请求
    result = check_module_can_control(name)

    if result is not None:
        return result

    if control == "start":
        # Notice: 启动子模块时，也会递归启动父模块
        MANAGER.start(name, with_sup=True)
    elif control == "stop":
        MANAGER.stop(name)

    # 如果模块启动失败，则说明是当前状态不支持
    # if not flag:
    #     return Result.create(
    #         code=ErrorCode.ModuleStatusNotSupported,
    #         data={"status": status, "statusLabel": moduleStatusMap[status]},
    #     )

    return Result.create()


@control_api.route("/module/change/<name>", methods=["PUT"])
def change_module_kind(name: str):
    data = request.get_json()
    try:
        kind = data["kind"]
    except KeyError:
        return Result.create(code=ErrorCode.KeyDataMissing)

    # 验证模块状态是否修改成功
    try:
        flag, status = MANAGER.change_module_kind(name, kind)
    except FileNotFoundError:
        return Result.create(code=ErrorCode.ModuleNotFound)
    except ValueError:
        return Result.create(code=ErrorCode.ModuleKindNotFound)

    return (
        Result.create()
        if flag
        else Result.create(
            code=ErrorCode.ModuleStatusNotSupported, data={"status": status}
        )
    )


@control_api.route("/module/config/<name>", methods=["PUT"])
def modify_module_config(name: str):

    data = request.get_json()
    try:
        kind = data["kind"]
        content: Dict = data["content"]
    except BaseException:
        return Result.create(code=ErrorCode.KeyDataMissing)

    try:
        CONFIG.update(name, kind, content, save=True)
    except KeyError:
        # 出现未知的配置信息条目
        return Result.create(code=ErrorCode.ModuleConfigItemNotFound)
    except TypeError:
        # 配置信息条目不匹配
        return Result.create(code=ErrorCode.ModuleConfigItemTypeUnmatched)

    return Result.create()


@control_api.route("/module/list/all", methods=["GET"])
def get_all_module():
    return Result.create(data={"list": MANAGER.module_info_list})


@control_api.route("/module/config/<name>", methods=["GET"])
def get_module_config(name: str):
    try:
        config_list = CONFIG.get(name)
    except KeyError:
        config_list = {}

    return Result.create(
        code=ErrorCode.ModuleConfigEmpty if len(config_list) == 0 else ErrorCode.Ok,
        data={"config": config_list},
    )
