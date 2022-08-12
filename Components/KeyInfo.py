from typing import NamedTuple, List, Optional, Dict, Any

class Args(NamedTuple):
  value: Dict[str, Any]

class FileName(NamedTuple):
  value: str

class Command(NamedTuple):
  value: str

class Key(NamedTuple):
  value: str

class KeyInfo(NamedTuple):
  file_name: FileName
  command: Command
  keys: List[Key]
  args: Optional[Args] = None
