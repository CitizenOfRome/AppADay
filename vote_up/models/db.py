# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite')
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db = db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db, hmac_key=Auth.get_or_create_key())
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables()

## configure email
mail=auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth,filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################
import urllib
import json
from datetime import datetime
def timedelta(frm, to=datetime.utcnow()):
    '''Returns the human readable time between two datetimes'''
    if frm==to: return "0 seconds"
    det = (to-frm).days
    s=""
    if det>0:
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
    det = (to-frm).seconds
    if det>=3600:
        det/=3600
        if  det>1: s="s"
        return str(det)+" hour"+s
    if det>=60:
        det/=60
        if  det>1: s="s"
        return str(det)+" minute"+s
    if  det!=1: s="s"
    return str(det)+" second"+s
import string
import hashlib
if session.user:    user_id=session.user.id
else: user_id=None
db.define_table('tags', db.Field('name', 'string'), db.Field('desc', 'text', default=""), db.Field('user', 'reference users', default=user_id), db.Field('time', 'datetime', default=datetime.utcnow()))
db.define_table('posts', 
    db.Field('title', 'string'),
    db.Field('message', 'text'),
    db.Field('user', 'reference users'),
    db.Field('votes', 'integer', default=0),
    db.Field('v_up', 'list:reference users'),
    db.Field('v_dn', 'list:reference users'),
    db.Field('tags', 'list:reference tags'),
    db.Field('time', 'datetime', default=datetime.utcnow())
)
db.define_table('answers',
    db.Field('message', 'text'),
    db.Field('post', db.posts),
    db.Field('user', 'reference users'),
    db.Field('votes', 'integer', default=0),
    db.Field('v_up', 'list:reference users'),
    db.Field('v_dn', 'list:reference users'),
    db.Field('time', 'datetime', default=datetime.utcnow())
)
db.define_table('comments',
    db.Field('message', 'string'),
    db.Field('post', db.posts),
    db.Field('user', 'reference users'),
    db.Field('votes', 'integer', default=0),
    db.Field('v_up', 'list:reference users'),
    db.Field('v_dn', 'list:reference users'),
    db.Field('time', 'datetime', default=datetime.utcnow())
)
db.define_table('comments_r',
    db.Field('message', 'string'),
    db.Field('answer', db.answers),
    db.Field('user', 'reference users'),
    db.Field('votes', 'integer', default=0),
    db.Field('v_up', 'list:reference users'),
    db.Field('v_dn', 'list:reference users'),
    db.Field('time', 'datetime', default=datetime.utcnow())
)

db.define_table('users',
    db.Field('name', 'string'),
    db.Field('password', 'password'),
    db.Field('reputation', 'integer', default=0),
    db.Field('joined', 'datetime', default=datetime.utcnow())
)