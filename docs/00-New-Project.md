Since `python-dev-template` is now a **GitHub template repository**, do not clone the template directly. First create a new repository from it so the AI agent gets its own name, remote, and Git history.

## 1. Create the new repository on GitHub

Open your `python-dev-template` repository on GitHub.

Click:

```text
Use this template
→ Create a new repository
```

Name the new repository something like:

```text
ai-agent
```

or, more specifically:

```text
personal-ai-agent
```

Choose public or private, then click:

```text
Create repository
```

GitHub will copy the template’s files into a completely new repository. The new project will not inherit the template repository’s commit history. ([GitHub Docs][1])

---

## 2. Clone the new AI-agent repository onto your Mac

Do this from your normal Mac terminal, **not from inside the existing template container**.

First go to your Python projects folder:

```bash
cd /Users/work/Documents/python
```

Then clone the newly created repository:

```bash
git clone https://github.com/michaelmagliulo/ai-agent.git
```

Replace `ai-agent` with the exact repository name you chose.

GitHub cloning creates a local copy that includes the repository files, Git configuration, branches, and history. ([GitHub Docs][2])

---

## 3. Enter the project

```bash
cd ai-agent
```

Check that the correct remote was created:

```bash
git remote -v
```

You should see:

```text
origin  https://github.com/michaelmagliulo/ai-agent.git (fetch)
origin  https://github.com/michaelmagliulo/ai-agent.git (push)
```

Notice that `origin` should point to the **new AI-agent repository**, not `python-dev-template`.

---

## 4. Open it in VS Code

```bash
code .
```

Make sure VS Code opens the folder itself and does not display:

```text
UNTITLED (WORKSPACE)
```

The Explorer heading should show something like:

```text
AI-AGENT
```

---

## 5. Open it in the Dev Container

In VS Code:

```text
Command Palette
→ Dev Containers: Reopen in Container
```

Because the project already contains:

```text
.devcontainer/
├── Dockerfile
└── devcontainer.json
```

VS Code should build the Python environment automatically.

The first build may take several minutes because it must install:

* Python
* Jupyter
* pandas
* matplotlib
* scikit-learn
* FastAPI
* Uvicorn
* Git
* GitHub CLI
* the other Linux utilities you added

---

## 6. Verify that this is the new project

Inside the Dev Container terminal, run:

```bash
pwd
```

It will probably report:

```text
/workspace
```

Then run:

```bash
git remote -v
```

Confirm that it says:

```text
michaelmagliulo/ai-agent.git
```

Also run:

```bash
git status
```

You should initially see:

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

---

## 7. Replace the template placeholders

Your template likely contains files such as:

```text
src/main.py
analysis/scratch.py
tests/test_main.py
README.md
```

Now customize them for the AI agent.

For example, revise `README.md` so it begins with:

```markdown
# AI Agent

A containerized Python project for developing and testing a personal AI agent.
```

You can also clear out placeholder code from:

```text
src/main.py
analysis/scratch.py
tests/test_main.py
```

Keep the folders and documentation that remain useful.

---

## 8. Commit the project customization

After changing the README and starter files:

```bash
git status
git add .
git commit -m "Initialize AI agent project from Python template"
git push
```

Because the repository was cloned from GitHub, its local `main` branch should already track `origin/main`, so you normally will not need `--set-upstream` this time.

## The important distinction

You now have two separate repositories:

```text
python-dev-template
```

This is the reusable foundation. Improve it only when you discover something that should benefit every future Python project.

```text
ai-agent
```

This is the actual application. Agent prompts, tools, APIs, business logic, experiments, and tests belong here.

Changes made in `ai-agent` will not automatically alter the template. That separation is exactly what you want.

[1]: https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository?utm_source=chatgpt.com "Creating a new repository"
[2]: https://docs.github.com/articles/cloning-a-repository?utm_source=chatgpt.com "Cloning a repository"
