def index():
    '''on=0/1 => -/+1 active for the given url'''
    on = request.vars["on"]
    url = request.vars["url"]
    record = db(db.urls.url==url).select().first()
    if not url or url=="": return response.render('default/index.html', locals())
    if not record:
        record_id = db.urls.insert(url=url, active=0)
        record = db.urls[record_id]
    if on == "1":   record.update_record(active=record.active+1)
    elif on == "0":   record.update_record(active=record.active-1)
    return record.active