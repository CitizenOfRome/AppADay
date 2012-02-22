import datetime
def timedelta(frm, to):
    '''Returns the human readable time between two datetimes'''
    det = (to-frm).seconds
    if frm==to: return "0s"
    if det==0:
        det = (to-frm).days
        if det>365:  return str(det/365)+"y"
        if det>30:  return str(det/30)+"m"
        if det>7:  return str(det/7)+"w"
        return str(det)+"d"
    if det>3600:  return str(det/3600)+"h"
    if det>60:  return str(det/60)+"m"
    return str(det)+"s"