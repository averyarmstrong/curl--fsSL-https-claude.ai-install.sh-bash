#!/usr/bin/env bash
# Render the poster HTML to PDF (48x36 in) and a PNG preview with headless Chromium.
set -euo pipefail
cd "$(dirname "$0")"
C=${CHROME:-/opt/pw-browsers/chromium-1194/chrome-linux/chrome}
"$C" --headless=new --no-sandbox --disable-gpu --no-pdf-header-footer --virtual-time-budget=4000 \
  --print-to-pdf="$PWD/aks_energy_week_poster.pdf" "file://$PWD/aks_energy_week_poster.html" 2>/dev/null
"$C" --headless=new --no-sandbox --disable-gpu --hide-scrollbars --virtual-time-budget=4000 --window-size=4800,3600 \
  --screenshot="$PWD/aks_energy_week_poster.png" "file://$PWD/aks_energy_week_poster.html" 2>/dev/null
pdfinfo aks_energy_week_poster.pdf | grep -E "Pages|Page size"
