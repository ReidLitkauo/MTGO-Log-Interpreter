import queue
import threading

from EventType import EventType

class EventCommunicator:
	
	__queues: dict[EventType, list[queue.SimpleQueue]]
	__queues_lock: threading.Lock
	
	def __init__(self):
		self.__queues = { event_type: [] for event_type in EventType }
		self.__queues_lock = threading.Lock()
	
	def subscribe(self, event_type: EventType) -> queue.SimpleQueue:
		new_queue = queue.SimpleQueue()
		with self.__queues_lock:
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

	def put(self, event_type: EventType, item) -> None:
		with self.__queues_lock:
			for event_queue in self.__queues[event_type]:
				event_queue.put(item)

