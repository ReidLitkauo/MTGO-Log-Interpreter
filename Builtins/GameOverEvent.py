import dataclasses

from .GameLogEvent import GameLogEvent

@dataclasses.dataclass
class GameOverEvent(GameLogEvent):

	winner: str

