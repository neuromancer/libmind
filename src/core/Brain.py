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
import numpy
import Associator

class Brain(object):

  """
   

  :version:
  :author:
  """

  def __init__(self, inputs, outputs):
    """
     

    @param list of Input inputs : 
    @param list of Output outputs : 
    @return  :
    @author
    """
    
    self.inputs = inputs
    self.outputs = outputs
    
    a_input_size  = 0
    a_output_size = 0
    
    for input in inputs:
        a_input_size = a_input_size + input.getInternalSize()
        
    for output in outputs:
        a_output_size = a_output_size + output.getInternalSize()
    
    self.associator = Associator.Associator(a_input_size, a_output_size)
    
    
  def getAssociation(self, inputs):
    """
     

    @param dict inputs : 
    @return  :
    @author
    """
    
    (input, _) = self.__handleIO(inputs, None)
    return self.associator.getAssociation(input)

  def setAssociation(self, inputs, outputs):
    
    """
     

    @param dict inputs : 
    @param dict outputs : 
    @return  :
    @author
    """
      
    (input, output) = self.__handleIO(inputs, outputs)
    
    self.associator.addToTrain(input, output)
   
  def flush(self, debug):
    
    """
     

    @param bool debug : 
    @return  :
    @author
    """
    self.associator.train(debug)
    
    

  def __handleIO(self, inputs = None, outputs = None):
    """
     
    @param dict inputs : 
    @param dict outputs : 
    @return  :
    @author
    """

    assert(inputs <> None or output <> None)
    
    input = None
    output = None
    
    # TODO: find a way to handle multiple inputs / outputs nicely
    
    if inputs <> None:
      input_list = []
      for input in self.inputs:
        input_list.append(inputs[input.getName()]) 
    
      input = numpy.concatenate(input_list)
      
      
    if outputs <> None:
      output_list = []
      for output in self.outputs:
        output_list.append(outputs[output.getName()]) 
    
      output = numpy.concatenate(output_list)
    
    return input, output
