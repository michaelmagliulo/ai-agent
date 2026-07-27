Yes. We’ll build a **VS Code Dev Container** that preserves your current workflow:

* Your `.py` files live in a normal Mac folder.
* You continue using `# %%` and **Run Cell**.
* Python, Jupyter, pip, and libraries run inside Linux.
* You can install new packages without rebuilding during normal work.
* A rebuild is only needed when you intentionally want to recreate the environment.

VS Code’s Dev Containers extension is designed to open a normal folder mounted into a container while using the container as the complete development environment. VS Code also supports `# %%` cells in ordinary `.py` files through its Python/Jupyter integration. ([Visual Studio Code][1])

# Part 1: Create the normal Mac folder

Open Terminal and run:

```shell
mkdir -p ~/Documents/python/python-dev
cd ~/Documents/python/python-dev
```

Confirm your location:

```shell
pwd
```

You should see something similar to:

```text
/Users/work/Documents/python/python-dev
```

Open the folder in Finder:

```shell
open .
```

This is where your actual work will live.

# Part 2: Open the folder in VS Code

From the same terminal:

```shell
code .
```

If the `code` command is unavailable:

1. Open VS Code.
2. Choose **File → Open Folder**.
3. Select:

```text
Documents/python/python-dev
```

# Part 3: Install the required VS Code extension

In VS Code:

1. Open Extensions using `Command+Shift+X`.
2. Search for:

```text
Dev Containers
```

3. Install the Microsoft extension named **Dev Containers**.

Also make sure these Microsoft extensions are installed:

```text
Python
Jupyter
```

The Python and Jupyter extensions provide the interactive `# %%` experience. The Dev Containers extension makes the container your development environment. ([Visual Studio Code][2])

# Part 4: Create the Dev Container configuration folder

Inside the VS Code Explorer, create a folder named:

```text
.devcontainer
```

Your project should now look like:

```text
python-dev/
└── .devcontainer/
```

Inside `.devcontainer`, create a file named:

```text
Dockerfile
```

Put this inside it:

```dockerfile
FROM python:3.13

WORKDIR /workspace

RUN python -m pip install --upgrade pip \
    && python -m pip install \
        ipykernel \
        jupyter \
        pandas \
        matplotlib \
        scikit-learn \
        fastapi \
        uvicorn
```

This defines the initial Linux Python environment.

# Part 5: Create `devcontainer.json`

Inside the same `.devcontainer` folder, create:

```text
devcontainer.json
```

Put this inside:

```json
{
    "name": "Python 3.13 Development",

    "build": {
        "dockerfile": "Dockerfile",
        "context": ".."
    },

    "workspaceFolder": "/workspace",

    "workspaceMount": "source=${localWorkspaceFolder},target=/workspace,type=bind",

    "forwardPorts": [
        8000,
        8888
    ],

    "customizations": {
        "vscode": {
            "extensions": [
                "ms-python.python",
                "ms-python.vscode-pylance",
                "ms-toolsai.jupyter"
            ],
            "settings": {
                "python.defaultInterpreterPath": "/usr/local/bin/python",
                "jupyter.askForKernelRestart": false
            }
        }
    }
}
```

Your folder should now look like:

```text
python-dev/
└── .devcontainer/
    ├── Dockerfile
    └── devcontainer.json
```

The important line is:

```json
"workspaceMount": "source=${localWorkspaceFolder},target=/workspace,type=bind"
```

That means:

```text
Mac folder                             Linux container
~/Documents/python/python-dev    →     /workspace
```

Your files stay on your Mac. `/workspace` is simply the container’s view of those same files.

# Part 6: Build and enter the container

In VS Code, press:

```text
Command+Shift+P
```

Search for:

```text
Dev Containers: Reopen in Container
```

Select it.

VS Code will now:

1. Read the Dockerfile.
2. Build the development image.
3. Create a container.
4. Mount your Mac folder at `/workspace`.
5. Install the Python and Jupyter extensions inside the container.
6. Reopen VS Code connected to Linux.

The first build may take a few minutes.

Afterward, look at the lower-left corner of VS Code. It should indicate that you are connected to something like:

```text
Dev Container: Python 3.13 Development
```

# Part 7: Confirm that VS Code is using Linux Python

Open a new VS Code terminal:

```text
Terminal → New Terminal
```

Run:

```shell
uname -a
```

You should see Linux.

Then run:

```shell
which python
```

Expected:

```text
/usr/local/bin/python
```

Check the version:

```shell
python --version
```

Expected:

```text
Python 3.13.x
```

Check where you are:

```shell
pwd
```

Expected:

```text
/workspace
```

You are now editing Mac files but executing everything inside Linux.

# Part 8: Test your `# %%` workflow

Create a normal file in the project root called:

```text
interactive_test.py
```

Put this inside:

```python
# %%
import sys
import platform

print(sys.executable)
print(platform.system())
print(platform.platform())

# %%
import pandas as pd

df = pd.DataFrame(
    {
        "name": ["Alice", "Bob", "Carol"],
        "score": [90, 85, 95],
    }
)

df

# %%
df.describe()
```

Above each cell, VS Code should show:

```text
Run Cell
```

Click **Run Cell** above the first section.

The results should indicate:

```text
/usr/local/bin/python
Linux
```

That confirms your interactive cells are executing inside the Docker Linux environment rather than through Anaconda or another Mac Python. VS Code recognizes `# %%` comments as Jupyter-style cells in ordinary `.py` files. ([Visual Studio Code][3])

# Part 9: Select the correct interactive kernel

The first time you press **Run Cell**, VS Code may ask you to choose a kernel.

Choose the interpreter that resembles:

```text
Python 3.13.x
/usr/local/bin/python
```

Do not choose:

```text
Anaconda
venv_py313
/Users/work/...
```

Anything beginning with `/Users/work` is a Mac interpreter.

The container interpreter should begin with:

```text
/usr/local/bin/python
```

# Part 10: Install a new package without rebuilding

Suppose you later need Polars.

In a VS Code terminal running inside the container:

```shell
python -m pip install polars
```

Or from one of your `# %%` cells:

```python
# %%
%pip install polars
```

Then use it:

```python
# %%
import polars as pl

df = pl.DataFrame(
    {
        "name": ["Alice", "Bob"],
        "score": [90, 85],
    }
)

df
```

You do **not** rebuild the container for this.

The package remains installed as long as that development container continues to exist.

# Part 11: Preserve the package list

After adding packages, update a file in your Mac project:

```shell
python -m pip freeze > requirements.txt
```

Because `/workspace` is your Mac folder, `requirements.txt` appears normally in Finder:

```text
python-dev/
├── .devcontainer/
├── interactive_test.py
└── requirements.txt
```

You can inspect it:

```shell
cat requirements.txt
```

This protects you if the container is deleted or rebuilt.

# Part 12: Make future rebuilds restore your packages

Once `requirements.txt` exists, modify `.devcontainer/Dockerfile` to this:

```dockerfile
FROM python:3.13

WORKDIR /workspace

COPY requirements.txt /tmp/requirements.txt

RUN python -m pip install --upgrade pip \
    && python -m pip install --no-cache-dir \
        ipykernel \
        jupyter \
    && python -m pip install --no-cache-dir \
        -r /tmp/requirements.txt
```

However, do this only after `requirements.txt` exists. Otherwise the `COPY` instruction will fail.

A simpler early-stage Dockerfile is:

```dockerfile
FROM python:3.13

WORKDIR /workspace

RUN python -m pip install --upgrade pip \
    && python -m pip install \
        ipykernel \
        jupyter \
        pandas \
        matplotlib \
        scikit-learn \
        fastapi \
        uvicorn
```

You can stay with that while learning.

# Your normal daily workflow

After the initial setup, your routine is simply:

1. Start Docker Desktop.
2. Open the project folder in VS Code.
3. Choose **Reopen in Container** if VS Code does not reconnect automatically.
4. Edit `.py` files.
5. Click **Run Cell** on your `# %%` sections.
6. Install new packages inside the container when needed.
7. Occasionally update `requirements.txt`.

You will **not** rebuild when you:

* Edit code
* Add a `.py` file
* Add another `# %%` section
* Change a function
* Create a CSV
* Add a FastAPI endpoint
* Install a package manually

You rebuild when you deliberately choose:

```text
Dev Containers: Rebuild Container
```

That is generally only necessary after changing the Dockerfile or the container configuration.

# The finished structure

```text
~/Documents/python/python-dev/
├── .devcontainer/
│   ├── Dockerfile
│   └── devcontainer.json
├── interactive_test.py
├── requirements.txt
├── data/
└── other_projects_or_scripts/
```

Your source files are physically stored in:

```text
~/Documents/python/python-dev
```

Your Python runtime is physically inside Docker’s Linux environment.

That is the exact separation you were looking for.

[1]: https://code.visualstudio.com/docs/devcontainers/containers?utm_source=chatgpt.com "Developing inside a Container"
[2]: https://code.visualstudio.com/docs/devcontainers/tutorial?utm_source=chatgpt.com "Dev Containers tutorial"
[3]: https://code.visualstudio.com/docs/python/jupyter-support-py?utm_source=chatgpt.com "Python Interactive window"
