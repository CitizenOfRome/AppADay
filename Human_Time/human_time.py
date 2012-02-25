import datetime
def timedelta(frm, to):
    '''Returns the human readable time between two datetimes'''
    if frm==to: return "0 seconds"
    det = (to-frm).seconds
    s=""
    if det==0:
        det = (to-frm).days
        if det>365:
            det /= 365
            if  det>1: s="s"
            return str(det)+" year"+s
        if det>30:
            det/=30
            if  det>1: s="s"
            return str(det)+" month"+s
        if det>7:
            det/=7
            if  det>1: s="s"
            return str(det)+" week"+s
        if det>1:  s="s"
        return str(det)+" day"+s
    if det>3600:
        det/=3600
        if  det>1: s="s"
        return str(det)+" hour"+s
    if det>60:
        det/=60
        if  det>1: s="s"
        return str(det)+" minute"+s
    if  det>1: s="s"
    return str(det)+" second"+s