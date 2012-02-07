def num2txt(n):
    '''Returns the textual equivalent of the given number'''
    n = abs(int(n))
    first19 = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    if n<20:  return first19[n]
    #100,200-900 10,20-90 0-9 => Pairs of 3 with "", thousand, million, bn, ...
    tens = ["twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    pow10 = ["thousand", "million", "billion", "trillion"]
    pow10_len = len(pow10)
    first19[0] = ""
    s = str(n)
    result = []
    while len(s)>0:
        x=int(s[-2:])
        if x!=0:    apn = " and"
        else:   apn = ""
        if x<20:    result = [first19[x]]+result
        else:   result = [tens[int(s[-2])-2]+" "+first19[int(s[-1])]]+result
        if len(s)>2:    result = [first19[int(s[-3])]+" hundred"+apn]+result
        s = s[:-3]
    p = 0
    i = 2
    while result[:-i]!=[]:
        result = result[:-i]+[pow10[p]]+result[-i:]
        i+=3
        p+=1
        if  p==pow10_len:   p = 0
    return " ".join(result)
    
from string import letters
letters += " "
def txt2num(s):
    '''Returns the numeric equvivalent of the given text'''
    nums = {"zero":0, "one":1, "two":2, "three":3, "four":4, "five":5, "six":6, "seven":7, "eight":8, "nine":9, "ten":10, "eleven":11, "twelve":12, "thirteen":13, "fourteen":14, "fifteen":15, "sixteen":16, "seventeen":17, "eighteen":18, "nineteen":19, "twenty":2, "thirty":3, "forty":4, "fifty":5, "sixty":6, "seventy":7, "eighty":8, "ninety":9}
    return int("".join(map(lambda x:str(nums[x]),filter(lambda x: x in nums,"".join(filter(lambda x: x in letters, str(s).lower())).split(" ")))))

import sys
s = " ".join(sys.argv[1:])
if len(sys.argv)<2: print "Usage: python "+sys.argv[0]+" whole-number"
else:
    try:
        print num2txt(int(s))
    except ValueError:
        try:    print txt2num(s)
        except ValueError:  print "Usage: python "+sys.argv[0]+" valid-whole-number"