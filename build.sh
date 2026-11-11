#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
if [ ! -x ".venv/bin/python" ]; then
    python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-build.txt
pyinstaller --clean -y RedirectVPNspoof.spec
echo
echo "======================================================"
echo "Done. Executable: dist/RedirectVPNspoof"
echo "======================================================"
