from abc import ABCMeta, abstractmethod
from module.interface import BasicModule


class CallerInterface(BasicModule, metaclass=ABCMeta):
    # Notice: 在抽象类中仅提供一个默认的 Prompt，不同的 LLM 可能需要分别优化
    default_system_prompt = (
        "你现在是一名青春活泼开朗的“中山大学介绍人”，请回答观众问题，"
        + "你将收到一个用户问题和一段资料，参考资料可能跟问题没有关系，"
        + "请你忽略没有关系的资料，最后请你参考资料回答问题，并将回答控制在30字以内。"
    )

    def __init__(self, system_prompt: str = None):
        super().__init__()
        self._system_prompt = (
            system_prompt
            if system_prompt is not None
            else CallerInterface.default_system_prompt
        )

    def check(self):
        """如果调用后不会报错且能够正常返回，则检验正常。
        在调用该函数时，会重新加载配置文件中的配置信息。
        因此该函数只运行一次即可。

        Returns:
            bool: 是否正常
        """
        self.single_call("hello", with_system_prompt=False)

    # 单条消息的调用（只能输入一条 query）
    @abstractmethod
    def single_call(self, query: str, with_system_prompt: bool = True) -> str: ...
