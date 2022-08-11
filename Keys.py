import sublime
import sublime_plugin
from typing import Dict, List, Tuple, Any, Optional
from Keys.Components.KeyInfo import KeyInfo, Command, FileName, Key

class KeysCommand(sublime_plugin.WindowCommand):

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
    ]

  @staticmethod
  def is_filtered_package(package: str) -> bool:
    return len(list(filter(lambda p: package.startswith(p), KeysCommand.packages_to_filter_in))) > 0

  def run(self) -> None:
    window = self.window

    if window:
      key_info_list: List[KeyInfo] = self.get_key_info()

      key_content = ""
      for key_info in key_info_list:
        fn = key_info.file_name.value
        command = key_info.command.value
        keys = key_info.key_combo()

        key_content += (f"{fn}\n")
        key_content += f"{'=' * len(fn)}\n"
        key_content += f"  {keys} -> {command}\n\n"

      # print(key_content)
      view = window.new_file(sublime.TRANSIENT)
      view.set_name("Keys")
      view.run_command('view_keys', {"content": key_content})
    else:
      sublime.message_dialog("No Window found")

  def get_key_info(self) -> List[KeyInfo]:
    # Should we cache this information?
    keymaps = sublime.find_resources("*.sublime-keymap")
    loaded_keymaps_pair: List[Tuple[str, str]] = [(key_map_file, sublime.load_resource(key_map_file)) for key_map_file in keymaps if "(Linux)" not in key_map_file if "(Windows)" not in key_map_file]
    list_keymap_dict: List[Tuple[str, List[Dict[str, Any]]]] = [(fn, sublime.decode_value(content)) for (fn, content) in loaded_keymaps_pair]

    key_info_list: List[KeyInfo] = []
    for n, (fn, d) in enumerate(list_keymap_dict):
      if KeysCommand.is_filtered_package(fn):
        file_name = FileName(fn)
        for els in d:
          possible_keys: List[str] = list(map(lambda k: k.upper(), els['keys']))
          assert len(possible_keys) > 0, "should have at least one key defined"
          separate_keys: List[str] = possible_keys[0].split("+") # assume at least one key
          keys: List[Key] = list(map(lambda k: Key(k.upper()), separate_keys))
          command = Command(els['command'])
          key_info_list.append(KeyInfo(file_name, command, keys))


    return key_info_list

class ViewKeysCommand(sublime_plugin.TextCommand):

  def run(self, edit:sublime.Edit, **args) -> None:
    view = self.view
    print(f"args: {args}")
    if view:
      view.insert(edit, 0, args['content'])
      view.set_read_only(True)
      view.set_scratch(True)
    else:
      sublime.message_dialog("No View found")













