from Keys.Components.KeyInfo import KeyInfo
from typing import List, Dict, Any

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

  @staticmethod
  def args(key_info: KeyInfo) -> str:
    if key_info.args:
      args_dict: Dict[str, Any] = key_info.args.value
      items: List[str] = list(map(lambda kv: f"{kv[0]} -> {kv[1]}", args_dict.items()))
      return " ".join(items)
    else:
      return "-"

