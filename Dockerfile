FROM python:3.8-slim
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y docker.io sudo
RUN pip install flask requests
EXPOSE 5000
CMD ["python", "load_balancer.py"]
