#!/bin/bash
set -e -x

# Pandoc to create the readme and bazaar for the translation files
brew install pandoc bazaar

# Display Python version
python -c "import sys; print sys.version"
python -c "import ssl; print ssl.OPENSSL_VERSION"

#################################
# Python modules
pip install --upgrade -r requirements.txt
pip install --upgrade -r travis/requirements_osx.txt

#################################
# Sleepless module install
cd builder/osx/sleepless/
python setup.py install
cd ../../../
