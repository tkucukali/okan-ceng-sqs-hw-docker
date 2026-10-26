# ANSWERS
### HW-1
**1. Explain the order of the instructions in your Dockerfile. What would happen to build time if you changed the order of two of them?**
I copied `requirements.txt` and installed the dependencies before copying the actual application code. This utilizes Docker's layer cache effectively. If I copied the source code first, every minor code edit would invalidate the cache for the installation step. That would force Docker to redownload and reinstall all dependencies on every build, significantly increasing the build time.

**2. What happens to data written inside a container when the container is removed? How would you keep the data, and where should an application keep important state?**
Any data written directly inside a container's filesystem is completely lost when that container is removed. To keep the data persistent, we must use Docker Volumes or bind mounts to store it outside the container on the host machine. A well-designed application should ideally be stateless and keep its important state in an external database or a managed storage service.

**3. Why is the `latest` tag a risk for reproducibility? What did you use instead?**
The `latest` tag is risky because it automatically updates to newer versions over time. A Dockerfile that builds perfectly today might suddenly fail tomorrow if the underlying `latest` image introduces breaking changes. To ensure reproducibility, I used a pinned version (`python:3.11-slim`) so the build environment remains exactly the same every time.

### HW-2
**1. Your app calls the second service by name. How does that work, and why does the same name not work between two containers on the default docker run network?**
Docker Compose automatically creates a custom bridge network and provides an embedded DNS server for the services it manages. When the `app` service tries to connect to the `db`, this DNS automatically resolves the name "db" to the correct container IP address. However, the default bridge network used by standard `docker run` lacks this embedded DNS resolution. Therefore, containers on the default network cannot discover each other by name; they must rely on explicit IP addresses or legacy features like the `--link` flag.

**2. Which of your services is stateless and which is not? Show the evidence: what did you do, and what happened to your data?**
My Flask application (`app`) is completely stateless, as it relies entirely on the database for storage and does not keep data on its own filesystem. The database service (`db`) is stateful. To prove this, I sent several requests to the `/fact` endpoint to increment the counter, then ran `docker compose rm -sf app` and `docker compose down`. After starting the system again with `docker compose up -d`, I verified that the counter maintained its value because the state was preserved in the `db_data` volume. Finally, when I ran `docker compose down -v`, the volume was destroyed, and the counter was completely lost, proving the state was tied to the volume.

**3. Where should a database password come from, and why is it a problem to commit it to Git, even in a private repository?**
Database passwords should never be hardcoded in the codebase or the `compose.yaml` file; they must be provided through environment variables, typically sourced from a `.env` file that is ignored by Git (`.gitignore`). Committing a secret to Git, even in a private repository, is a major security risk because anyone with read access to the repo can view it. Furthermore, because Git tracks the entire history of changes, even if you delete the password in a subsequent commit, it remains permanently exposed and easily accessible in the commit history.