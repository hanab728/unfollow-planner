# Unfollow Planner

A small Python tool that helps you decide **who to unfollow on Instagram** by
generating a manual checklist from your own data.

> **No login required.** The tool does **not** connect to Instagram, scrape
> anything, or auto-unfollow anyone. It only reads plain-text files you
> provide and writes output files you can use as a checklist.

---

## What it does

1. You provide a text file of usernames you want to unfollow (`data/given_list.txt`).
2. *(Optional)* You provide your **Following** list exported from Instagram's
   official data download (`data/following.txt`).
3. The tool writes three output files:

| File | Description |
|------|-------------|
| `output/to_unfollow.txt` | Cleaned list of usernames to unfollow (one per line) |
| `output/to_unfollow.csv` | Same list in spreadsheet/CSV format |
| `output/not_found.txt` | Usernames from your list that you don't currently follow *(only created when `following.txt` is present)* |

---

## Project layout

```
unfollow-planner/
  README.md
  requirements.txt
  .gitignore
  data/
    given_list.txt      ← your list of accounts to unfollow
    following.txt       ← (optional) your current following list
  src/
    unfollow_planner.py ← main script
  output/
    to_unfollow.txt     ← generated
    to_unfollow.csv     ← generated
    not_found.txt       ← generated (only when following.txt is present)
```

---

## Quick start

### 1 – Clone / download

```bash
git clone https://github.com/hanab728/unfollow-planner.git
cd unfollow-planner
```

### 2 – Prepare your input files

**`data/given_list.txt`** – one username per line (no `@` needed):

```
jane_doe
cool_photographer
some_brand_account
```

**`data/following.txt`** *(optional)* – one username per line.  
You can get this from Instagram's *Download Your Data* feature
(Settings → Your activity → Download your information). Convert the
exported `following.json` to one username per line, or paste usernames
manually.

Lines starting with `#` are treated as comments and ignored in both files.

### 3 – Run

```bash
python src/unfollow_planner.py
```

No third-party packages are needed – the tool uses only the Python standard
library.

### 4 – Check your output

Open `output/to_unfollow.txt` (or `to_unfollow.csv`) and work through the
list manually in the Instagram app or website.

---

## Input format details

| Feature | Behaviour |
|---------|-----------|
| Leading `@` | Stripped automatically (`@jane` → `jane`) |
| Case | Normalised to lowercase |
| Duplicates | Removed (first occurrence kept) |
| Blank lines | Ignored |
| Comment lines (`#…`) | Ignored |

---

## Requirements

Python 3.7 or newer. No third-party packages required.
