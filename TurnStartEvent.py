import dataclasses

from GameLogEvent import GameLogEvent

@dataclasses.dataclass
class TurnStartEvent(GameLogEvent):

	turn_number: int
	player_username: str

