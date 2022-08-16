from typing import NamedTuple, List, Dict, Any, Optional

class CommandLabel(NamedTuple):
  command: str
  args: Dict[str, Any]
  label: str

class CommandArgsKey(NamedTuple):
  value: str

class ConfigSettings(NamedTuple):
  packages_to_filter_in: List[str]
  symbol_map: Dict[str, str]
  label_map: Dict[CommandArgsKey, CommandLabel] = {}
  debug: bool = True

class ConfigSettingsHelper:

  @staticmethod
  def get_label(config_settings: ConfigSettings, command: str, args: Dict[str, Any]) -> Optional[str]:
    key = ConfigSettingsHelper.label_key(command, args)
    if key in config_settings.label_map:
      return config_settings.label_map[key].label
    else:
      return None

  @staticmethod
  def label_key(command: str, args: Dict[str, Any]) -> CommandArgsKey:
    return CommandArgsKey(f"{command}{str(args)}")

  @staticmethod
  def default_labels() -> Dict[CommandArgsKey, CommandLabel]:
    command_labels: List[CommandLabel] = \
      [
        CommandLabel("scoggle", {'matcher': 'prefix_suffix_matcher'}, "Scoggle: Prefix Suffix Matcher"),
        CommandLabel("scoggle", {'matcher': 'prefix_wildcard_suffix_matcher'}, "Scoggle: Prefix Wildcard Suffix Matcher"),
        CommandLabel("scoggle", {'matcher': 'wildcard_prefix_wildcard_suffix_matcher'}, "Scoggle: Prefix Wildcard Suffix Wldcard Matcher"),
        CommandLabel("package", {'style': 'full'}, "Scoggle: Insert Full package"),
        CommandLabel("package", {'style': 'step'}, "Scoggle: Insert Stepped package")
      ]

    label_map: Dict[CommandArgsKey, CommandLabel] = {}
    for cl in command_labels:
      key: CommandArgsKey = ConfigSettingsHelper.label_key(cl.command, cl.args)
      label_map.update({key: cl})

    return label_map
