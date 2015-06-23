"""
Origin: A file to test the psid_py package
Filename: test.py
Author: Tyler Abbot
Last modified: 23 June, 2015

This script contains test calls to the psid_py package.

"""
import psid_py

data_dir = '/home/tmabbot/Documents/data'

fam_vars = {'year': [2001, 2003],
            'house_value': ["ER17044", "ER21043"],
            'total_income': ["ER20456", "ER24099"],
            'education': ["ER20457", 'NA']}

#Simple verbose call
#panel_data = psid_py.build_panel(fam_vars, design="balanced", datadir=data_dir,
#                                 ind_vars=None, SAScii=None, heads_only=None,
#                                 sample=None, verbose=True)

#Test different panel designs
#panel_data = psid_py.build_panel(fam_vars, design=2, datadir=data_dir,
#                                 ind_vars=None, SAScii=None, heads_only=None,
#                                 sample=None, verbose=True)

#Test different subsamples
#panel_data = psid_py.build_panel(fam_vars, design='balanced', datadir=data_dir,
#                                 ind_vars=None, SAScii=None, heads_only=None,
#                                 sample='SRC', verbose=True)
#panel_data = psid_py.build_panel(fam_vars, design='balanced', datadir=data_dir,
#                                 ind_vars=None, SAScii=None, heads_only=None,
#                                 sample='SEO', verbose=True)
#panel_data = psid_py.build_panel(fam_vars, design='balanced', datadir=data_dir,
#                                 ind_vars=None, SAScii=None, heads_only=None,
#                                 sample='immigrant', verbose=True)
#panel_data = psid_py.build_panel(fam_vars, design='balanced', datadir=data_dir,
#                                 ind_vars=None, SAScii=None, heads_only=None,
#                                 sample='latino', verbose=True)

#Test Head of household
panel_data = psid_py.build_panel(fam_vars, design="balanced", datadir=data_dir,
                                 ind_vars=None, SAScii=None, heads_only=True,
                                 sample=None, verbose=True)
