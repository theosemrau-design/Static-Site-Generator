#!/bin/bash
for arg in "$@"; do
    case "$arg" in
        --server)
            SERVER=1
            ;;
        *)
            echo "Error: Unknown argument: $arg"
            exit 1
            ;;
    esac
done
python3 src/main.py
if [ -n "$SERVER" ]; then
    cd docs && python3 -m http.server 8888
fi