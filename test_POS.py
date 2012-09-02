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

import src.io.text.English as English
import src.core.Mind as Mind
import src.Stats as Stats
from src.aux import load_words_from_text

# mind initilization

winput = English.InputWords()
woutput = English.OutputWords()

mind = Mind.Mind([winput], [woutput], ["data/pos/categories.txt"])

cats_files = load_words_from_text("data/pos/categories.longer.txt", winput)
cats = load_words_from_text("data/pos/categories.txt", winput)

stats = Stats.Stats(mind)

# mind training

for (cat,cat_file) in zip(cats,cats_files):
    
  print "Assimilating", cat_file+"s.."
  
  words = load_words_from_text("data/pos/"+cat_file+"s_train.txt", winput)
  cat_inputs = dict( SeqWordsEn = list(cat)) 

  for word in words:
     word_inputs = dict( SeqWordsEn = list(word))
     mind.assimilate(word_inputs)
     mind.assimilate(cat_inputs)
     mind.stop()
     
# mind flushing trains several regression models to predict future data
     
mind.stop(flush = True)

# mind testing

for (cat,cat_file) in zip(cats,cats_files):
    
  
  words = load_words_from_text("data/pos/"+cat_file+"s_test.txt", winput)
  cat_inputs = dict( InputWordsEn = list(cat)) 

  for word in words:
    word_inputs = dict( SeqWordsEn = list(word))
    stats.evalSample(word_inputs, cat, False)
     
print "Final error -> ", stats.getError()

# TODO: Move to TUI.py

#while True:
#    print ">",
#    try:
#        words = raw_input()
#    except EOFError:
#        break
#    word_inputs = dict( InputWordsEn = words)
#    print mind.assimilate(word_inputs)
#    mind.stop()

