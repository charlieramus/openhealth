#!/usr/bin/env python3
"""Inline the Inter woff2 subsets into a page, as base64.

The published artifact may make zero network calls (CLAUDE.md), so the face
has to travel inside the file. Reading the woff2 happens here, at build time,
which is the same arrangement scripts/build_corpus.py already uses: a local
script that writes a committed file, not a server.

    python mockups/build.py                    # thermal.src.html -> thermal.html
    python mockups/build.py --into index.html  # fill the app's face block in place
    python mockups/build.py <dir-holding-inter-NNN.woff2>

The gallery carries a bare `/*INTER_FACES*/` placeholder, which is replaced on
the way to a second file. `--into` instead rewrites one file in place between

    /*INTER_FACES:BEGIN*/ ... /*INTER_FACES:END*/

markers, so re-running is idempotent and the app stays a single file with no
build step of its own. UPDATELOGV3 Stage 2.
"""
import base64
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
WEIGHTS = (400, 500, 600, 700)
BEGIN = "/*INTER_FACES:BEGIN*/"
END = "/*INTER_FACES:END*/"


def main() -> int:
    args = list(sys.argv[1:])
    into = None
    if "--into" in args:
        i = args.index("--into")
        if i + 1 >= len(args):
            print("--into needs a path", file=sys.stderr)
            return 1
        into = (ROOT / args[i + 1]).resolve()
        del args[i:i + 2]

    src = HERE / "thermal.src.html"
    out = HERE / "thermal.html"
    fonts = pathlib.Path(args[0]) if args else HERE / "fonts"

    faces = []
    total = 0
    for w in WEIGHTS:
        f = fonts / f"inter-{w}.woff2"
        if not f.exists():
            print(f"missing {f}", file=sys.stderr)
            return 1
        raw = f.read_bytes()
        total += len(raw)
        b64 = base64.b64encode(raw).decode("ascii")
        faces.append(
            "@font-face{font-family:'Inter';font-style:normal;font-weight:%d;"
            "font-display:block;src:url(data:font/woff2;base64,%s) format('woff2')}"
            % (w, b64)
        )

    # A metric-matched local fallback keeps the layout from reflowing on the
    # first paint, and keeps the file honest if the data URI is ever stripped.
    faces.append(
        "@font-face{font-family:'Inter Fallback';src:local('Segoe UI'),"
        "local('Helvetica Neue'),local('Arial');ascent-override:96.9%;"
        "descent-override:24.2%;line-gap-override:0%;size-adjust:107%}"
    )

    block = "\n".join(faces)

    if into is not None:
        page = into.read_text(encoding="utf-8")
        if BEGIN not in page or END not in page:
            print(f"{into.name} has no {BEGIN} / {END} markers", file=sys.stderr)
            return 1
        page = re.sub(
            re.escape(BEGIN) + r".*?" + re.escape(END),
            BEGIN + "\n" + block + "\n" + END,
            page,
            flags=re.S,
        )
        into.write_text(page, encoding="utf-8")
        print(
            f"filled {into.name}: {into.stat().st_size / 1024:.0f}KB "
            f"({len(WEIGHTS)} weights, {total / 1024:.0f}KB of woff2 before encoding)"
        )
        return 0

    html = src.read_text(encoding="utf-8").replace("/*INTER_FACES*/", block)
    out.write_text(html, encoding="utf-8")

    print(
        f"wrote {out.name}: {out.stat().st_size / 1024:.0f}KB "
        f"({len(WEIGHTS)} weights, {total / 1024:.0f}KB of woff2 before encoding)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
