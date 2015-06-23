"""
Origin: A module to build psid panel data sets
Filename: psid_py.py
Author: Tyler Abbot
Last modified: 23 June, 2015

This module is based on that by Florian Oswald
(http://cran.r-project.org/web/packages/psidR/index.html).

This module contains functions build psid data sets.

"""
import zipfile
import tempfile
import shutil
import os
import sys
import re
import getpass
from os import listdir, path
from io import BytesIO

import requests
from bs4 import BeautifulSoup
import pandas as pd
import read_sas


class SampleError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def makeids():
    """
    A function that hard codes the PSID variable names.
    Returns a dictionary object containing id's and codes
    CHANGE: Returns a dataframe indexed by year.
    """
    id_list = {'year': range(1968, 1997) + range(1997, 2013, 2)}
    id_list['ind_interview'] = ["ER30001", "ER30020", "ER30043", "ER30067",
                                "ER30091", "ER30117", "ER30138", "ER30160",
                                "ER30188", "ER30217", "ER30246", "ER30283",
                                "ER30313", "ER30343", "ER30373", "ER30399",
                                "ER30429", "ER30463", "ER30498", "ER30535",
                                "ER30570", "ER30606", "ER30642", "ER30689",
                                "ER30733", "ER30806", "ER33101", "ER33201",
                                "ER33301", "ER33401", "ER33501", "ER33601",
                                "ER33701", "ER33801", "ER33901", "ER34001",
                                "ER34101"]

    id_list['ind_seq'] = ['NA', "ER30021", "ER30044", "ER30068", "ER30092",
                          "ER30118", "ER30139", "ER30161", "ER30189",
                          "ER30218", "ER30247", "ER30284", "ER30314",
                          "ER30344", "ER30374", "ER30400", "ER30430",
                          "ER30464", "ER30499", "ER30536", "ER30571",
                          "ER30607", "ER30643", "ER30690", "ER30734",
                          "ER30807", "ER33102", "ER33202", "ER33302",
                          "ER33402", "ER33502", "ER33602", "ER33702",
                          "ER33802", "ER33902", "ER34002", "ER34102"]

    # name of variable "relationship to head"
    id_list['ind_head'] = ["ER30003",
                           "ER30022",
                           "ER30045",
                           "ER30069",
                           "ER30093",
                           "ER30119",
                           "ER30140",
                           "ER30162",
                           "ER30190",
                           "ER30219",
                           "ER30248",
                           "ER30285",
                           "ER30315",
                           "ER30345",
                           "ER30375",
                           "ER30401",
                           "ER30431",
                           "ER30465",
                           "ER30500",
                           "ER30537",
                           "ER30572",
                           "ER30608",
                           "ER30644",
                           "ER30691",
                           "ER30735",
                           "ER30808",
                           "ER33103",
                           "ER33203",
                           "ER33303",
                           "ER33403",
                           "ER33503",
                           "ER33603",
                           "ER33703",
                           "ER33803",
                           "ER33903",
                           "ER34003",
                           "ER34103"]

    # numeric code for "i am the head"
    id_list['ind_head_num'] = [1 for x in range(0, 15)]\
        + [10 for x in range(0, 22)]

    id_list['fam_interview'] = ["V3", "V442", "V1102", "V1802", "V2402",
                                "V3002", "V3402", "V3802", "V4302", "V5202",
                                "V5702", "V6302", "V6902", "V7502", "V8202",
                                "V8802", "V10002", "V11102", "V12502",
                                "V13702", "V14802", "V16302", "V17702",
                                "V19002", "V20302", "V21602", "ER2002",
                                "ER5002", "ER7002", "ER10002", "ER13002",
                                "ER17002", "ER21002", "ER25002", "ER36002",
                                "ER42002", "ER47302"]
    #setkey(id.list,year)
    return pd.DataFrame(id_list, index=id_list['year'])


def get_psid(file, datadir, name, params, c):
    """
    A function to connect to the PSID website and download data.
    Uses the requests package instead of curl, as in psidR.

    Parameters
    ----------
    file    :   string
        The PSID file number.
    datadir :   string
        A temporary directory to store data
    name    :   string
        The file name to output to.
    params  :   dictionary
        The curl form. NOTE: this is untested and may need to be fixed....
    c       :   requests session object
        A requests session to post to the form.
    """
    #Create a temporary directory to store unzipped files
    temp_dir = tempfile.mkdtemp() + os.sep

    url = 'http://simba.isr.umich.edu/Zips/GetFile.aspx?file=' + file

    c.post('http://simba.isr.umich.edu/u/Login.aspx', data=params,
           headers={"Referer": "http://psidonline.isr.umich.edu/"})

    data = c.get(url, allow_redirects=False)

    #Extract all of the zipped sas and txt files
    zipped = zipfile.ZipFile(BytesIO(data.content))
    files_to_unzip = (x for x in zipped.namelist()
                      if any(['.sas' in x, '.txt' in x]))

    for NAME in files_to_unzip:
        temp_name = zipped.extract(NAME, temp_dir)
        #If you have just found the dictionary,
        if temp_name.find('.sas') >= 0:
            dict_file = str(temp_name)
        #If you have just found the data
        else:
            data_file = str(temp_name)

    #Read and process the sas file
    print('Reading in file number ' + file + '.')
    x = read_sas.read_sas(data_file, dict_file)

    #Save the data to the data directory
    x.to_csv(name + '.csv')

    #Remove the temporary directory
    #os.removedirs(temp_dir)
    shutil.rmtree(temp_dir)

    return


def year_isnt_int(YEARS):
    """A funciton to test if years are integers"""
    return any(type(x) != int for x in YEARS)


def acquire_ascii_data(years, datadir):
    """
    A function to open up a requests session and download the sas  data files.

    Parameters
    ----------
    years       :   list; a list of years to download
    datadir     :   string; the directory to store output

    """
    print('WARNING: You have chosen to download the raw ASCII. \n')
    #Check if the user is aware of the time constraint
    if sys.version_info < (3, 0):
        confirm = raw_input("This can take several hours or even days to "
                            + "download.\nAre you sure you would like to "
                            + "continue? (yes or no): ")
    else:
        confirm = input("This can take several hours or even days to "
                        + "download.\nAre you sure you would like to "
                        + "continue? (yes or no): ")
    print('\n')
    if confirm == 'yes':
        #Read in the username and passwork for PSID
        if sys.version_info < (3, 0):
            USERNAME = raw_input("Please enter your PSID username: ")
            PASSWORD = getpass.getpass("Please enter your PSID"
                                       + " password: ")
        else:
            USERNAME = input("Please enter your PSID username: ")
            PASSWORD = getpass.getpass("Please enter your PSID"
                                       + " password: ")
        print('\n')

        #Create a requests session
        c = requests.Session()

        URL = 'http://simba.isr.umich.edu/u/login.aspx'
        #USERNAME = 'tyler.abbot@sciencespo.fr'
        #PASSWORD = 'tyler.abbot'

        #Get the html once to retrieve form variables
        page = c.get(URL)

        #Use the beautifulsoup package to scrape for form variables
        soup = BeautifulSoup(page.content)
        viewstate = soup.findAll("input", {"type": "hidden",
                                 "name": "__VIEWSTATE"})
        radscript = soup.findAll("input", {"type": "hidden",
                                 "name": "RadScriptManager1_TSM"})
        #eventtarget = soup.findAll("input", {"type": "hidden",
        #                           "name": "__EVENTTARGET"})
        #eventargument = soup.findAll("input", {"type": "hidden",
        #                             "name": " __EVENTARGUMENT"})
        viewstategenerator = soup.findAll("input", {"type": "hidden",
                                          "name": "__VIEWSTATEGENERATOR"})
        eventvalidation = soup.findAll("input", {"type": "hidden",
                                       "name": "__EVENTVALIDATION"})
        radscript = soup.findAll("input", {"type": "hidden", "name":
                                 "RadScriptManager1_TSM"})

        #Gather form data into a single dictionary
        params = {'RadScriptManager1_TSM': radscript[0]['value'],
                  '__EVENTTARGET': '',
                  ' __EVENTARGUMENT': '',
                  '__VIEWSTATE': viewstate[0]['value'],
                  '__VIEWSTATEGENERATOR': viewstategenerator[0]['value'],
                  '__EVENTVALIDATION': eventvalidation[0]['value'],
                  'ctl00$ContentPlaceHolder1$Login1$UserName': USERNAME,
                  'ctl00$ContentPlaceHolder1$Login1$Password': PASSWORD,
                  'ctl00$ContentPlaceHolder1$Login1$LoginButton': 'Log In',
                  'ctl00_RadWindowManager1_ClientState': ''}

        #Generate index objects for loop
        family = {'year': range(1968, 1997) + range(1997, 2013, 2),
                  'file': [1056] + range(1058, 1083) + range(1047, 1052) +
                  [1040, 1052, 1132, 1139, 1152, 1156]}
        psidFiles = {'year': [year for year in years if year in
                     family['year']] + [2011], 'file':
                     [family['file'][family['year'].index(year)] for year
                      in years if year in family['year']] + [1053]}

        #Download all the necessary files
        for i in range(0, len(psidFiles['file']) - 1):
            get_psid(str(psidFiles['file'][i]), datadir, name=datadir +
                     'FAM' + str(psidFiles['year'][i]) + 'ER',
                     params=params, c=c)

        get_psid(str(psidFiles['file'][-1]), datadir, name=datadir
                 + 'IND' + str(psidFiles['year'][-1]) + 'ER',
                 params=params, c=c)

        print('Finished downloading files to ' + datadir
              + '.  Continuing to build the data set.')
    elif confirm == 'no':
        pass
    return


def load_data(datadir, files, years, ftype, verbose):
    """
    A function to load the data files.

    Parameters
    ----------
    datadir     :   string; directory containing data files
    files       :   list; data file names
    years       :   list; years desired
    ftype       :   string; indicates type of data file
    verbose     :   bool; verbose output

    """
    if verbose:
        print('psid_py: loading data.\n')
    if ftype == 'stata':
        #Gather the names of all family data files. case insensitive
        #Simultaneously check that the year is in the requested files
        fam_dat = [datadir + f for f in files if 'fam' in f.lower()
                   and int(re.findall("[-+]?\d+[\.]?\d*", f)[0][:-1]) in years]

        #Convert fam_dat to dataframe indexed by year
        fam_dat = pd.DataFrame(fam_dat, index=years)

        #Gather the individual file and check for multiplicity
        tmp = [datadir + f for f in files if 'ind' in f.lower()]
        if len(tmp) > 1:
            print('WARNING: You have too many individual files.'
                  'I will take only the last one in the file: '
                  + tmp[-1])
            ind_file = datadir + tmp[-1]
        else:
            ind_file = tmp[0]

        #Read in the individual data file to dataframe
        ind = pd.read_stata(ind_file)
        #NOTE: in psidR he then converts to data table... not sure why
    elif ftype == 'Rdata':
        print('Sorry!  For now this has not been implemented.')
    elif ftype == 'csv':
        #Gather the names of all family data files. case insensitive
        #Simultaneously check that the year is in the requested files
        fam_dat = [datadir + f for f in files if 'fam' in f.lower()
                   and int(re.findall("[-+]?\d+[\.]?\d*", f)[0]) in years]

        #Sort the list by year
        fam_dat = sorted(fam_dat, key=lambda x: x[-10:-6])

        #Convert fam_dat to dataframe indexed by year
        fam_dat = pd.DataFrame(fam_dat, index=years, columns=['fam_file'])

        #Gather the individual file and check for multiplicity
        tmp = [datadir + f for f in files if 'ind' in f.lower()]
        if len(tmp) > 1:
            print('WARNING: You have too many individual files.'
                  'I will take only the last one in the file: '
                  + tmp[len(tmp) - 1])
            ind_file = datadir + tmp[-1]
        else:
            ind_file = [datadir + f for f in files if 'ind' in f.lower()][0]

        #Read in the csv files to dataframe
        ind = pd.read_csv(ind_file)
    elif ftype == 'HDF5':
        print('Sorry! For now this has not been implemented.')

    if verbose:
        print('Loaded individual file: ' + ind_file)
        print('Total memory used in MB: '
              + str((ind.values.nbytes + ind.index.nbytes)/10**6))

    return (fam_dat, ind)


def sub_sampling(yind, ind_vars, YEAR, sample, verbose):
    """
    A function to seperate the requested subsample.

    Parameters
    ----------
    yind        :   dataframe; the current years data
    ind_vars    :   dataframe; desired individual variables
    YEAR        :   int; current year
    sample      :   string; the type of subsampling
    verbose     :   bool; verbose output

    """
    #Seperate latino/immigrant and general samples
    if sample == 'SRC':
        #Check number of individuals
        n = yind.shape[0]
        yind = yind.query('ER30001 < 3000').copy(deep=True)
        if verbose:
            print('The full ' + str(YEAR) + ' sample has '
                  + str(n) + ' observations.')
            print('The SRC subsample you selected has %s' % yind.shape[0]
                  + ' observations.')
    elif sample == 'SEO':
        #Check number of individuals
        n = yind.shape[0]
        yind = yind.query('ER30001 < 7000 and ER30001 > 5000').copy(deep=True)
        if verbose:
            print('The full ' + str(YEAR) + ' sample has :'
                  + str(n) + 'observations.')
            print('The SEO subsample you selected has %s' % yind.shape[0]
                  + ' observations.')
    elif sample == 'immigrant':
        #Check number of individuals
        n = yind.shape[0]
        yind = yind.query('ER30001 < 5000 and ER30001 > 3000').copy(deep=True)
        if verbose:
            print('The full ' + str(YEAR) + ' sample has '
                  + str(n) + ' observations.')
            print('The immigrant subsample you selected has %s' % yind.shape[0]
                  + ' observations.')
    elif sample == 'latino':
        #NOTE: The latino sample is only for 1990 to 1995
        if YEAR < 1990 or YEAR > 1995:
            raise SampleError('You have requested the latino sample outside of'
                              ' years for which it is available.  Please check'
                              ' whether the data you are requesting exist and '
                              'try again.')
        #Check number of individuals
        n = yind.shape[0]
        yind = yind.query('ER30001 < 9309 and ER30001 > 7000').copy(deep=True)
        if verbose:
            print('The full ' + str(YEAR) + ' sample has '
                  + str(n) + ' observations.')
            print('The latino subsample you selected has %s' % yind.shape[0]
                  + ' observations.')
            print(yind.describe())

    return yind


def head_of_house(yind, current, verbose):
    """
    A function to seperate out only heads of household.

    Parameters
    ----------
    yind        :   dataframe; the current years data
    current     :   dataframe; the variable names for current year
    verbose     :   bool; verbose output

    """
    #Generate two matrices of dummies
    A = pd.get_dummies(yind[current['ind_head']])
    B = pd.get_dummies(yind[current['ind_seq']])

    #Generate an indicator for head of household by pairwise
    #multiply of the two dummies
    yind['headyes'] = A[current['ind_head_num']]*B[1.0]
    yind = yind.query('headyes == 1')
    if verbose:
        print('Dropping non-current heads of household leaves '
              + str(yind.shape[0]) + ' observations.')
    yind = yind.drop('headyes', axis=1)
    return yind


def build_panel(fam_vars, design="balanced", datadir=None, ind_vars=None,
                SAScii=None, heads_only=None, sample=None, verbose=False):
    """
    A function to build panel data sets from the PSID.

    Parameters
    ----------
    fam_vars        :   dict of list
        A dictionary of lists containing variable names and values.  These
        are the variables from the family file and you must specify all
        varibales you would like.  It would be nice in the future to modify
        this so it looks up what the variable names are... but that's for
        the future.
        ex: fam_vars = {'year': [2001, 2003],
                        'house_value': ["ER17044", "ER21043"],
                        'total_income': ["ER20456", "ER24099"],
                        'education': ["ER20457", 'NA']}
    design          :   string or integer
        Determines which individuals to include.  Accepted inputs are
            'balanced' => Include only individuals with observations in each
                          wave.
            'all'      => Include all individuals.
            integer    => Indicates a minimum number of years of participation.
    datadir         :   string
        Either 'None' or a given directory.  In the case of 'None',
        saves output into the dir containing input files.
    ind_vars        :   dict of list
        A dictionary of lists containing variable names and values.  ***In
        most cases this will indicate the survey weights to use.  Do not
        include id variables ER30001 and ER30002.***
        ex: ind_vars = {'year': [2001, 2003],
                        'longitud_wgt': ["ER33637", "ER33740"]}
    SAScii          :   boolean
        A true/false boolean determining whether to directly download the
        ASCII file.  This can take a long time.
    heads_only      :   boolean
        Indicates inclusion of current household head only or not.
    sample          :   boolean
        Indicates which sub-sample to select.
            'None'     => No subsampling
            'SRC'      =>
            'SEO'      => Survey for economic opportunity.
            'immigrant'=> Immigrant sample.
            'latino'   => Latino family sample.
    verbose         :   boolean
        True gives verbose output.

    """
    #Test if any of the year is not the proper d-type
    if year_isnt_int(fam_vars['year']):
        print("ERROR: The year must be entered as an integer.")
        return
    years = fam_vars['year']

    #Check the directory seperator used on the current system
    s = os.sep

    #If ind_vars is empty, add a year
    if not ind_vars:
        ind_vars = {'year': years}

    #Convert fam_vars and ind_vars to dataframes for simplicity
    #NOTE: setting index for ind_vars even when empty to avoid error
    fam_vars = pd.DataFrame(fam_vars, index=years)
    ind_vars = pd.DataFrame(ind_vars, index=years)

    #If no directory is specified, use a temporary one
    if datadir is None:
        datadir = tempfile.mkdtemp() + s
    elif datadir[-1] != s:
        datadir += s

    #Acquire data
    if SAScii:
        acquire_ascii_data(years, datadir)

    #Given a set of data, either downloaded by psidPy or user supplied
    #Check the data types in the directory
    files = [f for f in listdir(datadir) if path.isfile(datadir + f)]
    if len(files) == 0:
        print('ERROR: (build_panel) The datadir is empty.'
              + '  Please check the path and try again.')
        return

    #NOTE: All files must be of the same file type
    for i in range(0, len(files)):
        if files[i].endswith('.dta'):
            ftype = 'stata'
            break
        if files[i].endswith('.rda'):
            ftype = 'Rdata'
            break
        if files[i].endswith('.RData'):
            ftype = 'Rdata'
            break
        if files[i].endswith('.csv'):
            ftype = 'csv'
            break
        if files[i].endswith('.hdf'):
            ftype = 'HDF5'
            break

    #Load data
    fam_dat, ind = load_data(datadir, files, years, ftype, verbose)

    #Generate dictionary object to fill with data frames
    datas = {}

    #Retrieve a dictionary of ids
    ids = makeids()
    if verbose:
        print('\nThe following are the hardcoded PSID variables:')
        print(ids)

    #Add a family interview variable for the requested year
    fam_vars['interview'] = ids.loc[fam_vars['year'], 'fam_interview']

    #Loop over years cleaning the data
    for YEAR in years:
        if verbose:
            print('...........................................')
            print('Currently working on data for year ' + str(YEAR))

        #Subsetting ... not clear yet what this is for.
        current = ids.loc[YEAR]
        ind_subset = [current.ind_interview, current.ind_seq,
                      current.ind_head]
        DEF_subset = ["ER30001", "ER30002"]

        #Generate the current year's sample #NOTE: this needs testing
        yind = ind[DEF_subset + list(set(ind_subset +
                   list(ind_vars.loc[YEAR].drop('year'))))]\
            .copy(deep=True)

        if sample is not None:
            #Seperate the desired subsample
            yind = sub_sampling(yind, ind_vars, YEAR, sample, verbose)

        #Select for head of household only
        if heads_only:
            yind = head_of_house(yind, current, verbose)

        #Reset column names
        yind.columns = ['ID1968', 'pernum', 'interview', 'sequence',
                        'relation_head'] + list(ind_vars.columns[:-1])
        #Calculate a unique person identifier
        yind['pid'] = yind['ID1968']*1000 + yind['pernum']

        #Set the index as the interview number
        yind.index = yind['interview']

        #Load family files and subset them
        if ftype == 'stata':
            tmp = pd.read_stata(fam_dat.loc[YEAR][0])
        elif ftype == 'Rdata':
            print('I dont know how you got this far, but this is not yet'
                  + ' implemented!')
        elif ftype == 'csv':
            tmp = pd.read_csv(fam_dat.loc[YEAR][0])
        elif ftype == 'HDF5':
            print('I dont know how you got this far, but this is not yet'
                  + ' implemented!')

        if verbose:
            print('Loaded family file: ' + str(fam_dat.loc[YEAR][0]))
            print('Current memory usage in MB: ' + str((tmp.values.nbytes
                  + tmp.index.nbytes)/10**6))
        #Create a set of variable names for the current year
        curvar = fam_vars.loc[YEAR].drop('year')

        #Convert column names to lower case
        tmp.columns = map(str.lower, tmp.columns)
        curvar.index = map(str.lower, curvar.index)

        #Test if contains NA and if so fix it!
        if 'NA' in curvar.values:
            #Return the variable that is NA
            na = curvar.index[[x for x in range(len(curvar.values))
                               if curvar.values[x] == 'NA']]

            #Drop the na variables
            temp_var = curvar.drop(na[0])

            #Copyt the required columns
            tmp = tmp[temp_var.str.lower()]

            #Name the columns
            tmp.columns = temp_var.index

            #Replace the na variable with 'NA'
            tmp[na[0]] = 'NA'
        else:
            tmp = tmp[curvar.str.lower()]

            #Set the index and column names for merging
            tmp.columns = curvar.index

        #Merge datasets
        m = pd.merge(tmp, yind, on='interview')
        m['year'] = YEAR

        #Remove nonrepspondents for a given year
        idx = [x for x in range(len(fam_vars.loc[YEAR][curvar]))
               if fam_vars.loc[YEAR][curvar][x] != 'NA'][0]

        m['isna'] = pd.get_dummies(m[curvar.index[idx].lower()],
                                   dummy_na=True)[float('nan')]
        m = m.loc[m.isna == 0].drop('isna', axis=1)

        #Place the year's dataframe into a dictionary
        datas[YEAR] = m.copy(deep=True)
        print(datas[YEAR].shape)

    #Generate a single data frame from the datas dict
    data2 = pd.DataFrame()
    for df in datas.itervalues():
        data2 = pd.concat([data2, df])

    #Generate a variable for how many years the agent is present
    data2['present'] = data2[['year', 'pid']]\
        .groupby(['pid']).transform('count')

    #Work on design of the study
    if design == 'balanced':
        n = data2.shape[0]
        print(max(data2['present']))
        data2 = data2[data2['present'] ==
                      max(data2['present'])].copy(deep=True)
        if verbose:
            print("\nBalanced panel reduces sample"
                  " from %s to %s" % (n, data2.shape[0]))
    elif str(design).isdigit():
        n = data2.shape[0]
        data2 = data2[data2['present'] >= design].copy(deep=True)
        if verbose:
            print("\nDesign choice reduces sample"
                  " from %s to %s observations" % (n, data2.shape[0]))
    elif design == 'all':
        pass

    if verbose:
        print('\n\nEnd of build_panel\n\n')
        print('====================')

    return data2
