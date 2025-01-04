import asyncio
import queue
import websockets.asyncio.server

from ConfigKey import ConfigKey
from EventType import EventType
from WorkerThread import WorkerThread

class WebsocketServerThread(WorkerThread):
	
	__queue: queue.SimpleQueue
	__connections: set
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__queue = self._comms.subscribe(EventType.ALL_EVENTS)
		self.__connections = set()
	
	def run(self) -> None:
		if self._config[ConfigKey.PORT]:
			asyncio.run(self.__run_server())
	
	async def __run_server(self) -> None:
		async with websockets.asyncio.server.serve( self.__ws_handler, '', self._config[ConfigKey.PORT] ):
			while True:
				try:
					line = self.__queue.get_nowait()
					websockets.asyncio.server.broadcast(self.__connections, line.json())
					self._logger.info(line)
				except queue.Empty:
					pass
				finally:
					await asyncio.sleep(0)
	
	async def __ws_handler(self, ws) -> None:
		self.__connections.add(ws)
		try:
			await ws.wait_closed()
		finally:
			self.__connections.remove(ws)

