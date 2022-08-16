import sublime
from typing import Dict, List, Any
from Keys.Components.ConfigSettings import ConfigSettingsHelper
from Keys.Components.ConfigSettings import ConfigSettings, CommandArgsKey, CommandLabel

class SettingsLoader:

  @staticmethod
  def load_settings() -> ConfigSettings:
    settings: sublime.Settings = sublime.load_settings('Keys.sublime-settings')
    # include every package by default if there are no settings
    default_packages_to_filter_in: List[str] = ["Packages/"]
    # turn debug on if we can't load settings :)
    default_debug = True

    # no mappings by default
    default_symbol_map: Dict[str, str] = {}

    default_label_map: Dict[CommandArgsKey, CommandLabel] = {}

    packages_to_filter_in = \
      settings.get('packages_to_filter_in') if settings.has('packages_to_filter_in') else default_packages_to_filter_in

    symbol_map = \
      settings.get('symbol_map') if settings.has('symbol_map') else default_symbol_map

    label_map:Dict[CommandArgsKey, CommandLabel] = \
      SettingsLoader.load_label_map(settings.get('label_map_list')) if settings.has('label_map_list') else default_label_map


    debug = settings.get('debug') if settings.has('debug') else default_debug

    if debug:
      print(f"Keys:settings:{settings.to_dict()}")
      print(f"Keys:settings:using packages_to_filter_in={packages_to_filter_in}")
      print(f"Keys:settings:using symbol_map={symbol_map}")
      print(f"Keys:settings:using label_map_list={label_map}")
      print(f"Keys:settings:using debug is on, turn these messages off by setting 'debug: false' in Keys.sublime-settings")

    return ConfigSettings(packages_to_filter_in, symbol_map, label_map)

  @staticmethod
  def load_label_map(label_map_list: List[Dict[str, Any]]) ->  Dict[CommandArgsKey, CommandLabel]:
    print(f"-------------> loading {label_map_list}")
    label_map: Dict[CommandArgsKey, CommandLabel] = {}
    for lm in label_map_list:
      if 'command' in lm and 'args' in lm and 'label' in lm:
        command: str = lm['command']
        args: Dict[str, Any] = lm['args']
        label: str = lm['label']
        key: CommandArgsKey = ConfigSettingsHelper.label_key(command, args)
        value: CommandLabel = CommandLabel(command, args, label)
        label_map.update({key: value})

    return label_map

