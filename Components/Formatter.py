from Keys.Components.KeyInfo import KeyInfo
from typing import List


class Formatter:

  @staticmethod
  def key_combo(key_info: KeyInfo) -> str:
   return '+'.join(list(map(lambda k: k.value, key_info.keys)))

  @staticmethod
  def command_title_case(key_info: KeyInfo) -> str:
    command_value: str = key_info.command.value
    plain_value: List[str] = command_value.split("_")
    titled_value: List[str] = list(map(lambda w: w.title(), plain_value))
    return " ".join(titled_value)
