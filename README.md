# Simple Fact API
Build image: `docker build -t fact-app:v1 .`
Run container: `docker run -d --name my-container -p 8080:8080 -e AUTHOR_NAME="Tolgahan" fact-app:v1`
Test health: `curl http://localhost:8080/health`
Test fact endpoint: `curl http://localhost:8080/fact`