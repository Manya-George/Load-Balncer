                                              

This project implements a customizable load balancer using  that  distributes asyncronous client requests evenly among multiple server containers using **consistent hashing** .
The  servers have  multiple replicas.The containerization is done with docker and deployed within a docker network.


Functions of a load balancer:

* Maintains a fixed number of server replicas (containers)
* Monitors server health via heartbeats and respawns failed servers automatically
* Allows dynamic scaling (adding/removing servers)
* Routes client requests based on consistent hashing to ensure minimal disruption on scaling or failure



---

## Technologies & Environment

* **Operating System:** Ubuntu 20.04 LTS or above
* **Docker:** Version 20.10.23 or above
* **Docker Compose:** v2.15.1
* **Programming Language:** Python 3.8+
* **Libraries:** Flask (for HTTP servers), Requests (for testing)
* **Version Control:** Git & GitHub

---

## Installation & Setup
Installation
1. **Install Docker Engine**
 ```bash

sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg lsb-release
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io
 ```
Verify Docker:
 ```bash

sudo docker --version
 ```

2. **Install Docker Compose**
 ```bash

sudo curl -SL https://github.com/docker/compose/releases/download/v2.15.1/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
 ```
Verify Docker Compose:
 ```bash

docker-compose --version
 ```

3. **Install Git (if not installed)**
 ```bash

sudo apt-get install -y git
 ```

4. **Clone the repository:**

   ```bash
   git clone https://github.com/Manya-George/Load-Balncer.git
   cd Load-Balncer
   ```

5. **Build and run containers using Makefile**
 ```bash

make build       # Builds all Docker images (server + load balancer)
make start       # Starts the full system (load balancer + 3 server replicas)
make stop        # Stops and removes all containers
 
 ```




---

## Implementation Details

### Task 1: Server

* A minimal Flask-based HTTP server listening on port `5000`.
* Endpoints:

  * `/home` (GET): Returns `"Hello from Server: [ID]"`. Server ID is injected via Docker env variable.
  * `/heartbeat` (GET): Returns status 200 with empty response to indicate server health.
* Dockerized with environment variables and network settings.

---

### Task 2: Consistent Hashing




### Requirements:

* Number of physical server containers: **N = 3**
* Number of slots in the hash map: **512**
* Number of virtual servers per physical server: **K = 9** (since $\log_2 512 = 9$)
* Hash functions:

  * Request hash: $H(i) = (i + 2i^2 + 17) \mod 512$
  * Virtual server hash: $\Phi(i, j) = (i^2 + j + 2j^2 + 25) \mod 512$
* Collision resolution by **linear probing**


---

### Task 3: Load Balancer

* Maintains `N=3` server containers by default.
* HTTP API Endpoints:

  * `/rep` (GET): Lists current server replicas.
  * `/add` (POST): Adds new server replicas.
  * `/rm` (DELETE): Removes server replicas.
  * `/<path>` (GET): Routes request to appropriate server using consistent hashing.
* Monitors server health using `/heartbeat`. Spawns new containers if failures detected.
* Dockerized with privileged container setup for managing other containers.

---

### Task 4: Analysis & Testing

* Automated Python test scripts in `/tests` folder simulate 10,000 async requests.
* Collects and charts distribution of requests among servers.
* Tests dynamic scaling (`/add` and `/rm` endpoints).
* Measures load balancer’s responsiveness to server failures.
* Reports results in console and generates charts using matplotlib.

---

## Usage

1. **Access Load Balancer API:**

   By default, the load balancer listens on `http://localhost:5000`.

2. **Check replicas:**

   ```bash
   curl http://localhost:5000/rep
   ```

3. **Add servers:**

   ```bash
   curl -X POST http://localhost:5000/add -H "Content-Type: application/json" \
        -d '{"n":2,"hostnames":["S4","S5"]}'
   ```

4. **Remove servers:**

   ```bash
   curl -X DELETE http://localhost:5000/rm -H "Content-Type: application/json" \
        -d '{"n":1,"hostnames":["S4"]}'
   ```

5. **Send client requests:**

   ```bash
   curl http://localhost:5000/home
   ```

---

## Running Tests

Run automated test suite to validate system and analyze load balancing:

```bash
python3 tests/test_load_balancer.py
```

The script runs multiple async requests, outputs distribution stats, and generates charts saved under `/tests/results/`.

---

## Performance & Analysis

### Experiment A-1: Load Distribution with N=3

* Sent 10,000 requests asynchronously.
* Requests distributed nearly evenly among servers.
* Bar chart shows slight variance due to hashing randomness.

### Experiment A-2: Scaling from N=2 to N=6

* At each increment, sent 10,000 requests.
* Load balanced with high uniformity across servers.
* Line chart confirms scalability and smooth load distribution.

### Experiment A-3: Failure Recovery

* Simulated server failure by stopping container.
* Load balancer detected failure via heartbeat.
* Spawned new server container promptly to maintain `N` replicas.

### Experiment A-4: Hash Function Modification

* Changed hash functions `H(i)` and `Φ(i,j)`.
* Observed slight degradation in load uniformity.
* Consistent hashing properties verified.



---
