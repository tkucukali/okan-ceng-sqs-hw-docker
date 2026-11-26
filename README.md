<!--
# Simple Fact API
Build image: `docker build -t fact-app:v1 .`
Run container: `docker run -d --name my-container -p 8080:8080 -e AUTHOR_NAME="Tolgahan" fact-app:v1`
Test health: `curl http://localhost:8080/health`
Test fact endpoint: `curl http://localhost:8080/fact`
-->

<!--
# HW-2: Docker Compose Fact API

`cp .env.example .env`
`docker compose up -d --build`

Test health: `curl http://localhost:8080/health`
Test fact: `curl http://localhost:8080/fact`
Test database state: `curl http://localhost:8080/stats`
-->

# HW-3: Running fact-app on Kubernetes

Deploying the Flask + PostgreSQL app (`gawainn/fact-app:1.0.0`) from HW-2 onto a Kubernetes cluster (tested on Killercoda).

## How to Apply

First, check for syntax issues with a dry run:
```bash
kubectl apply --dry-run=client -f .
```

Apply the manifests in order (or all together with `kubectl apply -f .`):
```bash
kubectl apply -f secret.yaml
kubectl apply -f configmap.yaml
kubectl apply -f postgres.yaml
kubectl apply -f app.yaml
```

## How to Check

Check pod and service status:
```bash
kubectl get pods
kubectl get svc
kubectl describe pod <fact-app-pod-name>
```

Test the endpoints through the NodePort (`30080`):
```bash
curl http://localhost:30080/health
curl http://localhost:30080/fact
curl http://localhost:30080/stats
```

## What I Saw

- After applying everything, 2 `fact-app` pods and 1 `postgres` pod spun up.
- At first, the `fact-app` pods stayed at `0/1 Ready` for a few seconds until the `initialDelaySeconds` (5s) passed and `/health` started returning `200 OK`, switching them to `1/1 Ready`.
- One interesting thing I noticed during testing: on the very first run, `fact-app` started slightly faster than PostgreSQL, so `init_db()` couldn't connect at startup and `/stats` fell back to `"memory (no DB)"`. After PostgreSQL finished initializing, running `kubectl rollout restart deployment/fact-app-deployment` fixed it, and `/stats` properly tracked requests in PostgreSQL (`"state_storage": "postgresql"`).
- Checking `kubectl describe pod` showed that the env vars from `fact-app-config` and `fact-app-secret` were injected as expected, along with the CPU/memory requests and limits.

---

## Questions

**1. What is the difference between a readiness and a liveness probe?**
A readiness probe checks if the app is ready to handle traffic. If it fails, Kubernetes removes the pod from the Service's endpoints so users don't get routed to it, without restarting the container. A liveness probe checks if the app is still alive or stuck/deadlocked—if it fails, Kubernetes kills and restarts the container.

**2. Why is a Secret not the same as encryption?**
Kubernetes Secrets are just Base64-encoded by default, not encrypted. Anyone who can read the Secret manifest or run `kubectl get secret -o yaml` can easily decode it back to plain text. Actual encryption requires enabling encryption at rest in etcd and locking down access with RBAC.

**3. What happens when a container crosses its memory limit?**
The Linux kernel's OOM (Out-Of-Memory) killer steps in and terminates the container process. Kubernetes marks the pod status as `OOMKilled` (exit code 137) and restarts it based on the restart policy, which usually puts it into a `CrashLoopBackOff` if the memory spike keeps happening.

---

## Bonus: Removing the Readiness Endpoint

If the `/health` endpoint is removed (or changed to a path that returns `404`), the readiness probe fails after 3 consecutive attempts (`failureThreshold`). The pod stays in the `Running` state and doesn't immediately restart, but its status changes from `1/1` to `0/1` Ready. Kubernetes pulls its IP out of `fact-app-service`, so traffic stops going to that pod until it passes the health check again (or if all pods fail, requests to the service fail).