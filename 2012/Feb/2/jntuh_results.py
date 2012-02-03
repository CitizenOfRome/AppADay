#Python2.7.2
'''Usage: python jntu_results.py HallTicketNumebr ExamCode'''
'''Example: python jntu_results.py 08QQ1A0449 1036'''
import sys
import httplib
import string

if len(sys.argv)>2: ecode = sys.argv[-2]
else: ecode = "1036"
if len(sys.argv)>1: htno = sys.argv[-1]
else: htno = "08QQ1A0449"

def get_htno(htno, ecode):
    '''Gets the result HTML for the given HTNO and ECODE'''
    global conn, resp
    conn = None
    resp = None
    try:
        global conn, resp
        conn = httplib.HTTPConnection("jntu.ac.in")
        conn.request("GET", "/results/htno/"+htno+"/"+ecode+"/index.html")
        resp = conn.getresponse()
    except:
        print " conn_failed ",
        return get_htno(htno, ecode)
    conn.close()
    if resp.status > 400:
        print " BAD_STATUS: "+str(resp.status),
        return get_htno(htno, ecode)
    data = resp.read()
    acc = string.find(data, "<center>")
    if acc>-1:  data = data[acc:]
    else:
        print " BAD_DATA: "+data,
        return get_htno(htno, ecode)
    print data

get_htno(htno, ecode)