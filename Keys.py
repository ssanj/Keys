import sublime
import sublime_plugin
from typing import Dict, List, Tuple, Any, Optional
from Keys.Components.KeyInfo import KeyInfo, Command, FileName, Key, Args, Context
from Keys.Components.Formatter import Formatter

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

class KeysCommand(sublime_plugin.WindowCommand):


  def run(self) -> None:
    window = self.window

    if window:
      key_info_list: List[KeyInfo] = KeyLogic.get_key_info()

      key_content = ""
      for key_info in key_info_list:
        fn = key_info.file_name.value
        command = key_info.command.value
        keys = Formatter.key_combo(key_info)
        args = str(key_info.args.value) if key_info.args else "-"
        context_list: List[str] = Formatter.context(key_info)
        context_padding = "\n    "
        context_list.insert(0, "")
        context =  context_padding.join(context_list)

        key_content += (f"{fn}\n")
        key_content += f"{'=' * len(fn)}\n"
        key_content += f"  keys: {keys}\n"
        key_content += f"  command: {command}\n"
        key_content += f"  args: {args}\n"
        key_content += f"  context: {context}\n\n"


      # print(key_content)
      view = window.new_file(sublime.TRANSIENT)
      view.set_name("Keys")
      view.run_command('view_keys', {"content": key_content})
    else:
      sublime.message_dialog("No Window found")



class ViewKeysCommand(sublime_plugin.TextCommand):

  def run(self, edit:sublime.Edit, **args) -> None:
    view = self.view
    if view:
      view.insert(edit, 0, args['content'])
      view.set_read_only(True)
      view.set_scratch(True)
    else:
      sublime.message_dialog("No View found")


class KeysSearchCommand(sublime_plugin.WindowCommand):
  def run(self) -> None:
    window = self.window

    if window:
      key_info_list: List[KeyInfo] = KeyLogic.get_key_info()
      panel_items = list(map(lambda ki: self.create_quick_panel_item(window, ki),key_info_list))
      number_of_items = len(panel_items)
      if number_of_items > 0:
        # Don't show previews
        window.show_quick_panel(
          items = panel_items,
          on_select = self.when_key_selected,
          placeholder = f"Search Keys:"
        )
      else:
        sublime.message_dialog("No keys to display")
    else:
      sublime.message_dialog("No Window found")

  def create_quick_panel_item(self, window: sublime.Window, key_info: KeyInfo) -> sublime.QuickPanelItem:
    command_title_case = Formatter.command_title_case(key_info)
    key_combo = Formatter.key_combo(key_info)
    trigger: str = f"{command_title_case} [{key_combo}]"
    details: List[str] = \
    [
      f"<b>{key_combo}</b>",
      key_info.file_name.value,
      Formatter.args(key_info),
    ]
    has_context = "context" if key_info.context else ""
    has_args = "args" if key_info.args else ""
    annotation_prefix = "has" if has_context or has_args else ""
    annotation_infix = " and " if has_context and has_args else ""
    annotation: str = f"{annotation_prefix} {has_args}{annotation_infix}{has_context}"
    kind = sublime.KIND_AMBIGUOUS
    quick_panel_item = sublime.QuickPanelItem(trigger, details, annotation, kind)
    return quick_panel_item

  def when_key_selected(self, index: int) -> None:
    pass
