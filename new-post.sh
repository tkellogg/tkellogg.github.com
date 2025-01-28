#!/bin/zsh
set -euo pipefail

# Check if the argument (slug) is provided
if [ -z "$1" ]; then
  echo "Error: Slug is missing. Please provide a slug as an argument."
  exit 1
fi
SLUG="$1"
SLUG="$(echo "$1" | sd "\\n" "" | sd "\\s" "-")"

# Get the current date in YYYY-MM-DD format
current_date=$(date +%Y-%m-%d)

# Define the file name with .md extension and current date
file_name="${current_date}-${SLUG}.md"

# Check if the _posts directory exists, create it if not
if [ ! -d "_posts" ]; then
  mkdir _posts
fi

echo "_posts/$file_name"
rg --multiline --multiline-dotall '^---.*---' $(find _posts -type f ! -empty | sort -r | head -n1)
rg --multiline --multiline-dotall '^---.*---' $(find _posts -type f ! -empty | sort -r | head -n1) | sd '^date: .*$' "date: $(date +%Y-%m-%d)" > "_posts/$file_name"

sleep 0.1

nvim "_posts/$file_name"

