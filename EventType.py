import enum

class EventType(enum.Enum):
	
	UNKNOWN = 0
	RAW_LINE = 1
	
	GAMEPLAY_STATUS_UPDATE = 100
