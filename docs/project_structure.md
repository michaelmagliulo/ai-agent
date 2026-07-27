# Project Structure

This repository is a reusable Docker-based Python development template.

The goal is to provide a consistent project layout that separates production code, experimentation, documentation, testing, and project data.

---

## Directory Structure

```text
.
├── .devcontainer/
├── analysis/
├── data/
├── docs/
├── examples/
├── src/
├── tests/
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

# `.devcontainer/`

Contains the configuration used by Visual Studio Code to create and connect to the Docker development container.

This folder defines:

- The Docker image
- Python version
- Development environment
- VS Code configuration

These files are part of the project and should be committed to Git.

---

# `analysis/`

Contains exploratory Python code.

This folder is intended for learning, experimentation, debugging, and interactive development using `# %%` cells.

Examples:

- Trying a new Python library
- Testing an API
- Data exploration
- Performance experiments

Code in this folder is not considered production code.

---

# `data/`

Contains project data.

Examples include:

- CSV files
- JSON files
- Sample datasets
- Import/export files
- Test data

Large datasets and sensitive information should not be committed to Git.

---

# `docs/`

Contains project documentation.

Documentation should explain both **how** something works and **why** decisions were made.

Examples include:

- Container setup
- Package management
- Testing
- Architecture
- Design decisions
- Troubleshooting

The goal is that the project can be recreated from scratch using only the documentation.

---

# `examples/`

Contains small, self-contained examples.

Each file should demonstrate one concept with as little code as possible.

Examples:

- FastAPI example
- Pandas example
- Requests example
- Socket example
- OpenAI example

These are reference implementations, not production code.

---

# `src/`

Contains the project's production source code.

Only code that belongs in the finished application should live here.

Examples:

- API endpoints
- Business logic
- Database access
- Utility functions
- Application entry point

---

# `tests/`

Contains automated tests.

Tests verify that the application behaves correctly and help detect regressions as the project grows.

Examples:

- Unit tests
- Integration tests
- API tests

---

# `.gitignore`

Defines files and directories that Git should ignore.

Typical examples include:

- `__pycache__/`
- `.pytest_cache/`
- `.DS_Store`
- `.env`

---

# `LICENSE`

Defines the licensing terms for this repository.

This template uses the MIT License.

---

# `README.md`

Provides a high-level overview of the repository.

It should answer:

- What is this repository?
- How do I get started?
- Where can I find additional documentation?

Detailed instructions belong in the `docs/` directory.

---

# `requirements.txt`

Records the Python packages required by the project.

Each project created from this template should maintain its own dependency list.

New projects should install current package versions and then update `requirements.txt` using:

```bash
python -m pip freeze > requirements.txt
```

---

# Design Philosophy

This template intentionally separates different kinds of work.

- **Production code** belongs in `src/`
- **Experiments** belong in `analysis/`
- **Reference implementations** belong in `examples/`
- **Documentation** belongs in `docs/`
- **Automated verification** belongs in `tests/`

Keeping these responsibilities separate makes projects easier to understand, maintain, and extend over time.