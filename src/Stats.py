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

#import Input
#import aux
#import hyphen

class Stats:

  """
   

  :version:
  :author:
  """
  
  def __init__(self, mind):
    self.mind = mind
    self.samples_size = 0
    self.error_size = 0

  def evalSample(self, inputs, output, debug = False):
    
    prediction = self.mind.assimilate(inputs)
    self.mind.stop()
      
    if (prediction <> output):
      
      if debug:
        print list(prediction), " <> ", list(output)
      self.error_size = self.error_size + 1

    self.samples_size = self.samples_size + 1
      

  def getError(self):
    """
     

    @return float :
    @author
    """
    return float(self.error_size) / float(self.samples_size)

  def reset(self):
    """
     

    @return :
    @author
    """
    
    self.samples_size = 0
    self.error_size = 0

    
    
