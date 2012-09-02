# -*- coding: utf-8 -*-

# Without prejudice to the license governing the use of
# the Python standard module textwrap on which textwrap2 is based,
# PyHyphen is licensed under the same terms as the underlying
# `C library libhyphen <http://sourceforge.net/projects/hunspell/files/Hyphen/>`_.
# The essential parts of the license terms of libhyphen are quoted hereunder.
#
#
#
# Extract from the license information of hyphen-2.8 library
# ============================================================
#
#
#
# GPL 2.0/LGPL 2.1/MPL 1.1 tri-license
#
# Software distributed under these licenses is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the licences
# for the specific language governing rights and limitations under the licenses.
#
# The contents of this software may be used under the terms of
# the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL",



'''
hyphen - hyphenation for Python

This package contains the following items:

* class 'Hyphenator': wrapper class for libhyphen. Each instance
  uses its own hyphenation dictionary.
* 'dict_info': meta data on locally installed dictionaries
* 'load_dict_info' and 'save_dict_info': convenience functions to load and save
  meta date from and to a local file

'''

import hnj, config
import os, pickle



__all__ = ['dictools', 'Hyphenator', 'load_dict_info', 'save_dict_info']


def load_dict_info(path = config.default_dict_info_path):
    '''
    load meta data on locally installed hyphenation dictionaries and
    store it in hyphen.dict_info.
    
    'path': the path of the meta data file. It defaults to the value found in
    'hyphen.config'. The file name is hard-coded as 'hyphen_info.pickle'.
    
    return True if the meta data file has been loaded successfully, False otherwise (no IOError is raised).
    '''
    
    if os.path.exists(path + '/hyphen_dict_info.pickle'):
        with open(path + '/hyphen_dict_info.pickle', 'rb') as f:
           content = pickle.load(f)
           # Remove any pre-existing entries and ad the new ones
           while dict_info:
               e = dict_info.keys()[0]
               dict_info.pop(e)
           dict_info.update(content)
           return True
    # Meta data file does not exist
    else:
        return False



def save_dict_info(path = config.default_dict_info_path):
    '''
    save meta data from hyphen.dict_info to a file named 'hyphen_dict_info.pickle'
    
    'path': the path of the saved file; defaults to the value in 'hyphen.config'
    '''
    
    with open(path + '/hyphen_dict_info.pickle', 'wb') as f:
        pickle.dump(dict_info, f)


class Hyphenator:
    """
    Wrapper class around the class 'hnj.hyphenator_' from the C extension.
    It provides convenient access to the C library libhyphen.
    """
    
    def __init__(self, language = 'en_US', lmin = 2, rmin = 2, compound_lmin = 2,
    compound_rmin = 2,
        directory = ''):
        '''
        Return a hyphenator object initialized with a dictionary for the specified language, typically a locale name.

            Example: 'en_NZ' for English / New Zealand

        Each class instance has an attribute 'info' of type dict containing metadata on its dictionary including
        its local file path.
        If the module-level attribute dict_info
        does not contain an item for this dictionary, the info attribute of the Hyphenator instance is None.
        In this case the 'directory' argument must be set to the local
        path of the hyphenation dictionary.
        
        There is also a 'language' attribute of type str which is deprecated since v1.0b1.
        
        lmin, rmin, compound_lmin and compound_rmin: set minimum number of chars to be cut off by hyphenation in
        single or compound words
        
        '''
        
        
        if language in dict_info:
            file_path = dict_info[language].filepath
        else:
            file_path = '/'.join((directory, '/', 'hyph_' + language + '.dic'))
        self.__hyphenate__ = hnj.hyphenator_(file_path, lmin, rmin,
            compound_lmin, compound_rmin)
        self.language = language
        if language in dict_info:
            self.info = dict_info[language]
        else: self.info = None


    def pairs(self, word):
        '''
        Hyphenate a unicode string and return a list of lists of the form
        [[u'hy', u'phenation'], [u'hyphen', u'ation']].

        Return [], if len(word) < 4 or if word could not be hyphenated because
        
        * it is not encodable to the dictionary's encoding, or
        * the hyphenator could not find any hyphenation point
        '''
        if not isinstance(word, unicode): raise TypeError('Unicode object expected.')
        mode = 1
        if (len(word) < 4) or ('=' in word): return []
        if not word.islower():
            if (word.isupper()):
                mode += 4
                word = word.lower()
            else:
                if (word[1:].islower()):
                    mode += 2
                    word = word.lower()
                else: return []
        # Now call the hyphenator catching the case that 'word' is not encodable
        # to the dictionary's encoding.'
        try:
            return self.__hyphenate__.apply(word, mode)
        except UnicodeError:
            return []


    def syllables(self, word):
        '''
        Hyphenate a unicode string and return list of syllables.

        Return [], if len(word) < 4 or if word could not be hyphenated because

        * it is not encodable to the dictionary's encoding, or
        * the hyphenator could not find any hyphenation point

        Results are not consistent in case of non-standard hyphenation as a join of the syllables
        would not yield the original word.
        '''
        if not isinstance(word, unicode): raise TypeError('Unicode object expected.')
        mode = 0
        if (len(word) < 4) or ('=' in word): return []
        if not word.islower():
            if (word.isupper()):
                mode += 4
                word = word.lower()
            else:
                if (word[1:].islower()):
                    mode += 2
                    word = word.lower()
                else: return []
        # Now call the hyphenator catching the case that 'word' is not encodable
        # to the dictionary's encoding.'
        try:
            return self.__hyphenate__.apply(word, mode).split('=')
        except UnicodeError:
            return []


    def wrap(self, word, width, hyphen = '-'):
        '''
        Hyphenate 'word' and determine the best hyphenation fitting
        into 'width' characters.
        Return a list of the form [u'hypen-', u'ation']
        The '-' in the above example is the default value of 'hyphen'.
        It is added automatically and must fit
        into 'width' as well. If no hyphenation was found such that the
        shortest prefix (plus 'hyphen') fits into 'width', [] is returned.
        '''
        
        p = self.pairs(word)
        max_chars = width - len(hyphen)
        while p:
            if p[-1][0].endswith(hyphen): cur_max_chars = max_chars + 1
            else: cur_max_chars = max_chars
            if len(p[-1][0]) > cur_max_chars:
                p.pop()
            else: break
        if p:
            # Need to append a hyphen?
            if cur_max_chars == max_chars:
                p[-1][0] += hyphen
            return p[-1]
        else: return []



dict_info = {}
load_dict_info()

