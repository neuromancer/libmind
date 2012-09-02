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

import copy # for deep copying dicts

import WVectorizer
import Brain

from Bootstrap import gbootstrap

class Mind(object):

  """
   

  :version:
  :author:
  """

  spectral_radius = 0.9

  def __init__(self, inputs, outputs, fnames_texts = []):
    """
     

    @param list of Input inputs : 
    @param list of Output outputs : 
    @return  :
    @author
    """
    
    self.inputs = inputs
    self.outputs = outputs
    
    self.brain = Brain.Brain(inputs, outputs)
    self.old_inputs = dict()
    
    self.io          = dict()
    
    # TODO: populate and handle input and output only lists  
    
    self.input_only  = dict()
    self.output_only = dict()
    
    # Looking for inputs / outputs pairs
    
    for input in self.inputs:
        for output in self.outputs:
            if input.getName() == output.getName():
              # TODO: support multiple texts to bootstrap
              p = gbootstrap(input, output, fnames_texts)
              self.io[input.getName()] = input,p[0],p[1]
    
  def __process_inputs(self, inputs):
    """
     

    @param dict inputs : 
    @return dict :
    @author
    """
    pinputs = dict()
    
    if (inputs == dict()):
        return pinputs
    
    for input in self.input_only:
      
      ginput, vectorizer = self.input_only[input]
      seq = inputs[input]+ginput.stop_symbol
      vseq = ginput.input(seq)
      pinputs[input] = vectorizer.wvectorize(vseq)

      
    for input in self.io:
      
      ginput, vectorizer, _ = self.io[input]
      seq = inputs[input]+[ginput.stop_symbol]
      vseq = ginput.input(seq)
      pinputs[input] = vectorizer.wvectorize(vseq)

    return pinputs
  
  def __process_outputs(self, voutputs):
    """
     

    @param dict inputs : 
    @return dict :
    @author
    """
    
    # TODO: how to handle multiple outputs?
    poutputs = ""
    
    for output in self.output_only:
      
      goutput, unvectorizer = self.input_only[output]
      poutputs = poutputs + wunvectorizer.unvectorize(voutputs)
    
    for output in self.io:
      
      goutput, _, unvectorizer = self.io[output]
      poutputs = poutputs + unvectorizer.unvectorize(voutputs)
    
    return poutputs

  def __get_old_inputs(self, inputs):
    """
     

    @param dict inputs : 
    @return dict :
    @author
    """
    
    r = copy.deepcopy(self.old_inputs)
    
    for input in self.input_only:
      
      if not(input in self.old_inputs):
        self.old_inputs[input] = inputs[input]
      else:
        ginput, _ = self.input_only[input]
        self.old_inputs[input] += ([ginput.stop_symbol] + inputs[input]) 
    
    for input in self.io:
      
      if not(input in self.old_inputs):
        self.old_inputs[input] = inputs[input]
      else:
        ginput, _, _ = self.io[input]
        self.old_inputs[input] += ([ginput.stop_symbol] + inputs[input]) 
      
    return self.__process_inputs(r)
    

  def assimilate(self, inputs):
    """
     

    @param dict inputs : 
    @return dict :
    @author
    """
    
    old_inputs = self.__get_old_inputs(inputs)
    inputs = self.__process_inputs(inputs)
    
    y = self.brain.getAssociation(inputs)
    
    if (old_inputs <> dict()): # No previous inputs
      self.brain.setAssociation(old_inputs,inputs) 
    
    return self.__process_outputs(y)
    
  
  def stop(self, flush = False, debug = True):
    """
     

    @return :
    @author
    """
    if (flush):
        self.brain.flush(debug)
        
    self.old_inputs = dict()

  def __bootstrap(self, texts, alphabet):
    """
     

    @param list of strings texts : 
    @param string alphabet : 
    @return  :
    @author
    """
    pass
  


