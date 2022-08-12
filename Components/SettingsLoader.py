import sublime
from typing import Dict, List
from Keys.Components.ConfigSettings import ConfigSettings

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

    packages_to_filter_in = \
      settings.get('packages_to_filter_in') if settings.has('packages_to_filter_in') else default_packages_to_filter_in

    symbol_map = \
      settings.get('symbol_map') if settings.has('symbol_map') else default_symbol_map

    debug = settings.get('debug') if settings.has('debug') else default_debug

    if debug:
      print(f"Keys:settings:{settings.to_dict()}")
      print(f"Keys:settings:using packages_to_filter_in={packages_to_filter_in}")
      print(f"Keys:settings:using symbol_map={symbol_map}")
      print(f"Keys:settings:using debug is on, turn these messages off by setting 'debug: false' in Keys.sublime-settings")

    return ConfigSettings(packages_to_filter_in, symbol_map)
