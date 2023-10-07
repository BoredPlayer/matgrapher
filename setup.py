from setuptools import setup

setup(
    name='matgrapher',
    version = '0.2.6',
    description = 'An easy to use python class aiding with matplotlib graph making.',
    url = 'https://github.com/BoredPlayer/matgrapher',
    author = 'BoredPlayer',
    author_email = 'oskar.g.rpi@vp.pl',
    license = 'MIT License',
    packages = ['matgrapher'],
    install_requires = ['numpy', 'matplotlib'],
    
    classifiers=[
        'Developements Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: MIT License',
        'Programming Language :: Python :: 3'
    ]
)
