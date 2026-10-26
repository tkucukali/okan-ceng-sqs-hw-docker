<!--
# Simple Fact API
Build image: `docker build -t fact-app:v1 .`
Run container: `docker run -d --name my-container -p 8080:8080 -e AUTHOR_NAME="Tolgahan" fact-app:v1`
Test health: `curl http://localhost:8080/health`
Test fact endpoint: `curl http://localhost:8080/fact`
-->

# HW-2: Docker Compose Fact API

`cp .env.example .env`
`docker compose up -d --build`

Test health: `curl http://localhost:8080/health`
Test fact: `curl http://localhost:8080/fact`
Test database state: `curl http://localhost:8080/stats`