"""Print the declarative GraphFlow nodes, links, and paths."""

from topology import HOSTS, LINKS, PATHS, SWITCHES


def main():
    print("hosts:", " ".join(HOSTS))
    print("switches:", " ".join(SWITCHES))
    print("links:", ", ".join(f"{left}-{right}" for left, right in LINKS))
    print("paths:")
    for path in PATHS:
        print("  " + " -> ".join(path))


if __name__ == "__main__":
    main()
