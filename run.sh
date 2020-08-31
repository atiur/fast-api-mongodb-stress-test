#!/bin/sh
export MOTOR_MAX_WORKERS=20
uvicorn fastapi-stress-test:app --port 3000 --reload
