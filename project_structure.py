from pathlib import Path
import fnmatch


def load_gitignore(root: Path):
    gitignore = root / ".gitignore"
    patterns = []

    if gitignore.exists():
        with gitignore.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                patterns.append(line.rstrip("/"))

    return patterns


def is_ignored(path: Path, root: Path, patterns, extra_ignored):
    rel = path.relative_to(root).as_posix()

    if path.name in extra_ignored:
        return True

    for pattern in patterns:
        if (
            fnmatch.fnmatch(rel, pattern)
            or fnmatch.fnmatch(path.name, pattern)
            or rel.startswith(pattern + "/")
        ):
            return True

    return False


def print_structure(root: Path, prefix="", patterns=None, extra_ignored=None):
    if patterns is None:
        patterns = []

    if extra_ignored is None:
        extra_ignored = set()

    items = sorted(
        root.iterdir(),
        key=lambda p: (p.is_file(), p.name.lower())
    )

    items = [
        p for p in items
        if (p.is_dir() or p.suffix == ".py")
        and not is_ignored(p, project_root, patterns, extra_ignored)
    ]

    for i, item in enumerate(items):
        connector = "└── " if i == len(items) - 1 else "├── "
        print(prefix + connector + item.name)

        if item.is_dir():
            extension = "    " if i == len(items) - 1 else "│   "
            print_structure(
                item,
                prefix + extension,
                patterns,
                extra_ignored,
            )


if __name__ == "__main__":
    project_root = Path(
        input("Project path (blank=current): ").strip() or "."
    ).resolve()

    extra_ignored = {
        ".git",
        ".idea",
        ".vscode",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
    }

    gitignore_patterns = load_gitignore(project_root)

    print(project_root.name)
    print_structure(
        project_root,
        patterns=gitignore_patterns,
        extra_ignored=extra_ignored,
    )
