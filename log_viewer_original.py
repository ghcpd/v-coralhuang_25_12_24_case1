# log_viewer_original.py
#
# Primitive internal tool for searching logs.
# Intentionally minimal and not extensible.
#
# Matching semantics (IMPORTANT):
# - Reads the file line-by-line in order.
# - A line matches if `keyword` is a substring of the line (case-sensitive).
# - Returns a list of matched "raw lines" as strings, with trailing newline removed.

def search_logs(path, keyword):
    # returns a list of matching raw lines
    f = open(path, "r", encoding="utf-8", errors="replace")
    lines = f.readlines()
    f.close()

    out = []
    for line in lines:
        # keep it primitive: simple substring match, no regex, no parsing
        if keyword in line:
            out.append(line.rstrip("\n"))
    return out


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("usage: python log_viewer_original.py <path> <keyword>")
        sys.exit(2)

    p = sys.argv[1]
    k = sys.argv[2]
    res = search_logs(p, k)

    # primitive output (unstructured)
    print("matches:", len(res))
    for x in res:
        print(x)
