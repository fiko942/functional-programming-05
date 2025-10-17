Golden Dragon Wok - CLI ERP (functional core)

Quick start

1. Create a virtualenv and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Seed data and try commands:

```bash
python -m src.cli.main seed
python -m src.cli.main menu list
python -m src.cli.main inventory list
```

Project layout

- src/domain: pure functions only (no I/O)
	- menu.py          (PURE) - CRUD and validation for menu items
	- inventory.py     (PURE) - CRUD and stock adjustments, low-stock generator
	- recipes.py       (PURE) - recipe lookup, stock deduction logic
	- supplier.py      (PURE) - supplier CRUD
	- staff.py         (PURE) - staff CRUD
	- sales.py         (PURE) - create_order, add_item, void_item, close_order (business rules)
	- purchase.py      (PURE) - create_po, receive_po
	- pricing.py       (PURE) - subtotal, tax, service, total calculation
	- reports.py       (PURE) - generator-based reports (sales_by_date_generator, top_selling_menu)
	- validation.py    (PURE) - helper validation functions

- src/data: repository adapters (I/O - impure)
	- repository.py    (IMPURE) - Repository ABC + InMemoryRepository (in-memory)
	- json_repo.py     (IMPURE) - JSON file-based repository (reads/writes data/*.json)
	- seed.py          (IMPURE) - seed example data into repository

- src/cli: command-line adapters / I/O layer (IMPURE)
	- main.py          (IMPURE) - interactive TUI (prompt_toolkit + rich) with menus
	- main_simple.py   (IMPURE) - stdlib input/print based menu-driven CLI
	- src/cli/main.py  (IMPURE) - argparse-based legacy CLI commands

- Other tooling
	- main_purefunction_declarative.py (MIXED) - purely functional report helpers + small I/O runner (I/O only at top-level)
	- tests/           - pytest tests for pure domain logic

Pure vs impure rules in this project:
- "PURE" modules contain functions that accept inputs and return outputs without printing,
	reading/writing files, or mutating global state. Use these for business logic and unit tests.
- "IMPURE" modules perform I/O (console, filesystem) or manage persistence. Keep these
	thin and call into the pure domain functions.
