import asyncio
import dataclasses
import json
import queue
import websockets.asyncio.server

from ConfigKey import ConfigKey
from WorkerThread import WorkerThread

class WebsocketServerThread(WorkerThread):
	
	__queue: queue.SimpleQueue
	__connections: set
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__queue = self._comms.subscribe()
		self.__connections = set()
	
	def run(self) -> None:
		if self._config[ConfigKey.PORT]:
			asyncio.run(self.__run_server())
	
	async def __run_server(self) -> None:
		async with websockets.asyncio.server.serve( self.__ws_handler, '', self._config[ConfigKey.PORT] ):
			while True:
				try:
					event = self.__queue.get_nowait()
					event_dict = event.as_dict()
					event_dict['event_type'] = type(event).__name__
					websockets.asyncio.server.broadcast(self.__connections, json.dumps(event_dict))
					self._logger.info(event)
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

