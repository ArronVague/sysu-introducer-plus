import time
import random as ra

from .interface import CallerInterface
from ..kind import CallerKind

from utils.config import config

RANDOM_ANSWERS = [
    "欢迎欢迎",
    "见到你很高兴",
    "谢谢夸奖",
    "你说得对"
]


class VirtualCaller(CallerInterface):

    def __init__(self):
        super().__init__(CallerKind.Virtual.value)

        # 调研延迟 (单位为 ms)
        self.__delay: int
        # 生成回答策略：
        # 1. true: 从随机答案库中输出一个回答
        # 2. false: 输出我回答了 XXX
        self.__is_random: bool

    def _load_config(self):
        info = self._read_config()

        self.__delay = info['delay'] / 1000
        self.__is_random = info['isRandom']

        if self.__delay < 0:
            raise ValueError("delay must be not negative")
        
    def check(self):
        """如果调用后不会报错且能够正常返回，则检验正常。
        在调用该函数时，会重新加载配置文件中的配置信息。
        因此该函数只运行一次即可。

        Returns:
            bool: 是否正常
        """
        try:
            self._caller.load_config()

            response = self._caller.single_call("hello", with_system_prompt=False)
            return (response != None, None) 
        except Exception as e:
            return (False, e)

    def single_call(self, query: str, with_system_prompt: bool=True) -> str:
        time.sleep(self.__delay)

        if self.__is_random:
            return ra.sample(RANDOM_ANSWERS, 1)[0]
        else:
            return f"我回答了 {query}"
