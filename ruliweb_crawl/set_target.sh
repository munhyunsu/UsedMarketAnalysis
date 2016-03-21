#!/bin/sh

find . -maxdepth 1 -type f -name 'target_*.txt' -exec sh -c "echo $1 > {}" \;
