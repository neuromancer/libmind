"""
    This file is part of reserbot.

    reserbot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    reserbot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with reserbot.  If not, see <http://www.gnu.org/licenses/>.

    Copyright 2010 neuromancer
"""


# IO functions

import unicodedata

def fixcod(txt, codif='utf-8'):
    return unicodedata.normalize('NFKD', txt.decode(codif)).encode('ASCII','ignore')

def load_sentences_from_text(fname,winput,alt_stop_symbol):
        
        stop_symbol = winput.stop_symbol
        sep_symbol = winput.sep_symbol
        texto = open(fname).read()
        texto = texto.replace(alt_stop_symbol,stop_symbol)
        
        return texto.split(stop_symbol)

def load_words_from_text(fname,winput,alt_stop_symbol = "\n"):

        stop_symbol = winput.stop_symbol
        sep_symbol = winput.sep_symbol
        sentences = load_sentences_from_text(fname,winput, alt_stop_symbol)
        all_words = []

        for sentence in sentences:
            if sentence <> "":
                    words = sentence.lstrip(sep_symbol).rstrip(sep_symbol).split(sep_symbol)
                    words = map(winput.preprocess, words)
                    words = filter(lambda x: x <> "", words)    
                    all_words.extend(words)
        
        return all_words


from numpy import *

def normalize(x):    
    n = linalg.norm(x)
    return x/n

def list2vec(c,alphabet):
    try: 
        f = alphabet.index(c)
    except ValueError:
        f = -1
        print "#Warning \'",c,"\' is out of the alphabet \"",alphabet,"\""
        assert(False)
        
    r = repeat(0,len(alphabet))
    if (f>=0):
        r[f] = 1
    return r

def process(input,alphabet):
    x = zeros((len(input),len(alphabet)))
    for i in xrange(len(input)):
        x[i] = list2vec(input[i], alphabet)
    
    return x

identity = lambda x:x

concat = lambda l: reduce(lambda x,y: x+y, l, [])
