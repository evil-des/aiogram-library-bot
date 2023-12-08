#!/usr/bin/env bash

set -e

export DEBUG=True
exec poetry run python app/bot.py