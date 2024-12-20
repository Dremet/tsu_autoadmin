#!/bin/sh

### DO PYTHON THINGS
python3 run_event_end.py

### MOVE STAT FILES
# Path to the eventstats.json file
EVENT_STATS_FILE="./eventstats.json"
SESSION_STATS_FILE="./sessionstats.json"

# Directory where the file should be moved
DEST_DIR=~/stat_files

# Ensure the target directory exists
mkdir -p "$DEST_DIR"

# Check if "hotlapping": true exists in the event stats file
if grep -q '"hotlapping": true' "$EVENT_STATS_FILE"; then
  echo "Hotlapping mode detected. Removing event stats and session stats files."
  rm -f "$EVENT_STATS_FILE" "$SESSION_STATS_FILE"
  exit 0
fi

# Attempt to extract the track name from the JSON file
TRACK_NAME=$(jq -r '.level.name // empty' "$EVENT_STATS_FILE" 2>/dev/null | tr -d ' ')

# Get the current timestamp in the desired format
CURRENT_TIMESTAMP=$(date "+%Y%m%d_%H%M%S")

# Base for the new file name: timestamp
NEW_FILE_NAME="${CURRENT_TIMESTAMP}"

# Append the track name if available
if [ -n "$TRACK_NAME" ]; then
  NEW_FILE_NAME="${NEW_FILE_NAME}_${TRACK_NAME}"
fi

# Extend the file name with the file extension
EVENT_FILE_NAME="${NEW_FILE_NAME}_event.json"
SESSION_FILE_NAME="${NEW_FILE_NAME}_session.json"

# Check if the source file exists and is not empty
if [ ! -s "$EVENT_STATS_FILE" ]; then
  echo "Warning: The file '$EVENT_STATS_FILE' is empty or does not exist. An empty document will be moved."
fi

if [ ! -s "$SESSION_STATS_FILE" ]; then
  echo "Warning: The file '$SESSION_STATS_FILE' is empty or does not exist. An empty document will be moved."
fi

# Move the eventstats.json file to the target directory with the new file name
mv "$EVENT_STATS_FILE" "$DEST_DIR/$EVENT_FILE_NAME"
echo "Event stats file successfully moved to: $DEST_DIR/$EVENT_FILE_NAME"

mv "$SESSION_STATS_FILE" "$DEST_DIR/$SESSION_FILE_NAME"
echo "Session stats file successfully moved to: $DEST_DIR/$SESSION_FILE_NAME"
