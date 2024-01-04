#!/bin/bash

OUTPUT_BIN="main"

echo "starting watcher"

# Ensure the dependencies are met
go mod tidy
# Build the app
go build -o $OUTPUT_BIN main.go

# Check if not in dev mode
if [ "$USE_DEV_MODE" != "true" ]; then
  go build -o $OUTPUT_BIN main.go
fi

# Execute the project
if [ "$USE_DEV_MODE" = "true" ]; then
  nodemon --exec go run main.go;
else
  ./$OUTPUT_BIN
fi

# Run the daemon
./watcher