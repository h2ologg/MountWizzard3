# from distutils.core import setup
from setuptools import setup
import platform

setup(
    name='mountwizzard',
    version='3.0a13',
    packages=[
        'mountwizzard',
        'mountwizzard.analyse',
        'mountwizzard.ascom',
        'mountwizzard.astrometry',
        'mountwizzard.automation',
        'mountwizzard.baseclasses',
        'mountwizzard.imaging',
        'mountwizzard.dome',
        'mountwizzard.environment',
        'mountwizzard.gui',
        'mountwizzard.icons',
        'mountwizzard.indi',
        'mountwizzard.modeling',
        'mountwizzard.mount',
        'mountwizzard.relays',
        'mountwizzard.remote',
        'mountwizzard.widgets'
    ],
    python_requires='~=3.5',
    install_requires=[
        'PyQt5==5.10',
        'matplotlib==2.1.2',
        'wakeonlan>=1.0.0',
        'requests==2.18.4',
        'astropy==2.0.2',
        'numpy==1.14.0',
        'requests_toolbelt==0.8.0'
    ]
    + (['pypiwin32==220'] if "Windows" == platform.system() else [])
    + (['pywinauto==0.6.4'] if "Windows" == platform.system() else [])
    + (['comtypes==1.1.1'] if "Windows" == platform.system() else [])
    ,
    url='https://pypi.python.org/pypi/mountwizzard',
    license='APL 2.0',
    author='mw',
    author_email='michael@wuertenberger.org',
    description='tooling for a 10micron mount',
)

if platform.system() == 'Linux':
    print('#############################################')
    print('### Important hint:                       ###')
    print('### you have to install PYQT5 manually    ###')
    print('### sudo apt-get install pyqt5            ###')
    print('### There might be the need to install    ###')
    print('### libfreetype6-dev manually as well     ###')
    print('### sudo apt-get install libfreetype6-dev ###')
    print('#############################################')

