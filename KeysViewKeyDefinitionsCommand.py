import sublime
import sublime_plugin
from typing import List, Optional, Dict
from Keys.Components.SettingsLoader import SettingsLoader
from Keys.Components.KeyInfo import KeyInfo, FileName
from Keys.Components.Formatter import Formatter
from Keys.Components.KeyLogic import KeyLogic
from Keys.Components.ConfigSettings import ConfigSettings

class KeysViewKeyDefinitionsCommand(sublime_plugin.WindowCommand):

  VIEW_ID = "keys_command_view"

  def run(self) -> None:
    window = self.window

    config_settings: ConfigSettings = SettingsLoader.load_settings()

    if window:
      key_info_list: List[KeyInfo] = KeyLogic.get_key_info(settings = config_settings, filter_packages = False)
      key_info_map: Dict[FileName, List[KeyInfo]] = self.list_to_dict(key_info_list)

      key_content = ""
      for (file, keys_in_file) in key_info_map.items():
        file_name = file.value
        file_name_length = len(file_name)
        key_content += f"{'=' * file_name_length}\n"
        key_content += (f"{file_name}\n")
        key_content += f"{'=' * file_name_length}\n"

        for key_info in keys_in_file:
          command = key_info.command.value
          keys = Formatter.key_combo(key_info)
          args = str(key_info.args.value) if key_info.args else "-"
          context_list: List[str] = Formatter.context(key_info)
          context_padding = "\n    "
          context_list.insert(0, "")
          context =  context_padding.join(context_list)

          key_content += f"  keys: {keys}\n"
          key_content += f"  command: {command}\n"
          key_content += f"  args: {args}\n"
          key_content += f"  context: {context}\n"
          key_content += f"{'-' * file_name_length}\n"

        key_content += f"\n"


      found_keys_view = self.find_keys_view(window)
      view = self.create_new_view(window) if not found_keys_view else found_keys_view
      view.run_command('view_keys', {"content": key_content})
    else:
      sublime.message_dialog("No Window found")

  def list_to_dict(self, key_info_list: List[KeyInfo]) -> Dict[FileName, List[KeyInfo]]:
    key_info_by_file_map: Dict[FileName, List[KeyInfo]] = {}
    for ki in key_info_list:
      if ki.file_name not in key_info_by_file_map:
        key_info_by_file_map.update({ki.file_name: [ki]})
      else:
        key_info_by_file_map[ki.file_name].append(ki)

    return key_info_by_file_map

  def create_new_view(self, window: sublime.Window) -> sublime.View:
    view = window.new_file(sublime.TRANSIENT)
    view.set_name("Keys: KeyMap Definitions")
    view.settings().set(KeysViewKeyDefinitionsCommand.VIEW_ID, True)
    return view

  def find_keys_view(self, window: sublime.Window) -> Optional[sublime.View]:
    views = window.views()
    matched_views = [view for view in views if view.settings().has(KeysViewKeyDefinitionsCommand.VIEW_ID)]
    if len(matched_views) > 0:
      return matched_views[0]
    else:
      return None


# View used by KeysViewKeyDefinitionsCommand
class ViewKeysCommand(sublime_plugin.TextCommand):

  def run(self, edit:sublime.Edit, **args) -> None:
    view = self.view
    if view:
      view.erase(edit, sublime.Region(0, view.size()))
      view.insert(edit, 0, args['content'])
      view.set_read_only(True)
      view.set_scratch(True)
    else:
      sublime.message_dialog("No View found")
