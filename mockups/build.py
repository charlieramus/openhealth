#!/usr/bin/env python3
"""Inline the Inter woff2 subsets into thermal.src.html -> thermal.html.

The published artifact may make zero network calls (CLAUDE.md), so the face
has to travel inside the file. Fetching the woff2 happens here, at build time,
which is the same arrangement garmin.json already uses: a local script that
writes a committed file, not a server.

    python mockups/build.py <dir-holding-inter-NNN.woff2>
"""
import base64
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
WEIGHTS = (400, 500, 600, 700)


def main() -> int:
    src = HERE / "thermal.src.html"
    out = HERE / "thermal.html"
    fonts = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "fonts"

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

    html = src.read_text(encoding="utf-8").replace("/*INTER_FACES*/", "\n".join(faces))
    out.write_text(html, encoding="utf-8")

    print(
        f"wrote {out.name}: {out.stat().st_size / 1024:.0f}KB "
        f"({len(WEIGHTS)} weights, {total / 1024:.0f}KB of woff2 before encoding)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
