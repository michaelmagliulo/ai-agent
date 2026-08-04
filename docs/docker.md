Great. And yes, this is exactly the right time to introduce Docker Compose.
`docker compose` is **not** a Makefile.

Think of it this way:

* **Docker** = the engine.
* **Docker Compose** = a configuration file that describes one or more containers.
* **Makefile** = just a shortcut menu for commands.

For example, your Makefile might say:

```text
run:
    docker compose up
```

The Makefile isn't replacing Compose—it just saves you from typing the command.

Think of it like this:

```text
Makefile
    ↓
runs
    ↓
Docker Compose
    ↓
controls
    ↓
Docker
```

So in many projects you'll actually see both.

---

# Why Compose?

Right now, your `docker run` command has to remember:

* image name
* port mapping
* environment file
* restart policy
* container name
* etc.

Compose stores all of that in one file.

---

# Step 1 — Create `compose.yaml`

I recommend using `compose.yaml` instead of `docker-compose.yml`. Docker recognizes both, but `compose.yaml` is the newer preferred name.

Create it in the root of your project:

```text
ai-agent/
├── compose.yaml
├── Dockerfile
├── Makefile
├── requirements.txt
└── ...
```

Put this inside:

```yaml
services:
  ai-agent:
    build: .
    container_name: ai-agent

    env_file:
      - .env

    ports:
      - "8000:8000"

    restart: unless-stopped

    command: >
      uvicorn src.server:app
      --host 0.0.0.0
      --port 8000
```

---

# What each line means

```yaml
build: .
```

Build using the Dockerfile in this folder.

---

```yaml
container_name: ai-agent
```

Instead of Docker inventing a random name like:

```
happy_penguin
```

your container will always be called:

```
ai-agent
```

---

```yaml
env_file:
  - .env
```

Load your API key.

---

```yaml
ports:
  - "8000:8000"
```

Host port → container port.

---

```yaml
restart: unless-stopped
```

If Ubuntu reboots...

Docker starts your agent automatically.

This is huge.

---

```yaml
command:
```

Overrides the Dockerfile command and starts FastAPI.

---

# Step 2

Instead of

```
docker run ...
```

you now do

```bash
docker compose up
```

or, for a server,

```bash
docker compose up -d
```

The `-d` means **detached**, so it runs in the background.

---

# Step 3

To stop it:

```bash
docker compose down
```

---

# Step 4

To rebuild after code changes:

```bash
docker compose up -d --build
```

That one command:

* rebuilds the image
* recreates the container
* starts it
* leaves it running

---

## This is why I wanted Compose before CD

Your deployment script is about to become ridiculously simple.

GitHub will SSH into your server and run exactly one command:

```bash
cd ~/projects/ai-agent

git pull

docker compose up -d --build
```

That's essentially your entire deployment.

---

I think this is going to be one of those "aha" moments. Compose is where Docker starts feeling like a platform instead of a collection of commands. Once you see it working, you'll probably find yourself using it for almost every service you run on your homelab.
