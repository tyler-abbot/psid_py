psid_py
====================
A python module to build PSID data sets in Python.

This module is based on the psidR package by Florian Oswald, avalable at:
https://github.com/floswald/psidR/

About
============
``psid_py`` is a package to make building panel data sets from the PSID database fast and easy.  The package includes functionality to download the raw ASCII files for you, to parse the ASCII into a dataframe, and to build a panel based on user specifications.  Specifications include subsampling from SRC, SEO, immigrant, or latino subsamples, as well as by head of household only.  Finally, the user can specify a balanced panel or a panel consisting of individuals present for a specific number of years.

Usability
=========
The package comes with a ``test.py`` file that contains typical function calls and the proper way to define inputs.

More testing is forthcoming in future distributions.


This project is released under an MIT license.
