import sys
sys.path.append('../')
import tensorflow as tf
from layer.Layer import Layer
from layer.BidirectLSTMLayer import BidirectLSTMLayer
from .AverageSentenceEncoder import AverageSentenceEncoder

class BiLSTMAverageSentenceEncoder(Layer):
    def __call__(self,inputs,seq_len = None):
        
        if self.call_cnt ==0:
            self.bilstm = BidirectLSTMLayer("Bilstm",self.output_dim,reuse = self.reuse)
            self.average_sentence_encoder = AverageSentenceEncoder("ASE",reuse = self.reuse)
        
        with tf.variable_scope(self.scope) as scope:
            self.check_reuse(scope)
            outputs,states = self.bilstm(inputs,seq_len)
            concated_outputs = tf.concat([outputs[0],outputs[1]],axis = 2)
            
            return self.average_sentence_encoder(concated_outputs,seq_len)
        
if __name__ =="__main__":

    a = tf.Variable([[[1.0,2],[3,4]],[[5,6],[7,8]]])
    b = tf.Variable([[[2.0,2],[3,4]],[[5,6],[7,8]]])
    lstm = BiLSTMAverageSentenceEncoder("biLSTMASE",10)
    output = lstm(a,seq_len = [1,2])
    output2 = lstm(b,seq_len = [2,2])
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())
    print(sess.run(output))
