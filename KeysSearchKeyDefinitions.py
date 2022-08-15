import sublime
import sublime_plugin
from typing import Dict, List, Tuple, Any, Optional
from Keys.Components.KeyInfo import KeyInfo, Command, FileName, Key, Args, Context
from Keys.Components.Formatter import Formatter
from Keys.Components.KeyLogic import KeyLogic
from Keys.Components.ConfigSettings import ConfigSettings
from Keys.Components.SettingsLoader import SettingsLoader

class KeysSearchKeyDefinitionsCommand(sublime_plugin.WindowCommand):

  def run(self) -> None:
    window = self.window

    config_settings: ConfigSettings = SettingsLoader.load_settings()

    if window:
      key_info_list: List[KeyInfo] = KeyLogic.get_key_info(settings = config_settings, filter_packages = True)
      panel_items = list(map(lambda ki: self.create_quick_panel_item(config_settings, window, ki),key_info_list))
      number_of_items = len(panel_items)
      if number_of_items > 0:
        # Don't show previews
        window.show_quick_panel(
          items = panel_items,
          on_select = lambda n: self.when_key_selected(config_settings, window, key_info_list, n),
          placeholder = f"Search Keys:"
        )
      else:
        sublime.message_dialog("No keys to display")
    else:
      sublime.message_dialog("No Window found")

  def create_quick_panel_item(self, settings: ConfigSettings, window: sublime.Window, key_info: KeyInfo) -> sublime.QuickPanelItem:
    command_title_case = Formatter.command_title_case(key_info)
    key_combo = Formatter.key_combo(key_info)
    symbolic_key_combo: str = Formatter.get_symbolic_keys(settings, key_info)
    trigger: str = f"{command_title_case} [{key_combo}]"
    details: List[str] = \
    [
      f"<b>{symbolic_key_combo}</b>",
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

  def when_key_selected(self, settings: ConfigSettings, window: sublime.Window, key_info_list: List[KeyInfo], index: int) -> None:
    if index >= 0 and len(key_info_list) > index:
      key_info = key_info_list[index]
      key_combo = Formatter.key_combo(key_info)
      key_combo_symbolic = Formatter.get_symbolic_keys(settings, key_info)
      command = Formatter.command_title_case(key_info)
      # Possibly add more data to the popup (context, args)
      # move out styling to theme
      html_content = f"""
      <H3 style="color:salmon">{command}</H3>
      <H1>{key_combo}</H1>
      <H1>{key_combo_symbolic}</H1>
      """
      view = window.active_view()
      if view:
        view.show_popup(content = html_content, flags = sublime.HIDE_ON_CHARACTER_EVENT, max_width = 640, max_height = 480)
      else:
        sublime.message_dialog(key_combo)
