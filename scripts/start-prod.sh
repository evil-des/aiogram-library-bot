#!/usr/bin/env bash

set -e

export DEBUG=False
exec poetry run python app/bot.py