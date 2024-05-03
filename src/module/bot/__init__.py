from .kind import CallerKind
from ..interface import BasicModule


BOT = "bot"
BASE_PATH = f"module.{BOT}"

class BasicBot(BasicModule):
    system_prompt = "你现在是一名主播，请回答观众问题，请将回答控制在10字以内。"

    def __init__(self):
        super().__init__(BOT)

    def _load_config(self):
        pass

    def talk(self, query: str) -> str:
        return self._sub_modules["caller"].single_call(query)
    
    def caller_kind(self) -> CallerKind:
        return self._caller.kind