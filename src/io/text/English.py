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

import mhyphen
import src.io.Input as Input
import src.io.Output as Output
import src.aux as aux

h = mhyphen.Hyphenator(language = "en_US",
                       lmin=1, rmin=1, 
                       compound_lmin=1, 
                       compound_rmin=1, 
                       directory="src/io/text/mhyphen")

ginternalSize = 35

class InputWords (Input.Input):

  """
   

  :version:
  :author:
  """
  
  internalSize = ginternalSize

  def __init__(self):
    
    extra_letters = " .-"
    letters = "abcdefghijklmnopqrstuvwxyz"
    self.alphabet = letters + extra_letters
    self.stop_symbol = "."
    self.sep_symbol = " "
    self.max_seq = 15
    
  def preprocess(self, inp):
    inp = aux.fixcod(inp)
    inp = inp.lower()
    inp = filter(lambda c: c in self.alphabet, inp)
    return inp

  def input(self, inp):
    #inp = self.preprocess(inp)
    
    return aux.process(inp,self.alphabet)

  def getName(self):
    return "SeqWordsEn"

  def getInternalSize(self):
    return self.internalSize

  def getSize(self):
    """
     

    @return int :
    @author
    """
    return len(self.alphabet)

  def getSyllables(self,w):
    """
     

    @return list str :
    @author
    """
    
    sils = h.syllables(unicode(w))
    if sils == []:
        return map(str,[unicode(w)])
    else:
        return map(str,(sils))
    
    
class OutputWords (Output.Output):

  """
   

  :version:
  :author:
  """
  
  internalSize = ginternalSize

  def __init__(self):
    
    extra_letters = " .-"
    letters = "abcdefghijklmnopqrstuvwxyz"
    self.alphabet = letters + extra_letters
    self.stop_symbol = "."
    self.max_seq = 15

  def output(self, out):
    
    return out

  def getName(self):
    return "SeqWordsEn"

  def getInternalSize(self):
    return self.internalSize

  def getSize(self):
    """
     

    @return int :
    @author
    """
    return len(self.alphabet)
