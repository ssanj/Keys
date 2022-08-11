import sublime
import sublime_plugin
from typing import Dict, List, Tuple, Any, Optional


class KeysCommand(sublime_plugin.WindowCommand):

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
      keymaps = sublime.find_resources("*.sublime-keymap")
      loaded_keymaps_pair: List[Tuple[str, str]] = [(key_map_file, sublime.load_resource(key_map_file)) for key_map_file in keymaps if "(Linux)" not in key_map_file if "(Windows)" not in key_map_file]
      list_keymap_dict: List[Tuple[str, List[Dict[str, Any]]]] = [(fn, sublime.decode_value(content)) for (fn, content) in loaded_keymaps_pair]

      key_content = ""
      for n, (fn, d) in enumerate(list_keymap_dict):
        if KeysCommand.is_filtered_package(fn):
          key_content += (f"\n{fn}\n")
          key_content += f"{'=' * len(fn)}\n"
          for els in d:
            keys: List[str] = list(map(lambda k: k.upper(), els['keys']))
            command = els['command']
            key_content += f"  {keys} -> {command}\n"

      # print(key_content)
      view = window.new_file(sublime.TRANSIENT)
      view.set_name("Keys")
      view.run_command('view_keys', {"content": key_content})
    else:
      sublime.message_dialog("No Window found")


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













