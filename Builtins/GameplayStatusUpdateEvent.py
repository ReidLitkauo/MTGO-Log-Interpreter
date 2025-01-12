import dataclasses

from .BaseEvent import BaseEvent

@dataclasses.dataclass
class GameplayStatusUpdateEvent(BaseEvent):
	
	@dataclasses.dataclass
	class PlayerGameplayInformation:
		name: str
		mtgo_player_id: int
		library_size: int
		hand_size: int
		life_total: int
		controlled_cards: dict[str, list[int]] = dataclasses.field(default_factory = lambda : {
			'hand': [],
			'battlefield': [],
			'stack': [],
			'graveyard': [],
			'exile': [],
			'library': [],
			'sideboard': [],
			'other': [],
		})

	game_state: dict[str, PlayerGameplayInformation] = dataclasses.field(default_factory = lambda : {})
	
