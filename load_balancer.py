from flask import Flask, request,jsonify
import subprocess
import random
import os 
import json
from consistent_hash import ConsistentHash

app = Flask(__name__)

NUM_SLOTS = 512
VIRTUAL_REPLICAS = 9
hash_ring = ConsistentHash(num_slots=NUM_SLOTS, virtual_replicas=VIRTUAL_REPLICAS)
active_servers = {}

SERVER_PORT = 5000
DOCKER_IMAGE = "server_image"
DOCKER_NETWORK = "net1"

def generate_hostname():
	return f"S{random.randint(1000, 9999)}"

def spawn_server(server_id, hostname=None):
	ifnot hostname:
		hostname = generate_hostname()
	cmd = [
		"docker", "run", "d",
		"--name", hostname,
		"--network", DOCKER_NETWORK,
		"--network-alias", hostname,
		"-e", f"SERVER_ID={server_id}",
		DOCKER_IMAGE
	]
	result = subprocess.run(cmd, capture_output=True, text=True)
	if result.returncode == 0:
		active_servers[hostname] = server_id
		hash_ring.add_server(server_id)
		return True
	else:
		print(f"Error spawning {hostname}: {result.stderr}")
		return False

def remove_server(hostname):
	server_id = active_servers.get(hostname)
	if server_id is None:
		return False
	hash_ring.remove_server(server_id)
	subprocess.run(["docker", "stop", hostname])
	subprocess.run(["docker", "rm", hostname])
	del active_servers[hostname]
	return True

@app.route("/rep", methods=["GET"])
def get_replicas():
	return jsonify({
		"message": {
			"N": len(active_servers),
			"replicas": list(active_servers.keys())
		},
		"status": "successful"
	}), 200

@app.route("/add", methods=["POST"])
def add_servers():
	data = request.get_json()
	n = data.get("n", 0)
	hostnames = data.get("hostnames", [])
	if len(hostnames) > n:
		return jsonify({
			"message": "<Error> Length of hostname list is more than newly added instances"
			"status": "failure"
		}), 400
	for i in range(n):
		sid = len(active_servers) + 1
		name = hostnames[i] if i < len(hostnames) else None
		spawn_server(sid, name)
	return get_replicas

@app.route("/rm", methods=["DELETE"])
def remove_servers():
	data = request.get_json()
	n = data.get("n", 0)
	hostnames = data.get("hostnames", [])
	if len(hostnames) > n:
		return jsonify({
			"message": "<Error> Length of hostname list is more than removable instances"
			"status": "failure"
		}), 400
	removed = 0
	for name in hostnames:
		if name in active_servers:
			remove_server(name)
			removed += 1
	for name in list(active_servers.keys()):
		if removed >= n:
			break
		remove_server(name)
		removed += 1
	return get_replicas()

@app.route("/<path:endpoint>", methods=["GET"])
def forward_request(endpoint):
	rid = random.randint(100000, 999999)
	target = hash_ring.get_server(rid)
	if not target:
		return jsonify({"message": "No servers available", "status": "failure"}), 503

	for name, sid in active_servers.items():
		if f"Server {sid}" == target:
			url = f"http://{name}:{SERVER_PORT}/{endpoint}"
			try:
				import requests
				res = requests.get(url)
				return jsonify(res.json()), res.status_code
			except Exception as e:
				return jsonify({"message": str(e), "status": "failure"}), 500

	return jsonify({
		"message": f"<Error> '/{endpoint}' endpoint does not exist in server replicas"
		"status": "failure"
	}), 400

if __name__ == "__main__":
	for i in range(1, 4):
		spawn_server(i, f"Server{i}")
	app.run(host="0.0.0.0", port=5000)
