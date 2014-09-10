import gzip
import cPickle as pickle

def save_gzip(params,path):
    with gzip.open(path+'.pk.gz','wb') as ptr:
        pickle.dump(params,ptr)

def load_gzip(path):
    with gzip.open(path+'.pk.gz','rb') as ptr:
        params = pickle.load(ptr)
        
    return params

'''
Read in a file and return lines as list of lists
'''
def read_file(filename,splitOn=None,stripOn=None,header=False,removeQuotes=False):
    header_line = list() 
    body_lines = list()
    with open(filename,'r') as ifp:
        if header:
            header = ifp.readline().strip(stripOn).split(splitOn)
            if removeQuotes:
                header = [h.strip('"') for h in header]
            header_line = header

        for line in ifp.readlines():
            line = line.strip(stripOn).split(splitOn)
            if removeQuotes:
                line = [l.strip('"') for l in line]

            body_lines.append(line)

    if header:
        return (header_line,body_lines)
    else:
        return body_lines

def flatten_2d(list):
    return [item for sublist in list for item in sublist]

'''
Implementation taken from Kaggle.com
'''
def tiedrank(X):  
    Z = [(x, i) for i, x in enumerate(X)]  
    Z.sort()  
    n = len(Z)  
    Rx = [0]*n   
    for j, (x,i) in enumerate(Z):  
        Rx[i] = j+1  
        s = 1           # sum of ties.  
        start = end = 0 # starting and ending marks.  
        for i in range(1, n):  
            if Z[i][0] == Z[i-1][0] and i != n-1:  
                pos = Z[i][1]  
                s+= Rx[pos]  
                end = i   
            else: #end of similar x values.  
                tiedRank = float(s)/(end-start+1)  
                for j in range(start, end+1):  
                    Rx[Z[j][1]] = tiedRank  
                for j in range(start, end+1):  
                    Rx[Z[j][1]] = tiedRank  
                start = end = i  
                s = Rx[Z[i][1]]    
    return Rx

def AUC(labels, posterior):
    r = tiedrank(posterior)
    auc = (sum(r*(labels==1)) - sum(labels==1)*(sum(labels==1)+1)/2) / (sum(labels<1)*sum(labels==1));
    return auc
