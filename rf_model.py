import MySQLdb
import random
import numpy as np
from sklearn.cluster import KMeans
from sklearn import tree
from sklearn.externals.six import StringIO
import cPickle 
import sys


def connection():
    conn=MySQLdb.connect(host="localhost",user="root", passwd="utkarsh@mit", db="legion")
    cur= conn.cursor()
    return cur, conn

def extract_np_from_mysql(nrows = 500000):
    cur, conn = connection()
    cur.execute("SELECT * from bio_keywords")
    bio_keywords = cur.fetchall()
    cur.execute("SELECT alcohol, positive, negative, extra from acc_intents");
    acc_intents = cur.fetchall()
   
    
    len_bio_key = len(bio_keywords[0])
    len_acc_int = len(acc_intents[0])
    all_data = []
    for i in xrange(nrows):
        bio_keywords_one = []
        acc_intents_one = []
        data = []
        user_name = str(bio_keywords[i][0])[8:] #splice 'username' from user_name, retaining a number id
    
        bio_keywords_one.append(int(user_name))
        acc_intents_one.append(int(user_name))
    
        for j in xrange(1, len_bio_key):
            bio_keywords_one.append(float(bio_keywords[i][j]))
    
        for j in xrange(1, len_acc_int):
            acc_intents_one.append(float(acc_intents[i][j]))
        
        data = bio_keywords_one + acc_intents_one
        all_data.append(data) 
    
    return all_data


def kmeans_clustering():
    all_data = extract_np_from_mysql()
    model = KMeans(n_clusters = 8, max_iter = 50, tol = 0.0005)
    clustered_model = model.fit(all_data)
    #clustered_model.cluster_centers_
    print clustered_model.predict(all_data[0:10])
    with open('clustered_model.pkl', 'wb') as writer:
        cPickle.dump(clustered_model, writer)

def test():
    with open('clustered_model.pkl', 'rb') as reader:
        clustered_model = cPickle.load(reader)
    all_data = extract_np_from_mysql(10)
    print clustered_model.predict(all_data)    

if __name__ == '__main__':

    run_mode = sys.argv[1]
    if run_mode == 'train':
        kmeans_clustering()
    elif run_mode == 'test':
        test()
    else:
        print 'Invalid arguments!'
