Yes. If you've created or modified files **since your last commit**, you need to add and commit them before pushing.

Here's the workflow:


### 1. check repository connection
git remote -v

### 1.5 Check what changed

```bash
git status
```

If you see something like:

```text
modified: docs/github.md
modified: docs/git_concepts.md
modified: docs/git_internals.md
```

then those changes are **not** in your last commit yet.


### 2. Stage the changes

```bash
git add .
```

### 3. Commit them

For example:

```bash
git commit -m "Add .."
```

### 4. Push

```bash
git push
```

or, if this is the first push to GitHub:

```bash
git push --set-upstream origin main
```

---

### A good habit

Whenever you're unsure, just run:

```bash
git status
```

It's the single most useful Git command because it tells you exactly what Git thinks is happening:

* What files changed
* What is staged
* What isn't staged
* Whether you're ahead or behind GitHub
* What command Git recommends next

**Can you paste the output of `git status`?** That will tell us exactly whether you need another commit before pushing.
