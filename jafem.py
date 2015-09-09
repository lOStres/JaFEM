import sys, os
from readdata import *
from rtree import index

# perform k-NN search for file in spatial index
def similarity(directory, filename, k):
    # first extract features from query file
    featureVector = extractFeatures(directory,filename)

    # then open and query spatial index
    p = index.Property()
    p.dat_extension = 'data'
    p.idx_extension = 'index'
    p.dimension = 13

    rtree = index.Index('rtreez', properties=p, interleaved=True)
    similar = list(rtree.nearest((featureVector[0], featureVector[1],
        featureVector[2], featureVector[3], featureVector[4],featureVector[5],
        featureVector[6], featureVector[7], featureVector[8], featureVector[9],
        featureVector[10], featureVector[11], featureVector[12],
        featureVector[0], featureVector[1], featureVector[2], featureVector[3],
        featureVector[4], featureVector[5], featureVector[6], featureVector[7],
        featureVector[8], featureVector[9], featureVector[10],
        featureVector[11], featureVector[12]), k))
    return similar

