#!/bin/bash

set -ev

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m pip install -r optional-requirements.txt
python3 -m pip install -r test-requirements.txt
