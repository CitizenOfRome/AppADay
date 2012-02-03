#Python2.7.2
'''BruteForces passwords given the hashes'''
'''Usage: Call the Brute function with a list of hashes and the required encryption function'''
import hashlib
from itertools import combinations
import string
chars = string.printable
def brute(hashlist, enc="sha224", max_depth=10):
    '''Try to bruteforce the str from the hash'''
    cracked = {}
    for i in xrange(max_depth):
        for combo in combinations(chars, i):
            try:
                combo = "".join(map(str, combo))
                #print i, combo
                if enc=="sha224": cracked[hashlist[hashlist.index(hashlib.sha224(combo).hexdigest())]] = combo
            except:  pass
            finally:
                if len(cracked)==len(hashlist):    return cracked
    return cracked
print brute(map(lambda s: hashlib.sha224(s).hexdigest(), ["abc", "12", "2", "$~*"]))