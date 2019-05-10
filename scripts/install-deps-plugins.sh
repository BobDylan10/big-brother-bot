#!/bin/bash

set -ev

pip3 install --upgrade pip
pip3 install -r requirements.txt
pip3 install -r optional-requirements.txt
pip3 install -r test-requirements.txt
