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

import Output
import aux

class OutputWords (Output.Output):

  """
   

  :version:
  :author:
  """
  
  internalSize = 10

  def __init__(self):
    
    extra_letters = " .-"
    letters = "abcdefghijklmnopqrstuvwxyz"
    self.alphabet = letters + extra_letters
    self.stop_symbol = "."
    self.max_letters = 15
    

  def output(self, out):
    

    return out

  def getName(self):
    return "OutputWordsEs"

  def getInternalSize(self):
    return self.internalSize

  def getSize(self):
    """
     

    @return int :
    @author
    """
    return len(self.alphabet)

