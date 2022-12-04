#!/bin/sh

set -e

if [ "$1" = "book" ]; then
    echo "Executing a \"book\" command..."
    exec python3 src/book.py
fi

exec "$@"
