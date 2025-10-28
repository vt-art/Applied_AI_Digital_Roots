# serve_simple.py
import argparse
import http.server
import socketserver
import webbrowser
from pathlib import Path


def parse_args():
    ap = argparse.ArgumentParser(description="Serve a folder (no auto-reload).")
    ap.add_argument("--dir", default=".", help="Directory to serve (default: .)")
    ap.add_argument(
        "--file", default="index.html", help="Entry file (default: index.html)"
    )
    ap.add_argument("--port", type=int, default=8000, help="Port (default: 8000)")
    return ap.parse_args()


def main():
    args = parse_args()
    root = Path(args.dir).resolve()
    entry = root / args.file

    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Directory not found: {root}")
    if not entry.exists():
        raise SystemExit(f"Entry file not found: {entry}")

    def Handler(*h_args, **h_kwargs):
        return http.server.SimpleHTTPRequestHandler(
            *h_args, directory=str(root), **h_kwargs
        )

    with socketserver.TCPServer(("", args.port), Handler) as httpd:
        print(f"Serving directory: {root}")
        print(f"Entry file:        {entry}")
        print(f"URL:               http://localhost:{args.port}/{args.file}")
        try:
            webbrowser.open(f"http://localhost:{args.port}/{args.file}")
        except Exception:
            pass
        print("Server running. Press Ctrl+C to stop.")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
