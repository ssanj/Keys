import sublime
from typing import Dict, List
from Keys.Components.ConfigSettings import ConfigSettings

class SettingsLoader:

  @staticmethod
  def load_settings() -> ConfigSettings:
    # TODO: move to config
    packages_to_filter_in: List[str] = \
      [
        "Packages/User/",
        "Packages/SymbolView/",
        "Packages/RecentFolders/",
        "Packages/QuickView/",
        "Packages/QuickView/",
        "Packages/OpenWindows/",
        "Packages/OpenTabs/",
        "Packages/OpenSplit/",
        "Packages/Keys/",
        "Packages/Ghomments/",
        "Packages/BlogTools/",
        "Packages/Scoggle/",
        "Packages/Quick File Creator/",
        "Packages/LSP/",
        "Packages/Default/",
      ]

    symbol_map: Dict[str, str] = \
      {
        "COMMAND": "⌘",
        "SUPER": "⌘",
        "PRIMARY": "⌘",
        "CTRL": "⌃",
        "OPTION": "⌥",
        "ALT": "⌥",
        "SHIFT": "⇧",
        "UP": "↑",
        "DOWN": "↓",
        "TAB": "⇥",
        "LEFT": "←",
        "RIGHT": "→",
      }

    return ConfigSettings(packages_to_filter_in, symbol_map)
