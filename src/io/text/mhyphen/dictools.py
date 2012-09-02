# PyHyphen - hyphenation for Python
# module: dictools
'''
This module contains convenience functions to manage hyphenation dictionaries.
'''

import os
import __init__ as hyphen
from __init__ import config, save_dict_info
from xml.etree.ElementTree import ElementTree
from urllib2 import urlopen, URLError

__all__ = ['install', 'is_installed', 'uninstall', 'list_installed']

class DictInfo:
    '''
    Contains metadata on a hyphenation dictionary.
    '''
    
    def __init__(self, locales, filepath, url = None):
        '''
        locales: a list of locales for for which the dictionary is suitable, e.g. 'en_UK'
        filepath: the local path including filename of the dictionary file
        url: an  optional URL where the dictionary has been downloaded from
'''

        self.filepath = filepath
        self.locales = locales
        self.url = url
        
    def __str__(self):
        return ''.join(('Hyphenation dictionary:\n', 'Locales: ', str(self.locales), '\n',
            'filepath: ', self.filepath, '\n',
            'URL: ', self.url))


def list_installed(directory = config.default_dict_path):
    '''
    Return a list of locales for which dictionaries are installed.
    Deprecated since version 2.0. Use hyphen.dict_info.keys() instead.
    'directory' is ignored since version 2.0 as 'hyphen.dict_info' can be accessed.
    '''
    return hyphen.dict_info.keys()

def is_installed(language, directory = config.default_dict_path):
    '''return True if 'directory' (default as declared in config.py)
    contains a dictionary file for 'language',
    False otherwise.
    By convention, 'language' should have the form 'll_CC'.
    Example: 'en_US' for US English.
    Since version 2.0, 'directory' is ignored as the relevant information is in found 'hyphen.dict_info'.
    '''
    return (language in hyphen.dict_info.keys())
    
    
def uninstall(language):
    '''
    Uninstall the dictionary of the specified language.
    'language': is by convention a string of the form 'll_CC' whereby ll is the
        language code and CC the country code.
    '''
    file_path = hyphen.dict_info[language].filepath
    os.remove(file_path)
    # Delete all references in dict_info to the removed file
    for d in hyphen.dict_info.keys():
        if hyphen.dict_info[d].filepath == file_path: hyphen.dict_info.pop(d)
    save_dict_info()


def install(language, directory = config.default_dict_path,
            repos = config.default_repository, use_description = True):
    '''
    Download  and install a dictionary file.
    language: a string of the form 'll_CC'. Example: 'en_US' for English, USA
    directory: the installation directory. Defaults to the
    value given in config.py. After installation this is the package root of 'hyphen'
    repos: the url of the dictionary repository. (Default: as declared in config.py;
    after installation of PyHyphen this is LibreOffice's GIT repository .).
    '''

    # Download the dictionaries.xcu file from the LibreOffice repository if needed
    if use_description:
        # first try  full language name; it won't work in all cases...
        language_ext_name = language
        descr_url = repos + language_ext_name + '/dictionaries.xcu'

        try:
            descr_file = urlopen(descr_url)
        except URLError: 
            # OK. So try with the country code.
            language_ext_name = language[:2]
            descr_url = repos + language_ext_name + '/dictionaries.xcu'
            try: 
                descr_file = urlopen(descr_url)
            except URLError:
                descr_file = None
            
    # Parse the xml file if it is present, and extract the data.     
    if   use_description and descr_file: 
        descr_tree = ElementTree(file = descr_file)


        # Find the nodes containing meta data of hyphenation dictionaries
        # Iterate over all nodes
        for node in descr_tree.getiterator('node'):
            # Check if node relates to a hyphenation dict.
            # We assume this is the case if an attribute value
            # contains the substring 'hyph'
            node_values = [i[1] for i in node.items()]
            iter_values = (i for i in node_values if ('hyph' in i.lower()))
            for v in iter_values:
                # Found one! So extract the data and construct the local record
                for property in node.getchildren():
                    prop_values = [j[1] for j in property.items()]
                    for pv in prop_values:
                        if pv.lower() == 'locations':
                            # Its only child's text is a list of strings of the form %origin%<filename>
                            # For simplicity, we only use the first filename in the list.
                            raw_dict_fn = property.getchildren()[0].text.split()[0]
                            dict_fn = raw_dict_fn[9:] # strip the prefix '%origin%'
                            dict_url = ''.join((repos, language_ext_name, '/', dict_fn))
                            break # skip any other values of this property

                        elif pv.lower() == 'locales':
                            # Its only child's text is a list of locales. .
                            dict_locales = property.getchildren()[0].text.replace('-', '_').split()

                            break # skip any other values of this property


                # Install the dictionary file
                dict_str = urlopen(dict_url).read()
                filepath = directory + '/' + dict_fn
                with open(filepath, 'wb')  as dict_file:
                    dict_file.write(dict_str)

                    # Save the metadata
                # Generate a record for each locale, overwrite any existing ones
                new_dict  = DictInfo(dict_locales, filepath, url = dict_url)
                for l in dict_locales:
                    hyphen.dict_info[l] = new_dict

    # handle the case that there is no xml metadata
    else:
        # Download the dictionary guessing its URL
        dict_fn = ''.join(('hyph_dict_', language, '.dic'))
        dict_url = ''.join((repos, dict_fn))
        dict_str = urlopen(dict_url).read()
        filepath = directory + '/' + dict_fn
        with open(filepath, 'w')  as dict_file:
            dict_file.write(dict_str)
        # Store the metadata
        new_dict = DictInfo([language], filepath) # the URL is thus set to None.
        hyphen.dict_info[language] = new_dict
    # Save the modified metadata
    save_dict_info()

