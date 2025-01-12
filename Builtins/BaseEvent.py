import dataclasses
import json

@dataclasses.dataclass()
class BaseEvent:
	
	raw_contents: str
	line_number: int

	def as_dict(self):
		return dataclasses.asdict(self)

