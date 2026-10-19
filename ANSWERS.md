# ANSWERS

**1. Explain the order of the instructions in your Dockerfile. What would happen to build time if you changed the order of two of them?**
I copied `requirements.txt` and installed the dependencies before copying the actual application code. This utilizes Docker's layer cache effectively. If I copied the source code first, every minor code edit would invalidate the cache for the installation step. That would force Docker to redownload and reinstall all dependencies on every build, significantly increasing the build time.

**2. What happens to data written inside a container when the container is removed? How would you keep the data, and where should an application keep important state?**
Any data written directly inside a container's filesystem is completely lost when that container is removed. To keep the data persistent, we must use Docker Volumes or bind mounts to store it outside the container on the host machine. A well-designed application should ideally be stateless and keep its important state in an external database or a managed storage service.

**3. Why is the `latest` tag a risk for reproducibility? What did you use instead?**
The `latest` tag is risky because it automatically updates to newer versions over time. A Dockerfile that builds perfectly today might suddenly fail tomorrow if the underlying `latest` image introduces breaking changes. To ensure reproducibility, I used a pinned version (`python:3.11-slim`) so the build environment remains exactly the same every time.

*Note on AI assistants:* I used an AI assistant to help brainstorm a unique, simple app idea and structure the files properly according to the homework constraints. The answers and code reflect my own understanding of the lab concepts.