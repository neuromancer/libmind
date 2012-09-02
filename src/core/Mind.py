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
    #self.winput = None
    #self.woutput = None
    
    self.brain = Brain.Brain(inputs, outputs)
    #self.brain.flush(False)
    #self.to_associate = []
    self.old_inputs = dict()
    
    self.io          = dict()
    self.input_only  = dict()
    self.output_only = dict()
    
    # Looking for inputs / outputs pairs
    
    for input in self.inputs:
        for output in self.outputs:
            if input.getName() == output.getName():
              # TODO: support multiple texts to bootstrap
              p = gbootstrap(input, output, fnames_texts)
              self.io[input.getName()] = input,p[0],p[1]
    
    # Looking for linguistic inputs / outputs   
 
    #for input in self.inputs:
    #  if "SeqWord" in input.getName():
    #    self.winput = input

    #for output in self.outputs:
    #  if "SeqWord" in output.getName():
    #    self.woutput = output
    
    #assert(len(self.inout) == 1)
    
    #ioinput  = filter(lambda i: i.getName() in self.inout, self.inputs )[0]
    #iooutput = filter(lambda o: o.getName() in self.inout, self.outputs)[0]
    
    #self.vectorizer, self.unvectorizer = gbootstrap(ioinput, iooutput, fnames_texts)    

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
    #print voutputs
    poutputs = ""
    
    for output in self.output_only:
      
      goutput, unvectorizer = self.input_only[output]
      poutputs = poutputs + wunvectorizer.unvectorize(voutputs)
      #poutputs = poutputs + "\n"
    
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
    
    #if "SeqCatLogic" in r:
    #  print r["SeqCatLogic"], "->",  
    #else:
    #  print [], "->",
    
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
      
    
    #if "SeqCatLogic" in r:
    #  print r["SeqCatLogic"], "->",  
    #else:
    #  print [], "->",
      
    return self.__process_inputs(r)
    

  def assimilate(self, inputs):
    """
     

    @param dict inputs : 
    @return dict :
    @author
    """
    
    # old_words = ""
    # stop_symbol = self.winput.stop_symbol
    # winput_name = self.winput.getName()
    # woutput_name = self.woutput.getName()
    
    # # old inputs
    # for old_inputs in self.to_associate:
    #     old_words = old_words+old_inputs[winput_name]+stop_symbol
    
    # if self.to_associate <> []:
    #     old_vwords = self.winput.input(old_words)
    #     old_vwords = self.wvectorizer.wvectorize(old_vwords)
            
    
    # # current inputs
    # words = inputs[winput_name]+stop_symbol
    # vwords = self.winput.input(words)
    # vwords = self.wvectorizer.wvectorize(vwords)
    
    # if self.to_associate <> []:
        
    #     old_inputs =  dict([ (winput_name , old_vwords) ])
    #     outputs    = dict([ (woutput_name, vwords    ) ])
    #     self.brain.setAssociation(old_inputs,outputs)
    
    # self.to_associate.append(inputs)
        
    # inputs = dict([ (winput_name, vwords) ])
    #print inputs
    
    old_inputs = self.__get_old_inputs(inputs)
    #print inputs["SeqCatLogic"]
    inputs = self.__process_inputs(inputs)
    
    #print inputs
    
    y = self.brain.getAssociation(inputs)
    
    #print y
    
    if (old_inputs <> dict()):
      self.brain.setAssociation(old_inputs,inputs) 
    
    #print y
    
    return self.__process_outputs(y)
    
    # TODO: Clean up!
    #words = inputs[winput_name] 
    
    #print "Original words:", words
    #vwords = self.winput.input(words)
    
    #vwords = self.wvectorizer.wvectorize(vwords)
    #print "Vectorized words:"
    #print vwords
    
    #inputs = dict()
    #inputs[winput_name] = vwords
    
    #print "Random association:"
    #y = self.brain.getAssociation(inputs)
    #return self.wunvectorizer.unvectorize(y)
    #print y
    #return y
    
    #print "Test pronunciation:", self.wunvectorizer.unvectorize(vwords)
    
    #for input in self.inputs:
    #  
    #  print input.input(inputs[input.getName()])
  
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
  


