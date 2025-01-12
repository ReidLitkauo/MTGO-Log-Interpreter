import json
import re

from .BaseEvent import BaseEvent
from .BaseProcessor import BaseProcessor
from .GameplayStatusUpdateEvent import GameplayStatusUpdateEvent

class GameplayStatusUpdateProcessor(BaseProcessor):
	
	__regex: re.Pattern = re.compile('\\d\\d:\\d\\d:\\d\\d \\[INF\\] \\(Twitch Info\\|Game Play Status Update.*\\) (\\{.*\\})')

	def process(self, raw_event: BaseEvent) -> GameplayStatusUpdateEvent | None:
		raw_event = super().process(raw_event)
		if not raw_event:
			return None
		match = self.__regex.match(raw_event.raw_contents)
		if not match:
			return None
		raw_dict = json.loads(match.group(1))
		event = GameplayStatusUpdateEvent( **raw_event.as_dict() )
		self.__process_players(raw_dict, event)
		self.__process_cards(raw_dict, event)
		return event
		
	def __process_players(self, raw_dict: dict, event: GameplayStatusUpdateEvent) -> None:
		event.game_state = { mtgoplayer['Name']: GameplayStatusUpdateEvent.PlayerGameplayInformation(
			name           = mtgoplayer['Name'],
			mtgo_player_id = mtgoplayer['Id'],
			library_size   = mtgoplayer['LibraryCount'],
			hand_size      = mtgoplayer['HandCount'],
			life_total     = mtgoplayer['Life'],
		) for mtgoplayer in raw_dict['Players'] }
	
	def __process_cards(self, raw_dict: dict, event: GameplayStatusUpdateEvent) -> None:
		for mtgocard in raw_dict['Cards']:
			controller = self.__find_player_name_by_mtgo_id(raw_dict, mtgocard['Controller'])
			cat_id = mtgocard['CatalogID']
			zone = mtgocard['Zone'].lower()
			try:
				event.game_state[controller].controlled_cards[zone].append(cat_id)
			except KeyError:
				event.game_state[controller].controlled_cards['other'].append(cat_id)
	
	def __find_player_name_by_mtgo_id(self, raw_dict: dict, id: int) -> str:
		for mtgoplayer in raw_dict['Players']:
			if mtgoplayer['Id'] == id:
				return mtgoplayer['Name']
		raise KeyError(f'Player with ID ${id} not found')

