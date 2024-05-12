from typing import List, Self
from enum import Enum, IntEnum, unique

class ModuleName(Enum):
    Booter = "booter"
    Core = "core"
    Bot = "bot"
    Caller = "caller"
    Searcher = "searcher"
    Crawler = "crawler"

@unique
class ModuleStatus(IntEnum):
    NotLoaded = 0
    Stopped = 1
    Starting = 2
    Started = 3
    Stopping = 4

    def can_change(self: Self) -> bool:
        return self in [ModuleStatus.NotLoaded, ModuleStatus.Stopped]

moduleStatusMap = {
    ModuleStatus.NotLoaded: "未加载",
    ModuleStatus.Stopped: "未运行",
    ModuleStatus.Starting: "启动中",
    ModuleStatus.Started: "运行中",
    ModuleStatus.Stopping: "停止中",
}


class ModuleInfo:
    def __init__(self, name: str, alias: str, 
        kinds: List[str], kind: str, 
        notNull: bool,
        path: str, sub_modules: List[str]
    ):
        # 基本信息
        self.__name = name
        self.__alias = alias
        self.__kind = kind
        self.__kinds: List[str] = kinds
        self.__notNull = notNull
        self.__path = path

        # Notice: 当这个模块支持空时 则需要添加空值类型
        if len(kinds) == 0 and kind == "basic":
            self.__kinds.append("basic")

        if not notNull:
            self.__kinds.insert(0, "null")

        self.__parent_module = None

        # 子模块信息, Notice: Info 是存储对象无关的信息
        self.__sub_modules = sub_modules
        self.__depth = -1

        # 运行状态信息
        # self.__status: ModuleStatus = ModuleStatus.NotLoaded 

    def to_dict(self):
        return {
            "alias": self.alias,
            "name": self.name,
            "kind": self.kind,
            "kinds": self.kinds,
            "modules": self.sub_modules
        }        

    ''' ---- Getter ------ '''
    
    @property
    def name(self) -> str:
        return self.__name

    @property
    def alias(self) -> str:
        return self.__alias

    @property
    def kind(self) -> str:
        """返回当前实现类型"""
        return self.__kind
    
    @property
    def kinds(self) -> List[str]:
        """返回支持的实现类型列表"""
        return self.__kinds
    
    @property
    def notNull(self) -> bool:
        return self.__notNull

    @property
    def path(self) -> str:
        return self.__path

    @property
    def parent_module(self) -> str:
        return self.__parent_module

    @property
    def sub_modules(self) -> List[str]:
        return self.__sub_modules
    
    @property
    def depth(self) -> int:
        return self.__depth
    
    # @property
    # def status(self) -> ModuleStatus:
    #     return self.__status

    ''' ---- Setter ------ '''

    @kind.setter
    def kind(self, kind: str):
        self.__kind = kind

    @depth.setter
    def depth(self, depth: int):
        self.__depth = depth

    @parent_module.setter
    def parent_module(self, name: str):
        self.__parent_module = name

    # @status.setter
    # def status(self, status: ModuleStatus):
    #     self.__status = status