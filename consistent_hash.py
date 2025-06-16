import bisect

class ConsistentHash:
	def __init__(self, num_servers=3, num_slots=512, virtual_replicas=9):
		self.num_servers = num_servers
		self.num_slots = num_slots
		self.virtual_replicas = virtual_replicas
		self.ring = dict()
		self.sorted_keys = []
		self.server_map = {}

	def _hash_request(self, request_id: int) -> int:
		return (request_id + 2 * (request_id ** 2) + 17) % self.num_slots

	def _hash_virtual(self, server_id: int, replica_id: int) -> int:
		return (server_id ** 2 + replica_id + 2 * (replica_id ** 2) + 25) % self.num_slots

	def add_server(self, server_id: int):
		for replica_id in range(self.virtual_replicas):
			slot = self._hash_virtual(server_id, replica_id)
			original_slot = slot
			while slot in self.ring:
				slot = (slot + 1) % self.num_slots
				if slot == original_slot:
					raise Exception("Hash ring full!")
			self.ring[slot] = f"Server {server_id}"
			self.sorted_keys.append(slot)
			self.server_map.setdefault(f"Server {server_id}", []).append(slot)
		self.sorted_keys.sort()

	def remove_server(self, server_id: int):
		server_name = f"Server {server_id}"
		if server_name in self.server_map:
			for slot in self.server_map[server_name]:
				del self.ring[slot]
				self.sorted_keys.remove(slot)
			del self.server_map[server_name]

	def get_server(self, request_id: int) -> str:
		if not self.sorted_keys:
			return None
		slot = self._hash_request(request_id)
		idx = bisect.bisect(self.sorted_keys, slot) % len(self.sorted_keys)
		return self.ring[self.sorted_keys[idx]]

if __name__ == "__main__":
	ch = ConsistentHash(num_servers=3)
	for i in range (1, 4):
		ch.add_server(i)

	print("Request 132574 handled by:", ch.get_server(132574))
