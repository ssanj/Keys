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

  def key_combo(self) -> str:
   return '+'.join(list(map(lambda k: k.value, self.keys)))