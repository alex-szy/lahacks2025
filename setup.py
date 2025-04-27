from setuptools import setup

setup(
    name='munchkincli',
    version='0.1.0',
    py_modules=['munchkin'],
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'mckn = munchkin:cli',
        ],
    },
)
