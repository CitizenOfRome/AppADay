db.define_table('tags',
    db.Field('name', 'string'),
    db.Field('desc', 'text', default=""),
    db.Field('user', 'reference users', default=session.user),
    db.Field('time', 'datetime', default=datetime.utcnow())
)


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
    
    
if not db(db.tags.name == "meta").select().first():
    db.tags.insert(name="meta", desc="Meta is the place to discuss about the platform itself. All posts tagged 'meta' are listed here.")