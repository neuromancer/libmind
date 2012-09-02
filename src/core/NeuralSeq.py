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

import random
import numpy, Oger
import src.aux as aux

class NeuralSeq:
    
    def __init__(self,isize,osize,sr):
        """
        Initialization of a Neural Sequencer using:
         * Input size as integer.
         * Reservoir size as integer.
         * Spectral Radius
        """
        self.isize = isize
        self.osize = osize
        self.sr = sr
        #numpy.random.seed(global_seed)
        
        self.net = Oger.nodes.ReservoirNode(self.isize, 
                                            self.osize, 
                                            dtype='float64', 
                                            spectral_radius=self.sr,
                                            reset_states=False,
                                            input_scaling=1.0 )
        
        self.w_out = numpy.random.random((osize,osize))
        #if not (w == None):
        #    self.net.w_in = w

    """
    Reset internal state of neural sequencer to null vector
    """

    def reset(self): # not preserve(self.net.initial_state)
        self.net.states = numpy.zeros((1,self.osize))

    """
    Encode a sequence in R^n using:
     * Input as a list
    """
        
    def process_input(self,input, reset = True):
        
        if (reset):
          self.reset()
        
        pinput = input
        #if (self.f == None):
        #    pinput = input
        #else:
        #    pinput = self.f(input)
        
        
        pinput = numpy.array(pinput)
        pinput.shape = (len(input), self.isize)
        esnout = numpy.empty(self.osize,dtype=numpy.double)
        esnout = self(pinput)
        
        return esnout
        
    def __call__(self,input): # not preserve(net.states)
        return  aux.normalize(self.net(input)[-1])
