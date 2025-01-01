import abc

from EventType import EventType
from WorkerThread import WorkerThread

class LogLineProcessorThread(WorkerThread, abc.ABC):
	
	def __init__(self, event_type: EventType, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__queue = self._comms.subscribe(event_type)

	@abc.abstractmethod
	def _can_process(self, message: str) -> bool:
		raise NotImplementedError
	
	@abc.abstractmethod
	def _process_message(self, message: str) -> None:
		raise NotImplementedError

	def run(self) -> None:
		while True:
			message = self.__queue.get()
			if self._can_process(message):
				self._process_message(message)

