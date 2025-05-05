#!/bin/bash
cd /home/rui/shellrunner/
python3 -m venv env
source env/bin/activate
pip install flask gunicorn pwntools
exec sh -c "while :; do rm -rf /tmp/pwn*; sleep 10m; done" &
gunicorn -w 8 -b 0.0.0.0:8000 server:app
