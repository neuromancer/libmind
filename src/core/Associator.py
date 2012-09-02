import numpy, mdp, random
import Oger
import src.scaler as sc
import OnlineCluster as oc

class Associator:
    def __init__(self, isize, osize):
        self.isize  = isize
        self.osize  = osize
        self.lrs     = []
        self.Xscaler = sc.Scaler()
        self.Yscaler = sc.Scaler()
        
        self.Xtrain_data = []
        self.Ytrain_data = []
        
        self.randy = numpy.random.random((1,self.osize))
        
        # exp clustering
        # TODO: how to tune this parameter?
        self.clustering=oc.OnlineCluster(20)
        
    def addToTrain(self, x, y):
        
        self.clustering.cluster(x)
        
        if (self.Xtrain_data == []):
            self.Xtrain_data = [x]
            self.Ytrain_data = [y]
            return 
        
        self.Xtrain_data = numpy.concatenate((self.Xtrain_data, [x]))
        self.Ytrain_data = numpy.concatenate((self.Ytrain_data, [y]))
        
        
    def __mkmodel(self):
        
        # TODO: which one is better, linear or ridge regression?
        #model =  mdp.nodes.LinearRegressionNode(
        model =  Oger.nodes.RidgeRegressionNode(
                                  dtype='float64',
                                  input_dim=self.isize,
                                  output_dim=self.osize
                                  )
        return model
    
    def __getcluster(self, x):
        assert(self.centers <> [])
        ws = map(lambda center: oc.kernel(x,center), self.centers)
        #print ws
        # FIXME: check if there are several maxs
        return list.index(ws, max(ws))
        
    def train(self, debug):
    
        self.clusters = self.clustering.trimclusters()
        self.centers  = map(lambda c: c.center, self.clusters) 
        
        #print self.centers
        
        #print centers
        print "I clustered %d points and found %d clusters."%(len(self.Xtrain_data), len(self.clusters))
        
        for i in range(len(self.clusters)):
            self.lrs.append(self.__mkmodel())
            print "Training", i, "linear approximation with",
            tsize = 0
            
            for (x,y) in zip(self.Xtrain_data,self.Ytrain_data):
                xi = self.__getcluster(x)
                #
                if (xi == i):
                    self.lrs[i].train(x,y)
                    tsize = tsize + 1 
            
            print tsize
            if (tsize > 0):
                self.lrs[i].stop_training()
            else:
                self.centers[i] = numpy.repeat(float("-inf"),self.isize)
                self.lrs[i] = None
        
    def getAssociation(self, x):
        
        if (self.lrs == []):
            return self.randy
        
        single = [x]#self.Xscaler.transform([x])
        i = self.__getcluster(single[0]) 
        
        assert(self.lrs[i] <> None)
        
        y = self.lrs[i].execute(single[0])
        
        return y
