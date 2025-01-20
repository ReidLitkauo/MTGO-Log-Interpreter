import queue
import threading

from .Builtins.BaseEvent import BaseEvent

class EventCommunicator:
	
	__queues: dict[ type[BaseEvent] | None, list[queue.SimpleQueue] ]
	__queues_lock: threading.Lock
	
	def __init__(self):
		self.__queues = { None: [] }
		self.__queues_lock = threading.Lock()
	
	def subscribe(self, event_type: type[BaseEvent] | None = None) -> queue.SimpleQueue:
		new_queue = queue.SimpleQueue()
		with self.__queues_lock:
			if self.__queues.get(event_type) is None:
				self.__queues[event_type] = []
			self.__queues[event_type].append(new_queue)
		return new_queue

	def unsubscribe(self, old_queue: queue.SimpleQueue) -> bool:
		with self.__queues_lock:
			for event_type, queues in self.__queues:
				try:
					queues.remove(old_queue)
					return True
				except ValueError:
					pass
		return False

	def put(self, event: BaseEvent) -> None:
		with self.__queues_lock:
			queues_for_this_event_type = self.__queues.get(type(event), [])
			queues_for_all_event_types = self.__queues.get(None, [])
			for event_queue in queues_for_this_event_type + queues_for_all_event_types:
				event_queue.put(event)

