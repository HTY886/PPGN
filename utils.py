import os
import random
import json
import numpy as np

def read_json(filename):
    with open(filename, 'r') as fp:
        data = json.load(fp)
    return data


class utils():
    def __init__(self,args):
        self.batch_size = args.batch_size
        self.data_dir = args.data_dir
        self.dict_path = args.dict_path
        self.sequence_length = args.sequence_length
        self.word_id_dict = read_json(args.dict_path)
        self.unknown_id =  self.word_id_dict['__UNK__']
        self.droptout_id = self.word_id_dict['__DROPOUT__']
        self.EOS_id = 0
        self.BOS_id = 1


        self.id_word_dict = [[]]*len(self.word_id_dict)
        print("vocalbulary_size :"  + str(len(self.id_word_dict)))
        for word in self.word_id_dict:
            self.id_word_dict[self.word_id_dict[word]] = word


    def word_drop_out(self,sents,rate=0.3):
        sents = np.array(sents)
        for i in range(len(sents)):
            for j in range(len(sents[i])):
                if random.random()<=rate and sents[i][j]!=0:
                    sents[i][j] = self.word_id_dict['__DROPOUT__']
        return sents 


    def sent2id(self,sent,l=None):
        sent_list = sent.strip().split()
        vec = np.zeros((self.sequence_length),dtype=np.int32)
        sent_len = len(sent_list)
        unseen = 0
        for i,word in enumerate(sent_list):
            if i==self.sequence_length:
                break
            if word in self.word_id_dict:
                vec[i] = self.word_id_dict[word]
            else:
                vec[i] = self.unknown_id
        if l:
            return vec,sent_len
        else:
            return vec  


    def id2sent(self,ids):
        word_list = []
        for i in ids:
            if i != self.unknown_id and i != self.EOS_id:
                word_list.append(self.id_word_dict[i])
        return ' '.join(word_list)

