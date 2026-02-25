"""
Unfollow Planner
----------------
Reads a list of usernames you want to unfollow (given_list.txt) and,
optionally, your current following list (following.txt). It then produces:

  output/to_unfollow.txt  – cleaned list of usernames to unfollow
  output/to_unfollow.csv  – same list in CSV format
  output/not_found.txt    – usernames from your list that you don't follow
                            (only when following.txt is present)
"""

import csv
import os
import sys


DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")

GIVEN_LIST_PATH = os.path.join(DATA_DIR, "given_list.txt")
FOLLOWING_PATH = os.path.join(DATA_DIR, "following.txt")

TO_UNFOLLOW_TXT = os.path.join(OUTPUT_DIR, "to_unfollow.txt")
TO_UNFOLLOW_CSV = os.path.join(OUTPUT_DIR, "to_unfollow.csv")
NOT_FOUND_TXT = os.path.join(OUTPUT_DIR, "not_found.txt")


def read_usernames(filepath):
    """Read usernames from a text file, one per line.

    Lines that are blank or start with '#' are ignored.
    Leading/trailing whitespace and a leading '@' are stripped.
    Returns a list of lowercase usernames preserving order (duplicates kept).
    """
    usernames = []
    with open(filepath, "r", encoding="utf-8") as fh:
        for raw_line in fh:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            # Strip optional leading '@'
            line = line.lstrip("@")
            usernames.append(line.lower())
    return usernames


def build_unfollow_list(given, following=None):
    """Return (to_unfollow, not_found) lists.

    Parameters
    ----------
    given : list[str]
        Usernames the user wants to unfollow (may contain duplicates).
    following : list[str] or None
        Usernames the user currently follows. When None, every entry in
        *given* goes straight into *to_unfollow*.

    Returns
    -------
    to_unfollow : list[str]
        Deduplicated, ordered list of usernames to unfollow.
    not_found : list[str]
        Usernames that were in *given* but not found in *following*.
        Always empty when *following* is None.
    """
    # Deduplicate while preserving order
    seen = set()
    unique_given = []
    for name in given:
        if name not in seen:
            seen.add(name)
            unique_given.append(name)

    if following is None:
        return unique_given, []

    following_set = set(following)
    to_unfollow = []
    not_found = []
    for name in unique_given:
        if name in following_set:
            to_unfollow.append(name)
        else:
            not_found.append(name)

    return to_unfollow, not_found


def write_txt(filepath, usernames):
    """Write a list of usernames to a plain-text file, one per line."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as fh:
        for name in usernames:
            fh.write(name + "\n")


def write_csv(filepath, usernames):
    """Write a list of usernames to a CSV file with a header row."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["username"])
        for name in usernames:
            writer.writerow([name])


def main():
    # --- Read given list ---
    if not os.path.exists(GIVEN_LIST_PATH):
        print(f"ERROR: Given list not found at '{GIVEN_LIST_PATH}'")
        print("Please create data/given_list.txt with one username per line.")
        sys.exit(1)

    given = read_usernames(GIVEN_LIST_PATH)
    if not given:
        print("No usernames found in data/given_list.txt. Nothing to do.")
        sys.exit(0)

    # --- Optionally read following list ---
    following = None
    if os.path.exists(FOLLOWING_PATH):
        following = read_usernames(FOLLOWING_PATH)
        print(f"Following list loaded: {len(following)} account(s).")
    else:
        print(
            "No following list found (data/following.txt). "
            "Skipping verification – all given usernames will be included."
        )

    # --- Build results ---
    to_unfollow, not_found = build_unfollow_list(given, following)

    # --- Write outputs ---
    write_txt(TO_UNFOLLOW_TXT, to_unfollow)
    write_csv(TO_UNFOLLOW_CSV, to_unfollow)

    print(f"\nDone! {len(to_unfollow)} username(s) to unfollow.")
    print(f"  output/to_unfollow.txt  – plain-text checklist")
    print(f"  output/to_unfollow.csv  – spreadsheet format")

    if following is not None and not_found:
        write_txt(NOT_FOUND_TXT, not_found)
        print(
            f"\nNote: {len(not_found)} username(s) from your list were not found "
            f"in your following list and were skipped."
        )
        print(f"  output/not_found.txt    – skipped usernames")
    elif following is not None:
        print("\nAll usernames in your list are in your following list.")


if __name__ == "__main__":
    main()
