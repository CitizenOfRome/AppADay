#Python2.7.2
'''BruteForces passwords given the hashes (hexdigests)'''
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
                elif enc=="md5": cracked[hashlist[hashlist.index(hashlib.md5(combo).hexdigest())]] = combo
                elif enc=="sha1": cracked[hashlist[hashlist.index(hashlib.sha1(combo).hexdigest())]] = combo
                elif enc=="sha256": cracked[hashlist[hashlist.index(hashlib.sha256(combo).hexdigest())]] = combo
                elif enc=="sha384": cracked[hashlist[hashlist.index(hashlib.sha384(combo).hexdigest())]] = combo
                elif enc=="sha512": cracked[hashlist[hashlist.index(hashlib.sha512(combo).hexdigest())]] = combo
            except:  pass
            finally:
                if len(cracked)==len(hashlist):    return cracked
    return cracked
print brute(map(lambda s: hashlib.sha224(s).hexdigest(), ["abc", "12", "2", "$~*"]))