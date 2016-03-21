#!/bin/sh

find . -maxdepth 1 -type f -name 'max_*.txt' -exec sh -c "echo $1 > {}" \;
