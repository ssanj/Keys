import sublime
from typing import Dict, List, Tuple, Any, Optional
from Keys.Components.KeyInfo import KeyInfo, Command, FileName, Key, Args, Context

class KeyLogic:

  # TODO: Move this to settings
  packages_to_filter_in = \
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

  @staticmethod
  def is_filtered_package(package: str) -> bool:
    return len(list(filter(lambda p: package.startswith(p), KeyLogic.packages_to_filter_in))) > 0


  @staticmethod
  def get_key_info() -> List[KeyInfo]:
    # Should we cache this information?
    keymaps = sublime.find_resources("*.sublime-keymap")
    loaded_keymaps_pair: List[Tuple[str, str]] = [(key_map_file, sublime.load_resource(key_map_file)) for key_map_file in keymaps if "(Linux)" not in key_map_file if "(Windows)" not in key_map_file]
    list_keymap_dict: List[Tuple[str, List[Dict[str, Any]]]] = [(fn, sublime.decode_value(content)) for (fn, content) in loaded_keymaps_pair]

    key_info_list: List[KeyInfo] = []
    for n, (fn, d) in enumerate(list_keymap_dict):
      if KeyLogic.is_filtered_package(fn):
        file_name = FileName(fn)
        for els in d:
          possible_keys: List[str] = list(map(lambda k: k.upper(), els['keys']))
          assert len(possible_keys) > 0, "should have at least one key defined"
          separate_keys: List[str] = possible_keys[0].split("+") # assume at least one key
          keys: List[Key] = list(map(lambda k: Key(k.upper()), separate_keys))
          command = Command(els['command'])
          args = Args(els['args']) if 'args' in els else None
          context: Optional[Context] = KeyLogic.get_context(els)
          key_info_list.append(KeyInfo(file_name, command, keys, args, context))


    return key_info_list

  @staticmethod
  def get_context(key_dict: Dict[str, Any]) -> Optional[Context]:
    if 'context' in key_dict:
      context_dict_list: List[Dict[str, Any]] = key_dict['context']
      return Context(context_dict_list)
    else:
      return None
