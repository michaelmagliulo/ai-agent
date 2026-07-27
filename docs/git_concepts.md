# Git Concepts

Git is not simply a backup program.

It is a version control system that records the complete history of a project.

Once you understand a few core concepts, nearly every Git command becomes easy to remember.

---

# Repository

A repository (repo) is a folder that Git watches.

Everything inside can be versioned.

Example:

my-project/
├── src/
├── tests/
├── README.md
└── .git/

The hidden `.git` folder contains all of Git's history and metadata.

Deleting `.git` removes the repository's history but leaves your project files intact.

---

# Working Directory

Your working directory is simply your project as it currently exists on disk.

You edit files here.

Git does not automatically save these changes.

---

# Tracked vs Untracked Files

Tracked files

Git already knows about these files.

Example:

README.md

Untracked files

Git has never been told to track them.

Example:

new_script.py

Use

git add

to begin tracking them.

---

# The Three Git States

Every file lives in one of three places.

Working Directory

↓

Staging Area

↓

Repository (Commit)

Think of it like writing a book.

Working Directory

You're writing the chapter.

Staging Area

You've decided which pages are finished.

Commit

You've published that edition.

---

# git add

This command does NOT save your work.

It moves changes into the staging area.

Example

git add README.md

or

git add .

Meaning

"I want these changes included in my next snapshot."

---

# Commit

A commit is a permanent snapshot.

Think of it as taking a photograph of your project.

Each commit has

- a unique ID
- a timestamp
- an author
- a message
- a pointer to the previous commit

Example

A
↓

B
↓

C

Git stores changes efficiently, but conceptually think of every commit as a complete version of your project.

---

# HEAD

HEAD means

"This is where I currently am."

If HEAD points to commit C

A → B → C ← HEAD

you're working from commit C.

---

# Branch

A branch is simply a movable label.

main

↓

A → B → C

When you create another branch

feature

↓

A → B → C

both labels point to the same commit.

As you commit

main

↓

A → B → C

             \
feature       D → E

Only the feature branch moves.

The main branch stays where it was.

---

# main vs master

Historically Git used

master

Most projects today use

main

Rename

git branch -M main

GitHub creates new repositories using `main`.

---

# Remote

Your local repository lives on your computer.

A remote repository lives somewhere else.

Usually GitHub.

Local

↓

Your Computer

Remote

↓

GitHub

Connecting them

git remote add origin https://github.com/username/project.git

---

# origin

origin is only a nickname.

It usually means

"The GitHub repository."

You could call it

production

or

bob

but almost everyone uses

origin

---

# Push

Push means

"Copy my commits to GitHub."

Nothing more.

It does NOT create commits.

It uploads commits.

---

# Pull

Pull means

"Download commits from GitHub."

Then merge them into my work.

---

# Clone

Clone means

"Download an entire repository."

Including

- history
- branches
- tags

Everything.

---

# Fetch

Fetch downloads new commits

WITHOUT changing your work.

Pull = Fetch + Merge

---

# Merge

Suppose

main

A → B → C

feature

A → B → C → D → E

Merge combines them.

Result

A → B → C → D → E → M

where M is a merge commit.

---

# Conflict

If two people edit the same lines

Git cannot decide.

It asks you.

This is called a merge conflict.

You choose the correct version.

---

# .gitignore

Some files should never be stored.

Examples

__pycache__/

.env

node_modules/

build/

These belong in

.gitignore

---

# Tags

A tag is a permanent label.

Example

v1.0.0

↓

A → B → C

Unlike branches

tags never move.

They mark important releases.

---

# GitHub

Git stores history.

GitHub stores repositories online.

Git works perfectly without GitHub.

GitHub simply adds

- cloud storage
- collaboration
- pull requests
- issue tracking
- releases

---

# Common Workflow

1. Edit files

↓

2. git status

↓

3. git add .

↓

4. git commit -m "Describe the work"

↓

5. git push

---

# Think Like Git

Git does not think in files.

Git thinks in snapshots.

Every commit is another snapshot in the history of your project.

Your job is simply to tell Git:

"What version of my project do I want to remember forever?"