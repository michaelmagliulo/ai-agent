# Git Internals

Git often feels complicated until you realize one thing:

**Git is basically a content-addressed database with pointers.**

Everything else is built on top of that idea.

---

# The Big Picture

A Git repository is really just

```
Project Files
        │
        ▼
 Staging Area (Index)
        │
        ▼
     Git Objects
        │
        ▼
    Branch Pointers
```

Every Git command simply manipulates one of these pieces.

---

# The .git Folder

The hidden `.git` directory is the repository.

Your project files are **not** Git.

Git lives here.

Example

```
.git/

HEAD
config
index
objects/
refs/
logs/
hooks/
```

Deleting `.git`

removes

- commit history
- branches
- tags
- remotes

Your source code remains.

---

# Objects

Git stores four kinds of objects.

1. Blob
2. Tree
3. Commit
4. Tag

Everything is one of these.

---

# Blob

A blob stores file contents.

Nothing else.

Example

```
hello.py
```

contains

```python
print("Hello")
```

Git stores

```
Blob

print("Hello")
```

Notice

Git does NOT store

- filename
- permissions
- folder

Only bytes.

---

# Tree

Trees represent directories.

Example

```
src/

main.py

util.py
```

Git stores

```
Tree

main.py -> Blob A

util.py -> Blob B
```

Trees connect names to blobs.

---

# Commit

A commit stores

- tree
- parent commit
- author
- timestamp
- message

Example

```
Commit

Tree: abc123

Parent: def456

Author: Michael

Message: Add login page
```

Notice

The commit does NOT contain the files.

It points to the tree.

The tree points to blobs.

---

# Tag

A tag simply points to a commit.

Example

```
v1.0

↓

Commit C
```

Unlike branches

tags never move.

---

# SHA Hashes

Every Git object has a SHA hash.

Example

```
9fceb02d0ae598...
```

Git uses the hash as the object's ID.

The hash depends entirely on the object's contents.

If the contents change

the hash changes.

---

# Why SHA Hashes Matter

Suppose

```
README.md
```

changes

from

```
Hello
```

to

```
Hello World
```

Git creates

an entirely new blob.

The old blob still exists.

Nothing is overwritten.

---

# Immutability

Git objects never change.

Ever.

Instead

Git creates new objects.

Old history remains intact.

This is one reason Git is so reliable.

---

# The Object Database

All objects live inside

```
.git/objects/
```

They are compressed.

Git automatically reuses identical objects.

If two commits contain the exact same file

Git stores only ONE blob.

---

# HEAD

HEAD is simply a pointer.

Usually

```
HEAD

↓

main
```

which points to

```
Commit C
```

Meaning

```
HEAD

↓

main

↓

Commit C
```

HEAD tells Git

"This is where I'm working."

---

# Detached HEAD

Normally

HEAD points to a branch.

Sometimes

HEAD points directly to a commit.

```
HEAD

↓

Commit B
```

This is called

Detached HEAD.

You can experiment safely.

But commits made here are easy to lose unless you create a branch.

---

# Branches

A branch is NOT a copy.

A branch is only a label.

Example

```
main

↓

Commit C
```

After

```
git branch feature
```

you have

```
main

↓

Commit C

↑

feature
```

Both labels point to the same commit.

Nothing was duplicated.

---

# Making a Commit

Suppose

```
feature

↓

Commit C
```

You commit.

Git creates

```
Commit D
```

Then

moves

```
feature
```

forward.

```
main

↓

C

      \
feature

↓

D
```

The branch moved.

The commits didn't.

---

# Why Branches Are Cheap

Since a branch is only a pointer

creating one takes almost no space.

Creating hundreds of branches is normal.

---

# Refs

Branches and tags are called references.

Or

refs.

They live in

```
.git/refs/
```

A branch file literally contains a commit hash.

That's all.

---

# The Index

The staging area is called

the Index.

It lives here

```
.git/index
```

When you run

```bash
git add file.py
```

Git updates the Index.

Nothing has been committed yet.

---

# Commit Process

```
Edit File

↓

git add

↓

Index Updated

↓

git commit

↓

New Tree

↓

New Commit

↓

Branch Moves
```

---

# Garbage Collection

Old unreachable objects stay around.

Eventually

Git cleans them.

```
git gc
```

compresses

and removes unreachable objects.

---

# Packfiles

Repositories with thousands of objects become slow.

Git packs them into

Packfiles.

This reduces storage dramatically.

You normally never think about this.

Git handles it automatically.

---

# Merge

Suppose

```
A

↓

B

↓

C
```

Feature becomes

```
A

↓

B

↓

C

↓

D

↓

E
```

Meanwhile

main becomes

```
A

↓

B

↓

C

↓

F
```

Merge creates

```
        D

        ↓

A → B → C → F

        ↘

         M

        ↗

        E
```

Merge commit M has

two parents.

---

# Rebase

Merge preserves history.

Rebase rewrites history.

Instead of

```
A

↓

B

↓

C

↓

D

↓

E
```

Git recreates

D

and

E

on top of

main.

Cleaner history.

Different commit hashes.

---

# Cherry-pick

Cherry-pick copies

ONE commit

onto another branch.

Useful when

only one change is needed.

---

# Why Git Rarely Loses Data

Git almost never deletes objects immediately.

Even if you

```
git reset

git checkout

git branch -D
```

the objects often still exist.

Git simply loses the pointer.

This is why many "lost" commits can be recovered.

---

# reflog

Git records where HEAD has been.

View it with

```bash
git reflog
```

This is one of Git's greatest recovery tools.

If you accidentally delete a branch or reset too far, `git reflog` often lets you find the commit and recover it.

---

# Why Git Is Fast

Git does not compare files every time.

It compares hashes.

Equal hash

↓

Same content

Different hash

↓

Different content

This makes operations extremely fast.

---

# Mental Model

Git is not a folder full of files.

Git is

a database

plus

a graph

plus

a few movable pointers.

The source code is simply one view into that database.

Understanding this makes nearly every Git command logical instead of something to memorize.



One thing I'd add that most Git tutorials don't

I think the most helpful mental shift is this:

Git doesn't care about files—it cares about objects and relationships.

When you run git commit, Git isn't thinking, "Save my project." It's thinking:

Create blobs for any new file contents.
Create trees describing the directory structure.
Create a commit pointing to that tree and its parent commit.
Move the current branch pointer to the new commit.

Once you see Git as a graph of immutable objects connected by pointers, commands like branch, merge, rebase, checkout, and reset become operations on that graph rather than mysterious magic. For someone who enjoys understanding systems from the inside out, that's the model that tends to stick.