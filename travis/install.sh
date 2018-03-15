#!/bin/bash
set -e -x

# Force update
brew update >/dev/null

# Pandoc to create the readme and bazaar for the translation files
brew install bazaar

# Update Python, if fails ignore
brew install python@2 || true
brew link --overwrite python@2

# Display Python version
python -c "import sys; print sys.version"
python -c "import ssl; print ssl.OPENSSL_VERSION"

#################################
# Python modules
pip install --upgrade -r requirements.txt
pip install --upgrade -r travis/requirements_osx.txt
