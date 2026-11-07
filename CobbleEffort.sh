#!/usr/bin/env bash
# Usage: ./CobbleEffort.sh path/to/model.bbmodel   (or run it and drag the file into the terminal)
HERE="$(cd "$(dirname "$0")" && pwd)"
MODEL="$1"
if [ -z "$MODEL" ]; then
  read -r -p "Drag your .bbmodel / .geo.json here and press Enter: " MODEL
  MODEL="${MODEL%\"}"; MODEL="${MODEL#\"}"; MODEL="${MODEL%\'}"; MODEL="${MODEL#\'}"
  MODEL="${MODEL//\\ / }"; MODEL="${MODEL%% }"
fi
PYTHONPATH="$HERE${PYTHONPATH:+:$PYTHONPATH}" python3 -m cobbleeffort quick "$MODEL"
