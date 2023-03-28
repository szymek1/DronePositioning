import os
import json
from dataclasses import dataclass
from typing import Dict


class InfoReader:
	"""Internal utility for loading data from JSON"""

	@staticmethod
	def get_data() -> Dict[int, str]:
		"""Returns dictionary with key connection info"""
		relative_path = "connection_data.json"
		data_path = os.path.join(os.path.dirname(__file__), relative_path)

		with open(data_path, "r") as data:
			connection_data = json.load(data)

		return connection_data


@dataclass
class ServerInfo:
	"""Important informations regarding server connection"""

	connection_data = InfoReader().get_data()
	
	# Connection Information
	localHostIP: str = connection_data["localHostIP"]
	remoteIP: str = connection_data["remoteIP"]
	port: int = connection_data["port"]
	dataBufferSize: int = connection_data["dataBufferSize"]
