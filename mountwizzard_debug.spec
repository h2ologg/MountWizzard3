############################################################
# -*- coding: utf-8 -*-
#
#       #   #  #   #   #  ####
#      ##  ##  #  ##  #     #
#     # # # #  # # # #     ###
#    #  ##  #  ##  ##        #
#   #   #   #  #   #     ####
#
# Python-based Tool for interaction with the 10micron mounts
# GUI with PyQT5 for python
# Python  v3.6.7
#
# Michael Würtenberger
# (c) 2016, 2017, 2018
#
# Licence APL2.0
#
###########################################################
# standard libraries
import os
import sys
# external packages
import astropy
# local import
# remove TK
sys.modules['FixTk'] = None

# define paths
DISTPATH = '../dist'
WORKPATH = '../build'
astropy_path, = astropy.__path__

block_cipher = None
pythonPath = '/Users/astro/Envs/mw3-32/Lib'
sitePack = pythonPath + '/site-packages'
distDir = '/Users/astro/PycharmProjects/MountWizzard3/dist'
packageDir = '/Users/astro/PycharmProjects/MountWizzard3/mountwizzard3'
importDir = '/Users/astro/PycharmProjects/MountWizzard3'

a = Analysis(['mountwizzard3/mountwizzard3.py'],
    pathex=[packageDir],
    binaries=[
        ],
    datas=[(astropy_path, 'astropy'),
        ],
    hiddenimports=['shelve', 'numpy.lib.recfunctions',
        ],
    hookspath=[],
    runtime_hooks=[],
    excludes=['FixTk', 'tcl', 'tk', '_tkinter', 'tkinter', 'Tkinter',
              'astropy',
        ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    )

# remove thing to reduce size and number of files in package (have to be extracted)
a.binaries = [x for x in a.binaries if not x[0].startswith('mpl-data/sample_data')]
a.binaries = [x for x in a.binaries if not x[0].startswith('mpl-data/fonts')]
a.binaries = [x for x in a.binaries if not x[0].startswith('PyQt5/Qt/translations')]
a.binaries = [x for x in a.binaries if not x[0].startswith('QtQuick')]
a.binaries = [x for x in a.binaries if not x[0].startswith('QtQml')]
a.binaries = [x for x in a.binaries if not x[0].startswith('astropy/analytic_functions')]
a.binaries = [x for x in a.binaries if not x[0].startswith('astropy/config.tests')]
a.binaries = [x for x in a.binaries if not x[0].startswith('astropy/constants.tests')]
a.binaries = [x for x in a.binaries if not x[0].startswith('astropy/convolution')]
a.binaries = [x for x in a.binaries if not x[0].startswith('astropy/cosmology')]
a.binaries = [x for x in a.binaries if not x[0].startswith('astropy/samp')]
a.binaries = [x for x in a.binaries if not x[0].startswith('astropy/modeling')]
a.binaries = [x for x in a.binaries if not x[0].startswith('astropy/table')]
a.binaries = [x for x in a.binaries if not x[0].startswith('astropy/vo')]

# same to datas
a.datas = [x for x in a.datas if not x[0].startswith('mpl-data/sample_data')]
a.datas = [x for x in a.datas if not x[0].startswith('mpl-data/fonts')]
a.datas = [x for x in a.datas if not x[0].startswith('PyQt5/Qt/translations')]
a.datas = [x for x in a.datas if not x[0].startswith('QtQuick')]
a.datas = [x for x in a.datas if not x[0].startswith('QtQml')]
a.datas = [x for x in a.datas if not x[0].startswith('astropy/analytic_functions')]
a.datas = [x for x in a.datas if not x[0].startswith('astropy/config.tests')]
a.datas = [x for x in a.datas if not x[0].startswith('astropy/constants.tests')]
a.datas = [x for x in a.datas if not x[0].startswith('astropy/convolution')]
a.datas = [x for x in a.datas if not x[0].startswith('astropy/cosmology')]
a.datas = [x for x in a.datas if not x[0].startswith('astropy/samp')]
a.datas = [x for x in a.datas if not x[0].startswith('astropy/modeling')]
a.datas = [x for x in a.datas if not x[0].startswith('astropy/table')]
a.datas = [x for x in a.datas if not x[0].startswith('astropy/vo')]


pyz = PYZ(a.pure,
          a.zipped_data,
          cipher=block_cipher,
          )

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='MountWizzard3debug',
          debug=True,
          strip=False,
          upx=False,
          console=True,
          icon='./mountwizzard3/icons/mw.ico',
          )

#
# we have to prepare the build as there is an error when overwriting it
# if file present, we have to delete python3 --version
#

sys.path.append(importDir)
from mountwizzard3.build.build import BUILD
BUILD_NO = BUILD.BUILD_NO_FILE

buildFile = distDir + '/MountWizzard3debug.exe'
buildFileNumber = distDir + '/mountwizzard3debug-' + BUILD_NO + '.exe'

print(BUILD_NO)

app = BUNDLE(exe,
             name='MountWizzard3debug.exe',
             version=3,
             icon='./mountwizzard3/icons/mw.ico',
             bundle_identifier=None)

#
# we have to prepare the build as there is an error when overwriting it
# if file present, we have to delete it
#

if os.path.isfile(buildFileNumber):
    os.remove(buildFileNumber)
    print('removed existing app bundle with version number')

os.rename(buildFile, buildFileNumber)
