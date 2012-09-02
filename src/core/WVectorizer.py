#!/usr/bin/env python2

import NeuralSeq

class WVectorizer:

    def __init__(self, input_size, output_size , spectral_radius):
      
      # initialization
      self.osize = output_size
      self.seqLetterWord = NeuralSeq.NeuralSeq(input_size, output_size, spectral_radius)


    def wvectorize(self, input):
      r = self.seqLetterWord.process_input(list(input))
      r.shape = (1,self.seqLetterWord.osize)
      return r
