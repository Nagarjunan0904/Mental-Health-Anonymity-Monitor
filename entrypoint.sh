#!/bin/bash
set -e

echo "[INFO] Starting Project 1 Data Collector container..."
mkdir -p /app/data
exec python main.py
