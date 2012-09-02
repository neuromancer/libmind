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

import src.io.Input as Input
import src.io.Output as Output
import src.aux as aux

ginternalSize = 15

class InputCats (Input.Input):

  """
   

  :version:
  :author:
  """
  
  internalSize = ginternalSize

  def __init__(self, elements, name = "", sep_symbol = " ", stop_symbol = "\0"):
    
    self.name = name
    self.stop_symbol = stop_symbol
    self.sep_symbol = sep_symbol
    
    elements = list(set(elements))
    
    # Basic checks
    assert(not(self.stop_symbol in elements))
    assert(not(self.sep_symbol in elements))
    
    self.alphabet = elements + [self.stop_symbol]
    
  def preprocess(self, inp):
    
    assert(inp in self.alphabet)
    return inp

  def input(self, inp):
    
    #inp = self.preprocess(inp)
    return aux.process(inp,self.alphabet)

  def getName(self):
    return "SeqCat" + self.name

  def getInternalSize(self):
    return self.internalSize

  def getSize(self):
    """
     

    @return int :
    @author
    """
    return len(self.alphabet)
    
    
class OutputCats (Output.Output):

  """
   

  :version:
  :author:
  """
  
  internalSize = ginternalSize

  def __init__(self, elements, name = "", sep_symbol = " ", stop_symbol = "\0"):
    
    self.name = name
    self.stop_symbol = stop_symbol
    self.sep_symbol = sep_symbol
    
    elements = list(set(elements))
    
    # Basic checks
    assert(not(self.stop_symbol in elements))
    assert(not(self.sep_symbol in elements))
    
    self.alphabet = elements + [self.stop_symbol]
    
    self.max_seq = 1

  def output(self, out):
    
    return out

  def getName(self):
    return "SeqCat" + self.name

  def getInternalSize(self):
    return self.internalSize

  def getSize(self):
    """
     

    @return int :
    @author
    """
    return len(self.alphabet)
