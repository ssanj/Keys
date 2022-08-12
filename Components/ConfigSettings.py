from typing import NamedTuple, List, Dict

class ConfigSettings(NamedTuple):
  packages_to_filter_in: List[str]
  symbol_map: Dict[str, str]
