import json
import re

from .BaseEvent import BaseEvent
from .BaseProcessor import BaseProcessor
from .GsMessageMessageEvent import GsMessageMessageEvent

class GsMessageMessageProcessor(BaseProcessor):
	
	__regex: re.Pattern = re.compile('\\d\\d:\\d\\d:\\d\\d \\[INF\\] \\(Game Management\\|Processing Registered Handler for GsMessageMessage in Match(?:Joined|Watching)EventUnderwayState\\) Processor: Match(?:Joined|Watching)EventUnderwayState Message: (\\{.*\\})')
	
	def process(self, raw_event: BaseEvent) -> GsMessageMessageEvent | None:
		raw_event = super().process(raw_event)
		if not raw_event:
			return None
		match = self.__regex.match(raw_event.raw_contents)
		if not match:
			return None
		return GsMessageMessageEvent( **raw_event.as_dict(), gs_message = self.__decode_gsmessagemessage(match.group(1)) )

	def __decode_gsmessagemessage(self, raw_json: str) -> str:
		return json.loads(raw_json)['MetaMessage']

