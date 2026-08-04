No problem. Let's write this like it's part of your personal playbook.

# Starting your AI Agent Dev Container

## 1. Open a terminal

Go to your project:

```bash
cd ~/Documents/python/Ai_Agent/ai-agent
```

(Use whatever path your repository is actually in.)

Verify you're in the project:

```bash
pwd
ls
```

You should see:

```text
Dockerfile
README.md
requirements.txt
src
.devcontainer
...
```

---

## 2. Open VS Code

From the project directory:

```bash
code .
```

VS Code should open the project.

---

## 3. Reopen in the Dev Container

In VS Code press:

**⇧⌘P** (Shift + Command + P)

Type:

```text
Dev Containers: Reopen in Container
```

Select it.

VS Code will either:

* Build the container (first time or after changes), or
* Reconnect to the existing container.

Wait until the bottom-left corner changes to something like:

```text
Dev Container: ai-agent
```

---

## 4. Open the terminal

Inside VS Code:

```
Terminal
→ New Terminal
```

or press:

```
Ctrl + `
```

You are now inside the Linux container.

---

## 5. Verify you're inside

Run:

```bash
python --version
```

Then:

```bash
which python
```

Then:

```bash
pwd
```

Everything from here is happening **inside the Dev Container**, not on your Mac.

---

## 6. Check pytest

Run:

```bash
pytest --version
```

If it works, great.

If not:

```bash
pip install pytest
```

---

## Tip

I would put these instructions in a file like:

```text
docs/dev_container.md
```

Eventually you'll have your own cookbook for things you don't do every day.

---

### One thing I'd like to fix soon

I remember you mentioning that `code .` keeps opening an **"Untitled Workspace"** instead of just opening the folder. We never fully resolved that. Once we finish CI, I'd like to help you fix that annoyance because it'll make working with the Dev Container much smoother every day.


# Start Server
uvicorn src.server:app --host 0.0.0.0 --port 8000