from Keys.Components.ConfigSettings import ConfigSettings
from Keys.Components.KeyInfo import KeyInfo, Key
from Keys.Components.KeyLogic import KeyLogic
from typing import List, Dict, Any

class Formatter:

  @staticmethod
  def key_combo(key_info: KeyInfo) -> str:
   return '+'.join(list(map(lambda k: k.value, key_info.keys)))

  @staticmethod
  def get_symbolic_keys(settings: ConfigSettings, key_info: KeyInfo) -> str:
    key_items: List[str] = list(map(lambda k: Formatter.get_symbolic(settings, k).value, key_info.keys))
    return "+".join(key_items)

  @staticmethod
  def get_symbolic(settings: ConfigSettings, key: Key) -> Key:
    key_value = key.value.upper()
    if key_value in settings.symbol_map:
      return Key(settings.symbol_map[key_value])
    else:
      return key

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

  @staticmethod
  def context(key_info: KeyInfo) -> List[str]:
    if key_info.context:
      context: List[Dict[str, Any]] = key_info.context.value
      context_str: List[str] = []
      for rule in context:
        rule_items: List[str] = list(map(lambda kv: f"{kv[0]} -> [{Formatter.decode(kv[1])}]", rule.items()))
        rule_str: str = ", ".join(rule_items)
        context_str.append(rule_str)
      return context_str
    else:
      return []

  @staticmethod
  def decode(context_value: str) -> str:
    if context_value == "\n":
      return "<newline>"
    else:
      return context_value
