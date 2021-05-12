#!/bin/bash

# Run as root

source venv/bin/activate

export FLASK_APP=main.py
export FLASK_EN=development

flask run --host=0.0.0.0 --port=80
