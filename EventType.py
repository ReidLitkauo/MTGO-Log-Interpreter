import enum

class EventType(enum.Enum):
	
	ALL_EVENTS = 'all_events'
	
	UNKNOWN = 'unknown'
	RAW_LINE = 'raw_line'
	
	GAMEPLAY_STATUS_UPDATE = 'gameplay_status_update'

