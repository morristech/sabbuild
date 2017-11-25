#!/bin/bash
set -e -x

# Update to get latest python
brew update >/dev/null

# Pandoc to create the readme and bazaar for the translation files
brew install bazaar

# Update Python 2.7.13
brew install https://raw.githubusercontent.com/Homebrew/homebrew-core/dad1a47c6722455fd7390c0ff99c72cc7503ef1d/Formula/python.rb
export PATH="/usr/local/opt/python/libexec/bin:$PATH"

# Display Python version
python -c "import sys; print sys.version"
python -c "import ssl; print ssl.OPENSSL_VERSION"

#################################
# Python modules
pip install --upgrade -r requirements.txt
pip install --upgrade -r travis/requirements_osx.txt
