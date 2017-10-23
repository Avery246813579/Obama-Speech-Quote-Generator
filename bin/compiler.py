# This file is used to load our Markov Model and save it using pickle. This shortens our load time by > 2x

from RainbowChain import RainbowChain
import pickle
import time

start_time = time.time()

print("Loading Markov Model\n===============")
raw_model = RainbowChain('../static/data/raw_corpus.txt', 3)

corpus_load = time.time()
print("Corpus Loaded in " + str(corpus_load - start_time) + "s\n")


print("Saving Markov Model\n===============")
with open('../static/data/model.pickle', 'wb') as handle:
    pickle.dump(raw_model, handle, protocol=pickle.HIGHEST_PROTOCOL)

corpus_save = time.time()
print("Markov Model saved in " + str(corpus_save - corpus_load) + "s\n")

print("Time to Complete: " + str(corpus_save - start_time) + "s")
