#!/bin/bash
set -e -x

# Update to get latest python
brew update >/dev/null

# Pandoc to create the readme and bazaar for the translation files
brew install bazaar

# Update Python, if fails ignore
brew upgrade python || :
export PATH="/usr/local/opt/python/libexec/bin:$PATH"

# Display Python version
python -c "import sys; print sys.version"
python -c "import ssl; print ssl.OPENSSL_VERSION"

#################################
# Python modules
pip install --upgrade -r requirements.txt
pip install --upgrade -r travis/requirements_osx.txt
