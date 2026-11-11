"""Local launcher for RedirectVPNspoof.

Запускается двойным кликом (после сборки в .exe) или командой:
    python run.py                  # дефолт: 127.0.0.1:5000
    python run.py --host 0.0.0.0 --port 8080 --no-browser

Выбирает лучший доступный WSGI-сервер:
  1. waitress  — чистый Python, кроссплатформенный (идеален для Windows и .exe)
  2. встроенный dev-сервер Flask (fallback)
"""
from __future__ import annotations

import argparse
import os
import sys
import threading
import time
import webbrowser


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="RedirectVPNspoof local launcher")
    p.add_argument("--host", default=os.environ.get("HOST", "127.0.0.1"))
    p.add_argument("--port", type=int, default=int(os.environ.get("PORT", "5000")))
    p.add_argument("--no-browser", action="store_true", help="не открывать браузер автоматически")
    p.add_argument("--debug", action="store_true", help="использовать dev-сервер Flask с debug=True")
    return p.parse_args()


def _open_browser_later(url: str, delay: float = 1.2) -> None:
    def _open() -> None:
        time.sleep(delay)
        try:
            webbrowser.open(url)
        except Exception:
            pass

    threading.Thread(target=_open, daemon=True).start()


def main() -> int:
    args = _parse_args()

    # Импортируем после разбора аргументов, чтобы --help работал без Flask.
    from app import create_app

    app = create_app()

    # Для корректных ссылок /r/<token>, когда слушаем только localhost.
    display_host = "localhost" if args.host in ("0.0.0.0", "127.0.0.1", "::") else args.host
    url = f"http://{display_host}:{args.port}/"

    print("=" * 60)
    print(f" RedirectVPNspoof запущен: {url}")
    print(f" Остановить: Ctrl+C")
    print("=" * 60, flush=True)

    if not args.no_browser:
        _open_browser_later(url)

    if args.debug:
        app.run(host=args.host, port=args.port, debug=True, use_reloader=False)
        return 0

    try:
        from waitress import serve  # type: ignore
    except ImportError:
        print("[info] waitress не найден, использую встроенный сервер Flask.", flush=True)
        app.run(host=args.host, port=args.port, debug=False, use_reloader=False)
        return 0

    serve(app, host=args.host, port=args.port, threads=8)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n[остановлено пользователем]")
        sys.exit(0)
