#!/usr/bin/env python3

# python setup.py sdist --format=zip,gztar

from setuptools import setup
import os
import sys
import platform
import imp
import argparse

with open('contrib/requirements/requirements.txt') as f:
    requirements = f.read().splitlines()

with open('contrib/requirements/requirements-hw.txt') as f:
    requirements_hw = f.read().splitlines()

version = imp.load_source('version', 'lib/version.py')

if sys.version_info[:3] < (3, 4, 0):
    sys.exit("Error: Electrum-bci requires Python version >= 3.4.0...")

data_files = []

if platform.system() in ['Linux', 'FreeBSD', 'DragonFly']:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root=', dest='root_path', metavar='dir', default='/')
    opts, _ = parser.parse_known_args(sys.argv[1:])
    usr_share = os.path.join(sys.prefix, "share")
    if not os.access(opts.root_path + usr_share, os.W_OK) and \
       not os.access(opts.root_path, os.W_OK):
        if 'XDG_DATA_HOME' in os.environ.keys():
            usr_share = os.environ['XDG_DATA_HOME']
        else:
            usr_share = os.path.expanduser('~/.local/share')
    data_files += [
        (os.path.join(usr_share, 'applications/'), ['electrum-bci.desktop']),
        (os.path.join(usr_share, 'pixmaps/'), ['icons/electrum-bci.png'])
    ]

setup(
    name="Electrum-bci",
    version=version.ELECTRUM_VERSION,
    install_requires=requirements,
    packages=[
        'electrum',
        'electrum_gui',
        'electrum_gui.qt',
        'electrum_plugins',
        'electrum_plugins.audio_modem',
        'electrum_plugins.hw_wallet',
        'electrum_plugins.keepkey',
        'electrum_plugins.ledger',
        'electrum_plugins.trezor',
        'electrum_plugins.virtualkeyboard',
    ],
    package_dir={
        'electrum': 'lib',
        'electrum_gui': 'gui',
        'electrum_plugins': 'plugins',
    },
    package_data={
        'electrum': [
            'servers.json',
            'servers_testnet.json',
            'servers_regtest.json',
            'currencies.json',
            'checkpoints.json',
            'www/index.html',
            'wordlist/*.txt',
            'locale/*/LC_MESSAGES/electrum.mo',
        ]
    },
    scripts=['electrum-bci'],
    data_files=data_files,
    description="Lightweight Bitcoin Interest Wallet",
    author="The Bitcoin Interest Developers",
    author_email="admin@bitcoininterest.io",
    license="MIT Licence",
    url="https://www.bitcoininterest.io/",
    long_description="""Lightweight Bitcoin Interest Wallet"""
)

# Optional modules (not required to run Electrum)
import pip
opt_modules = requirements_hw + ['pycryptodomex']
[ pip.main(['install', m]) for m in opt_modules ]
