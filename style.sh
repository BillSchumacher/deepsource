#!/bin/bash

isort .
black --exclude='.*\/*(venv|node_modules)\/*.*' .