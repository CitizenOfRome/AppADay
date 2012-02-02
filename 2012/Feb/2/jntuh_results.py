import sys
import httplib

if len(sys.argv)>2: ecode = sys.argv[-2]
else: ecode = "1036"
if len(sys.argv)>1: htno = sys.argv[-1]
else: htno = "08QQ1A0449"

def get_htno(htno, ecode):
    '''Gets the result HTML for the given HTNO and ECODE'''
    try:
        conn = httplib.HTTPConnection("jntu.ac.in")
        conn.request("GET", "/results/htno/"+htno+"/"+ecode+"/index.html")
        resp = conn.getresponse()
    except:
        print " conn_failed ",
        get_htno(htno, ecode)
    conn.close()
    if resp.status > 400:
        print " BAD_STATUS: "+str(resp.status),
        get_htno(htno, ecode)
    data = resp.read()
    try:
        data = data[data.index("<center>"):]
    except IndexError:
        print " BAD_DATA: "+data,
        get_htno(htno, ecode)
    print data

get_htno(htno, ecode)