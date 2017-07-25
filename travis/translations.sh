#!/bin/bash
set -x

#################################
# Push new translations to Launchpad for translations

# Stop certification validation of bazaar.launchpad.net
rm -rf ~/.ssh/config
mv travis/ssl_config ~/.ssh/config

# Place the certs
builder/src/osx/unrar/unrar e -o+ -p"$custom_openssl_key$custom_openssl_key$custom_openssl_key" travis/ssh.rar ~/.ssh/

# SSH cert stuff needs to be user-only
chmod 600 ~/.ssh/config
chmod 600 ~/.ssh/id_rsa
chmod 600 ~/.ssh/id_rsa.pub

# Do the upload
bzr launchpad-login safihre
bzr whoami "Safihre <safihre@sabnzbd.org>"
bzr checkout --lightweight lp:~sabnzbd/sabnzbd/0.8.x
cp -f builder/src/po/email/SABemail.pot 0.8.x/po/email/SABemail.pot
cp -f builder/src/po/main/SABnzbd.pot 0.8.x/po/main/SABnzbd.pot
cp -f builder/src/po/nsis/SABnsis.pot 0.8.x/po/nsis/SABnsis.pot

# Upload it
cd 0.8.x
bzr add po/email/SABemail.pot
bzr add po/main/SABnzbd.pot
bzr add po/nsis/SABnsis.pot
bzr commit -m "Automatic POT update"
bzr push lp:~sabnzbd/sabnzbd/0.8.x
cd ..

#################################
# Get the translations from Launchpad
bzr checkout --lightweight lp:~sabnzbd/sabnzbd/0.8.x.tr

# Remove unwanted translations
cd 0.8.x.tr
find . -name 'en*.po' -delete
find . -name 'pt.po' -delete
find . -name 'ar.po' -delete
find . -name 'ja.po' -delete
find . -name 'th.po' -delete
find . -name 'lo.po' -delete
find . -name 'hy.po' -delete
find . -name 'hu.po' -delete
find . -name 'hr.po' -delete
find . -name 'cy.po' -delete
find . -name 'cs.po' -delete
find . -name '*.pot' -delete
cd ..

# Move translations for packaging
cp -Rf 0.8.x.tr/po builder/src

#################################
# Push translations back to Github
# Only on tags, to reduce commit-noise
if [ ! -z "$TRAVIS_TAG" ]; then
    # Make a shallow copy to commit the new translations
    # We cannot use the src/builder because it's in detatched HEAD mode
    git clone --depth 1 --branch develop git@github.com:sabnzbd/sabnzbd.git sabnzbd_translations

    # Copy translations
    cp -Rf 0.8.x.tr/po sabnzbd_translations
    cd sabnzbd_translations

    # Set a more usefull username
    git config user.name "SABnzbd Automation"
    git config user.email "bugs@sabnzbd.org"

    # Add and commit
    git add -A
    git commit -m "Automatic translation update"
    git push

    # All done!
    cd ..
fi