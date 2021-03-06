#!/usr/bin/python -OO
# Copyright 2008-2017 The SABnzbd-Team <team@sabnzbd.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from __future__ import unicode_literals
import biplist
import os.path

import os
import sys
import re
import platform
import pkginfo


# We need to call dmgbuild from command-line, so here we can setup how
if __name__ == "__main__":
    # Check for DMGBuild
    try:
        import dmgbuild
    except:
        print 'Requires dmgbuild-module, use pip install dmgbuild'
        exit()

    # Check if signing is possible
    authority = os.environ.get('SIGNING_AUTH')
    if not authority:
        print 'No SIGNING_AUTH set! Aborting.'
        exit(1)

    # Extract version info and set DMG path
    # Create sub-folder to upload later
    os.system('mkdir dmg')
    release = pkginfo.Develop('./src/').version
    prod = 'SABnzbd-' + release
    fileDmg = os.path.join('dmg', prod + '-osx.dmg')


    # Path to app file
    apppath = 'src/dist/SABnzbd.app'

    # Copy Readme
    readmepath_old = os.path.join(apppath, 'Contents/Resources/README.mkd')
    readmepath_new = 'README.txt'
    os.system('cp -p "%s" "%s"' % (readmepath_old, readmepath_new))

    # Path to background
    backgroundpath = 'osx/image/sabnzbd_new_bg.png'

    # Mae DMG
    print 'Building DMG'
    os.system('dmgbuild -s make_dmg.py -D app="%s" -D readme="%s" -D background="%s" "%s" "%s"' % (apppath, readmepath_new, backgroundpath, prod, fileDmg))

    # Resign APP
    print 'Siging DMG'
    os.system('codesign --deep -f -i "org.sabnzbd.SABnzbd" -s "%s" "%s"' % (authority, fileDmg))
    print 'Signed!'
    exit()


### START OF DMGBUILD SETTINGS
### COPIED AND MODIFIED FROM THE EXAMPLE ONLINE
application = defines.get('app', 'AppName.app')
readme = defines.get('readme', 'ReadMe.rtf')
appname = os.path.basename(application)

def icon_from_app(app_path):
    plist_path = os.path.join(app_path, 'Contents', 'Info.plist')
    plist = biplist.readPlist(plist_path)
    icon_name = plist['CFBundleIconFile']
    icon_root,icon_ext = os.path.splitext(icon_name)
    if not icon_ext:
        icon_ext = '.icns'
    icon_name = icon_root + icon_ext
    return os.path.join(app_path, 'Contents', 'Resources', icon_name)

# .. Basics ....................................................................

# Volume format (see hdiutil create -help)
format = defines.get('format', 'UDBZ')

# Volume size (must be large enough for your files)
size = defines.get('size', '100M')

# Files to include
files = [ application, readme ]

# Symlinks to create
symlinks = { 'Applications': '/Applications' }

# Volume icon
#
# You can either define icon, in which case that icon file will be copied to the
# image, *or* you can define badge_icon, in which case the icon file you specify
# will be used to badge the system's Removable Disk icon
#
#icon = '/path/to/icon.icns'
badge_icon = icon_from_app(application)

# Where to put the icons
icon_locations = {
    readme:         (70,  160),
    appname:        (295, 220),
    'Applications': (510, 220)
}

# .. Window configuration ......................................................

# Window position in ((x, y), (w, h)) format
window_rect = ((100, 100), (660, 360))

# Background
#
# This is a STRING containing any of the following:
#
#    #3344ff          - web-style RGB color
#    #34f             - web-style RGB color, short form (#34f == #3344ff)
#    rgb(1,0,0)       - RGB color, each value is between 0 and 1
#    hsl(120,1,.5)    - HSL (hue saturation lightness) color
#    hwb(300,0,0)     - HWB (hue whiteness blackness) color
#    cmyk(0,1,0,0)    - CMYK color
#    goldenrod        - X11/SVG named color
#    builtin-arrow    - A simple built-in background with a blue arrow
#    /foo/bar/baz.png - The path to an image file
#
# Other color components may be expressed either in the range 0 to 1, or
# as percentages (e.g. 60% is equivalent to 0.6).
background = defines.get('background', 'builtin-arrow')

show_status_bar = False
show_tab_view = False
show_toolbar = False
show_pathbar = False
show_sidebar = False
sidebar_width = 0

# Select the default view; must be one of
#
#    'icon-view'
#    'list-view'
#    'column-view'
#    'coverflow'
#
default_view = 'icon-view'

# General view configuration
show_icon_preview = False

# Set these to True to force inclusion of icon/list view settings (otherwise
# we only include settings for the default view)
include_icon_view_settings = 'auto'
include_list_view_settings = 'auto'

# .. Icon view configuration ...................................................

arrange_by = None
grid_offset = (0, 0)
grid_spacing = 50
scroll_position = (0, 0)
label_pos = 'bottom' # or 'right'
text_size = 16
icon_size = 64

# .. List view configuration ...................................................

# Column names are as follows:
#
#   name
#   date-modified
#   date-created
#   date-added
#   date-last-opened
#   size
#   kind
#   label
#   version
#   comments
#
list_icon_size = 16
list_text_size = 12
list_scroll_position = (0, 0)
list_sort_by = 'name'
list_use_relative_dates = True
list_calculate_all_sizes = False,
list_columns = ('name', 'date-modified', 'size', 'kind', 'date-added')
list_column_widths = {
    'name': 300,
    'date-modified': 181,
    'date-created': 181,
    'date-added': 181,
    'date-last-opened': 181,
    'size': 97,
    'kind': 115,
    'label': 100,
    'version': 75,
    'comments': 300,
}
list_column_sort_directions = {
    'name': 'ascending',
    'date-modified': 'descending',
    'date-created': 'descending',
    'date-added': 'descending',
    'date-last-opened': 'descending',
    'size': 'descending',
    'kind': 'ascending',
    'label': 'ascending',
    'version': 'ascending',
    'comments': 'ascending',
}





