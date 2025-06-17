
---

# Kubernetes Hackathon

This project demonstrates a containerized microservice architecture deployed on a local Kubernetes cluster (Minikube). The entire system runs inside a VirtualBox VM using Ubuntu. This guide will walk you through setting up the environment, deploying the application, and exploring different solutions.

## Requirements

### Host Machine:

* **VirtualBox**: Ensure it's installed on your host machine.
*  **UBUNTU-24.04.2**: This is the operating system of the virtual machine.
* **Internet Connection**: Required for installing dependencies inside the Ubuntu VM.

### Inside Ubuntu VM (20.04 or later):

* Docker
* Minikube
* Kubectl
* Git


## Setup Instructions

### 1. Update System & Install Dependencies

Run the following commands to update your system:

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Install Docker

Install Docker and add your user to the Docker group:

```bash
sudo apt install -y docker.io
sudo usermod -aG docker $USER
newgrp docker
```

### 3. Install Minikube

Download and install Minikube:

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

### 4. Install Kubectl

Download and install kubectl:

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

### 5. Start Minikube

Start Minikube with the Docker driver:

```bash
minikube start --driver=docker
```

> **Note**: If using VirtualBox driver, replace `--driver=docker` with `--driver=virtualbox`.

### 6. Clone the Project Repository

Clone the repository and navigate into the project directory:

```bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo
```
To clone our repo
    - Open a terminal (PowerShell on Windows; any shell on Linux/macOS) 
    - Run: `git clone https://github.com/kubernetes_hackathon.git`
  

### 7. Deploy to Kubernetes

Deploy the application using the Kubernetes configuration files:

```bash
kubectl apply -f k8s/
```

### 8. Access the Application

To access the application, you can retrieve the service URL as follows:

```bash
minikube service <service-name> --url
```

## Solutions Overview

### Solution 1: Basic Deployment

Widgetario, a company that sells gadgets, runs its public web app on Kubernetes. All components are packaged into container images and published on Docker Hub. In this solution, we start with a simple setup using one replica for each component. We were able to ping `127.0.0.1` or browse port `8080` on the cluster.

To deploy after Cloning 
```bash

kubectl apply -f kubernetes_hackathon/solution-part-1/products-db -f kubernetes_hackathon/solution-part-1/products-api  -f kubernetes_hackathon/solution-part-1/stock-api -f kubernetes_hackathon/solution-part-1/web
```
### Solution 2: Secure Configuration

The `widgetario/products-db:21.03` image exposes the database password through environment variables. This solution addresses the security issue by:

* Storing passwords securely in environment variables.
* Enabling the front-end team to experiment with a new dark mode via a config setting.

Key tasks:

* **Products DB**: Secure the `POSTGRES_PASSWORD` environment variable.
* **Stock API**: Use a Go app that connects to the PostgreSQL database with a connection string.
* **Products API**: Update the Spring Boot application’s `application.properties` with the new password.
* **Web App**: A .NET Core app that uses `/app/secrets/api.json` for overriding settings, including API URLs and theme configurations.

Environment variables:

* `Widgetario__Theme=dark` (for dark mode)

  To deploy after cloning this repo

```
kubectl apply -f kubernetes_hackathon/solution-part-2/products-db -f kubernetes_hackathon/solution-part-2/products-api  -f kubernetes_hackathon/solution-part-2/stock-api -f kubernetes_hackathon/solution-part-2/web
```


### Solution 3: PostgreSQL Replication & Caching

Enabled local caching for the Stock API (`/cache` directory) to survive Pod restarts. We also switched to a replicated PostgreSQL setup using `widgetario/products-db:postgres-replicated`.

* **PostgreSQL Replication**: Configure the Products API to connect to the primary DB and the Stock API to the secondary.
* **Deployment Update**: Clean up old persistent volumes and services.

Commands:

```bash
kubectl delete deploy products-db
kubectl delete svc products-db
kubectl delete pvc -l app=products-db

kubectl apply -f kubernetes_hackathon/solution-part-3/products-db \
              -f kubernetes_hackathon/solution-part-3/products-api \
              -f kubernetes_hackathon/solution-part-3/stock-api \
              -f kubernetes_hackathon/solution-part-3/web

kubectl rollout restart deploy/products-api deploy/stock-api
```

### Solution 4: Ingress Configuration

Configured Ingress resources for clean domain-based routing:

* **Web App**: `http://widgetario.local`
* **API**: `http://api.widgetario.local`

Commands:

```bash
./scripts/add-to-hosts.sh widgetario.local 127.0.0.1
./scripts/add-to-hosts.sh api.widgetario.local 127.0.0.1
```

This ensures that the web app and APIs are accessible through friendly domain names.

To deploy after cloning this repo
```
kubectl apply -f kubernetes_hackathon/solution-part-44/ingress-controller -f kubernetes_hackathon/solution-part-44/products-db -f kubernetes_hackathon/solution-part-44/products-api  -f kubernetes_hackathon/solution-part-44/stock-api -f kubernetes_hackathon/solution-part-44/web
```



## Part 5 - Productionizing
Deployment:

```
kubectl apply -f kubernetes_hackathon/solution-part-5/ingress-controller -f kubernetes_hackathon/solution-part-5/products-db -f kubernetes_hackathon/solution-part-5/products-api  -f kubernetes_hackathon/solution-part-5/stock-api -f kubernetes_hackathon/solution-part-5/web
```

Everything works in the same way:

> Browse to http://widgetario.local to see the app

> See the API response at http://api.widgetario.local/products



The StatefulSet rollout takes a few minutes, and the app may not be responsive until both Pods are up. **And** there are CPU resources in the specs, so if your cluster doesn't have enough capacity you may see Pods stuck in the _Pending_ status, so you'll need to adjust the values.


## Part 6 - Observability


All the API and web servers publish metrics, so we don't need to change any code. To prove monitoring is usable you'll need to:

- run a monitoring stack with Prometheus and Grafana
- configure the Pod specs so Prometheus collects metrics - the database doesn't expose any metric but the other components do
- the app devs have said the Products API using a custom metrics path `/actuator/prometheus`, and the web app might be running with a custom port
- deploy the changes and check all the components are having metrics stored in Prometheus
- open Grafana and load the dashboard from `kubernetes_hackathon/files/grafana-dashboard.json`; use the app and confirm all the visualizations show data.

And then you'll also need to set up centralized logging:

- run the EFK stack to collect and store logs in the app namespace
- the dev team say the web app writes logs to a file, so you'll need to add a sidecar container to print logs from `/logs/app.log` in the app container
- open Kibana and load the dashboard from `kubernetes_hackathon/files/kibana-dashboard.ndjson`; check the visualizations to see every component is writing logs


```
kubectl apply -f kubernetes_hackathon/solution-part-6/monitoring -f kubernetes_hackathon/solution-part-6/logging -f kubernetes_hackathon/solution-part-6/ingress-controller -f kubernetes_hackathon/solution-part-6/widgetario
```


* Grafana on http://localhost:30003 or http://localhost:3000

* Kibana on http://localhost:30005 or http://localhost:5601



## Part 7 - CI/CD

The last thing we need is a full CI/CD pipeline to build from source code and deploy to a test environment.

We've settled on Helm for packaging, so the first task is to work up the YAML specs into a Helm chart. The chart should support:
- multiple release in the same namespace
- variables for image tags, replica counts, and whether resource limits should be included
- app configuration per release, including the database password and the web theme

We'll be using standard deployments for the ingress controller, monitoring and logging stacks so you don't need to build Helm charts for those

Then we need to put together the continuous integration pipeline:

- we'll use Jenkins, BuildKit and Gogs to power the pipeline
- you'll need to create a registry Secret to push to Docker Hub (or your own registry)
- the source code is all in the `/hackathon/project` folder

So then we're ready to add continuous deployment:

- extend the Jenkinsfile to add the deployment steps
- use the Helm chart for deploying to a test namespace
- deploy the chart with the values file 
- the deployment needs to use the latest images which were pushed in the build.

Now when you trigger the build from Jenkins you should see a new version of the app deployed in your test namespace, running all the latest image versions.


```
# On Windows (run as Admin)
./scripts/add-to-hosts.ps1 widgetario.uat 127.0.0.1
./scripts/add-to-hosts.ps1 api.widgetario.uat 127.0.0.1

# OR on Linux/macOS
./scripts/add-to-hosts.sh widgetario.uat 127.0.0.1
./scripts/add-to-hosts.sh api.widgetario.uat 127.0.0.1
```

Try the Products API:

```
curl -k https://api.widgetario.uat/products
```

> Browse to http://widgetario.uat; you'll see a new _Buy_ button from the latest image update

_Deploy the build infrastructure:_

```
kubectl apply -f kubernetes_hackathon/solution-part-7/infrastructure
```

_When it's all running, push your local code to Gogs:_

```
git remote add hackathon http://localhost:30031/kiamol/kiamol.git


_Create a configmap with the details for the image name - be sure to use a registry and domain you have push access for:_

```
kubectl -n infra create configmap build-config --from-literal=REGISTRY=docker.io  --from-literal=REPOSITORY=$REGISTRY_USER 
```

_Restart Jenkins to load the latest config:_

```
kubectl rollout restart deploy/jenkins -n infra
```

> Browse to Jenkins http://localhost:30007, sign in with the `kiamol` username and password

Open the Widgetario job in Jenkins, enable and build it. Confirm that your images build and are pushed with the correct tags.

_Add the Helm deploy stage to Jenkins:_

You can edit the Jenkisfile:

- open http://localhost:30880/job/widgetario/configure
- scroll down to _Script Path_
- change the path to `hackathon/solution-part-7/Jenkinsfile`

Build again and confirm the latest images are deployed in the new namespace.

_Add smoke test domain to hosts file:_

```
# On Windows (run as Admin)
./scripts/add-to-hosts.ps1 widgetario.smoke 127.0.0.1
./scripts/add-to-hosts.ps1 api.widgetario.smoke 127.0.0.1

# OR on Linux/macOS
./scripts/add-to-hosts.sh widgetario.smoke 127.0.0.1
./scripts/add-to-hosts.sh api.widgetario.smoke 127.0.0.1
```

Check the Products API:

```
curl -k https://api.widgetario.smoke/products
```

> And test the app at http://widgetario.smoke


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


