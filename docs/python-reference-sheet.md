# Python Developer Cheat Sheet

## Virtual Environment

Create

```bash
python -m venv venv
```

Activate (Linux/macOS)

```bash
source venv/bin/activate
```

Deactivate

```bash
deactivate
```

---

## Install Packages

```bash
pip install requests
```

Upgrade a package

```bash
pip install --upgrade requests
```

Install from requirements

```bash
pip install -r requirements.txt
```

Freeze dependencies

```bash
pip freeze > requirements.txt
```

---

## Run Python

```bash
python main.py
```

Run a module

```bash
python -m src.main
```

---

## Formatting

```bash
black .
```

```bash
isort .
```

---

## Linting

```bash
ruff check .
```

Fix automatically

```bash
ruff check . --fix
```

---

## Testing

```bash
pytest
```

Verbose

```bash
pytest -v
```

Single file

```bash
pytest tests/test_main.py
```

---

## Git

Status

```bash
git status
```

Add

```bash
git add .
```

Commit

```bash
git commit -m "Message"
```

Push

```bash
git push
```

Pull

```bash
git pull
```

---

## Docker

Build

```bash
docker build -t ai-agent .
```

Run

```bash
docker run --rm ai-agent
```

List containers

```bash
docker ps
```

Stop container

```bash
docker stop <container>
```

---

## Make

```bash
make run
```

```bash
make test
```

```bash
make lint
```

---

## Useful Commands

Current directory

```bash
pwd
```

List files

```bash
ls -la
```

Find Git root

```bash
git rev-parse --show-toplevel
```

Git remote

```bash
git remote -v
```

Python version

```bash
python --version
```

Pip version

```bash
pip --version
```

Installed packages

```bash
pip list
```