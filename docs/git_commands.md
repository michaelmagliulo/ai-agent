# GitHub Quick Reference

This document contains the Git and GitHub commands I commonly use when creating and maintaining projects.

---

# First-Time Repository Setup

## Initialize Git

```bash
git init
```

---

## Rename the default branch to `main`

Some versions of Git still create `master` by default.

Rename it before making your first push:

```bash
git branch -M main
```

---

## Stage all files

```bash
git add .
```

---

## Commit

```bash
git commit -m "Initial release"
```

---

## Connect to GitHub

```bash
git remote add origin https://github.com/<username>/<repository>.git
```

Verify:

```bash
git remote -v
```

---

## First Push

```bash
git push --set-upstream origin main
```

This creates the remote branch and links the local `main` branch to it.

Future pushes only require:

```bash
git push
```

---

# Daily Workflow

Check status:

```bash
git status
```

See changes:

```bash
git diff
```

Stage everything:

```bash
git add .
```

Commit:

```bash
git commit -m "Describe what changed"
```

Push:

```bash
git push
```

Pull latest changes:

```bash
git pull
```

---

# Branch Information

Current branch:

```bash
git branch
```

View remote branches:

```bash
git branch -a
```

---

# Remotes

View remotes:

```bash
git remote -v
```

Change the remote URL:

```bash
git remote set-url origin <url>
```

Remove remote:

```bash
git remote remove origin
```

---

# Tags

Create a version tag:

```bash
git tag v1.0.0
```

Push the tag:

```bash
git push origin v1.0.0
```

List tags:

```bash
git tag
```

---

# Helpful Log Commands

Compact history:

```bash
git log --oneline
```

Graph history:

```bash
git log --graph --decorate --oneline --all
```

---

# Ignore Files

If a file should never be tracked:

1. Add it to `.gitignore`

Then remove it from Git tracking:

```bash
git rm --cached <file>
```

Commit:

```bash
git commit -m "Stop tracking file"
```

---

# Clone an Existing Repository

```bash
git clone https://github.com/<username>/<repository>.git
```

---

# Common Problems

## Authentication Failed

GitHub no longer accepts account passwords for Git operations.

Use one of:

- GitHub CLI (`gh auth login`)
- Personal Access Token (PAT)
- SSH keys

---

## Branch has no upstream

```
fatal: The current branch has no upstream branch.
```

Fix:

```bash
git push --set-upstream origin main
```

Afterwards:

```bash
git push
```

works normally.

---

## Check Configuration

```bash
git config --list
```

User name:

```bash
git config --global user.name
```

Email:

```bash
git config --global user.email
```

Set them:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

---

# Useful Aliases (Optional)

```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.cm commit
```

Then you can type:

```bash
git st
git cm -m "message"
```

instead of the longer commands.