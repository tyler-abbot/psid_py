"""A setup module for psidPy

Based on the pypa sample project.

A tool to download data and build psid panels based on psidR by Florian Oswald.

See:
https://github.com/floswald/psidR
https://github.com/tyler-abbot/psidPy
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='psid_py',
    version='1.0.0',
    description='A tool to build PSID panels.',

    # The project's main homepage
    url='https://github.com/tyler-abbot/psidPy',

    # Author details
    author='Tyler Abbot',
    author_email='tyler.abbot@sciencespo.fr',

    # Licensing information
    license='MIT',
    classifiers=[
        #How mature is this project?
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Information Analysis',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'],

    # What does your project relate to?
    keywords='statistics econometrics data',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['requests',
                      'pandas',
                      'bs4'],
)
