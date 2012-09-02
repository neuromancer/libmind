import sys
import mdp
import src.scaler as sc

from NeuralSeq import *
from src.aux import *

class WunVectorizer:

    def __init__(self, spectral_radius, woutput):
      
      #self.wvectorizer = wvectorizer
      self.alphabet = woutput.alphabet
      
      self.isize = woutput.getInternalSize()
      self.osize = woutput.getInternalSize()#output_size
      self.max_letters = woutput.max_seq
      
      #assert(stop_symbol in self.alphabet)
      self.stop_symbol = woutput.stop_symbol
      
      self.seqWordLetter = NeuralSeq(self.isize , self.osize, spectral_radius)
      self.scaler = sc.Scaler()
    
   
    def __get_vletter(self, vword):
      r =  self.seqWordLetter.process_input(list(vword), False)
      r.shape = (1,self.seqWordLetter.osize)
      return r
    
    def unvectorize(self, vword):
      
      self.seqWordLetter.reset()
      word = []
      
      for i in range(self.max_letters):
        
        word.append(self.__get_letter(vword))
        
        if (word[-1] == self.stop_symbol):
          break
      
      word = "".join(word)
      
      if word[-1] <> self.stop_symbol:
        word = word.rstrip(word[-1])+word[-1]
        #word = word + [self.stop_symbol]
      
      return word.strip(self.stop_symbol)
      
    
    def __get_letter(self, vword):
      vletter = self.__get_vletter(vword)
      svletter = self.scaler.transform(vletter)
      
      class NullWriter:
        def write(self, *args, **kwargs):
            pass
      
      stdout = sys.stdout
      sys.stdout = NullWriter()
      
      i = int(self.svm.label(svletter)[0])
      
      sys.stdout = stdout
      
      return self.alphabet[i]
      
    def __scale(self, data):
        sdata = self.scaler.transform(data)
        data_train = []

        for x in sdata:
            data_train.append(x)
        return data_train
    
    def __test_svm(self,  xs, ys):
        error = 0
    
        class NullWriter:
            def write(self, *args, **kwargs):
                pass
                    
        stdout = sys.stdout
        sys.stdout = NullWriter()
    
        for (x,y) in zip(xs,ys):
            if not (int(self.svm.label(x)[0]) == self.alphabet.index(y)):
                error = error + 1
            
        sys.stdout = stdout
        return float(error)/float(len(xs))
    
    def __process_data(self, words):
      
      vletters = []
      letters = []
      
      for (word,v) in words:
        
        #v = self.wvectorizer.wvectorize(word)
        self.seqWordLetter.reset()
        
        #print word
        
        for letter in word:
          #print letter
          vletters.append(self.__get_vletter(v))
          letters.append(letter)
        
        # end of words  
        #vletters.append(self.__get_vletter(v))
        #letters.append(".")
      
      return (vletters, letters)
      
    def __train_svm(self, xs, ys, c, gamma):
        
        svmRBF = mdp.nodes.LibSVMClassifier(kernel = 'RBF',
                                 params = {"C" : c, "gamma" : gamma},
                                 classifier = 'C_SVC', 
                                 probability = False,
                                 dtype='float64',
                                 input_dim=self.osize)
        
        for (vletter,letter) in zip(xs,ys):
            x = vletter
            y = numpy.array([self.alphabet.index(letter)])
            svmRBF.train(x,y)    
      
       
        svmRBF.stop_training()
        self.svm = svmRBF
    
    #def test_word(self,word):
    #  return (word, self.unvectorize(self.wvectorizer.wvectorize(word)))
    
    def train(self,train_words, test_words, debug = False):
      
      (train_vletters, train_letters) = self.__process_data(train_words)
      (test_vletters, test_letters) = self.__process_data(test_words)
      
      # data fitting for scaling
      self.scaler.fit(train_vletters)
      
      # data scaling
      train_svletters = self.__scale(train_vletters)
      
      if test_vletters <> []:
          test_svletters = self.__scale(test_vletters)
      else:
          test_svletters = []
      
      min_err = float('inf')

      # TODO: add linear svm
      
      for c_exp in range(1,8,2):
          for gamma_exp in range(-3,4,1):
              self.__train_svm(train_svletters, train_letters, pow(2,c_exp), pow(2,gamma_exp))
              error = self.__test_svm(test_svletters+train_svletters, test_letters+train_letters)
              
              
              if (min_err > error):
                  if (debug):
                      #print "c:", pow(2,c_exp), "gamma:", pow(2,gamma_exp), "->", error  
                      print error,
                      
                      print map(lambda (_,v): self.unvectorize(v), train_words)
                  self.last_svm = self.svm
                  min_err = error
      
      self.svm = self.last_svm
      return min_err
        
