#!/bin/bash

until /home/steinvord/steinvord/steinvord.py; do
     echo "Steinvord crashed with exit code $?.  Respawning.." >&2
     sleep 1
done
