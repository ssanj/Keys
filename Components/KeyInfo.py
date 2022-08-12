from typing import NamedTuple, List

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
