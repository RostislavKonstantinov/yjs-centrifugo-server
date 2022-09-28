#!/bin/sh

set -o errexit -o nounset

echo "$@"
exec bash -c "$@"
