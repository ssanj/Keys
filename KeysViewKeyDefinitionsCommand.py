import sublime
import sublime_plugin
from typing import List, Optional
from Keys.Components.SettingsLoader import SettingsLoader
from Keys.Components.KeyInfo import KeyInfo
from Keys.Components.Formatter import Formatter
from Keys.Components.KeyLogic import KeyLogic

class KeysViewKeyDefinitionsCommand(sublime_plugin.WindowCommand):

  VIEW_ID = "keys_command_view"

  def run(self) -> None:
    window = self.window

    settings: sublime.Settings = SettingsLoader.load_settings()

    if window:
      key_info_list: List[KeyInfo] = KeyLogic.get_key_info(settings)

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


      found_keys_view = self.find_keys_view(window)
      view = self.create_new_view(window) if not found_keys_view else found_keys_view
      view.run_command('view_keys', {"content": key_content})
    else:
      sublime.message_dialog("No Window found")

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
