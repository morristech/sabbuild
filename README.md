SABBuilder
==========
# :warning: NOT INTENDED FOR END-USERS :warning:
This repository is used to build and package releases of SABnzbd using TravisCI (macOS) and AppVeyor (Windows). Releases will be pushed as drafts to this repository, after which they can be moved to the main `sabnzbd` repo.


# How to's

- Add `[skip translations]` to the commit message to skip adding the new texts to the `sabnzbd` repo.

# For future development:

- Investigate which files should or shouldn't be included in the repo, such as installers etc.

## macOS build (Travis)

- In order to get `codesign` to work you need to login to your Apple Developer account, create a new `OSX production certificate` which will make you create a certificate signing request on a Mac.
After the certificate is generated you need to import that certificate on the Mac. Then you can export the key-certificate pair by right-clicking on it in the Keychain manager. This `p12` file is what you will need.
- This file should NEVER be published, you need to use `travis encrypt-file --add` to create a version to commit.
WARNING: encrypted files generated with `travis encrypt-file` on Windows do not work!
- Using `openssl` for file-encrypting sucks, used encrypted `.rar` because it kept failing.
- All `.sh` files need to have `0755` permissions to run on Travis.
- Certificate verification for SSH will fail because you cannot say `yes`, so need to be disabled on a per-host basis.
- All `~/.ssh/` files need to have only user-read permissions.
- Don't forget to add private-keys to Launchpad and GitHub if ever changed.

## Windows build

- Changes to `PATH` don't transfer correctly to the virtualenv's so have to be set after starting them, this could be improved.
