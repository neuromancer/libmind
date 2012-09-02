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

    Copyright 2010, 2011, 2012 by neuromancer
"""

import WVectorizer
import WunVectorizer
import src.aux as aux

def gbootstrap(ginput, goutput, fnames):
    
    print "Bootstrapping", ginput.getName(), "with",
    
    if fnames == []:
      print "basic elements"
    else:
      for fname in fnames:
        print "\""+fname+"\"",
      print ""
    
    # fixed parameters
    spectral_radius = 0.9
  
    # Sequences
    seqs = []
    
    for fname in fnames:
        x = aux.load_words_from_text(fname, ginput)
        seqs.extend(x)

    if fnames == []:
        seqs = list(goutput.alphabet) # to avoid using a reference!
        seqs.remove(goutput.stop_symbol)
        
    #print seqs

    #print "words #", len(words)
    
    train_set = seqs
    #test_set  = ???
    
    to_train = []
    #to_test = []
    
    for seq in train_set:
        if "SeqWord" in ginput.getName():
          syls = ginput.getSyllables(seq)
        
          for j in range(len(syls)-1):
            to_train.append(list("".join(syls[0:j])))
            
          to_train.extend(list(syls))
          
          to_train.append(list(seq) + [ginput.stop_symbol])
        else:
          to_train.append([seq , ginput.stop_symbol])
    

    wvectorizer   = WVectorizer.WVectorizer(ginput.getSize(), ginput.getInternalSize(), spectral_radius)
    
    #to_train = list(set(to_train))
    
    #print to_train
    
    if "" in to_train:
        to_train.remove("")
        
    if [] in to_train:
        to_train.remove([])
    
    #print to_train
    to_train = map(lambda x: (x, wvectorizer.wvectorize(ginput.input(x))), to_train) 
    #to_test = map(lambda x: (x, wvectorizer.wvectorize(winput.input(x))), to_test) 
    #print to_train
    
    wunvectorizer = WunVectorizer.WunVectorizer(spectral_radius, goutput)
    wunvectorizer.train(to_train, [], True)
    #print ""

    return wvectorizer, wunvectorizer
