import json

session.path_to = {}
session.path_to["static"] = "/"+request.application+"/static"
session.path_to["default"] = "/"+request.application+"/default"

def index():
    '''Display a post, its comments, its answers and allow for vote-up'''
    #print db(db.users).select()
    path_to=session.path_to
    posts=db(db.posts).select(orderby=(~db.posts.votes), limitby=(0,20))
    if not session.user: return user()
    return response.render('default/main.html', locals())
    
def get_post():
    '''Display a post, its comments, its answers and allow for vote-up'''
    path_to=session.path_to
    post=db(db.posts.id == request.args[0]).select().first()
    answers=db(db.answers.post == post).select(orderby=(~db.answers.votes), limitby=(0,20))
    comments=db(db.comments.post == post).select(orderby=(~db.comments.votes), limitby=(0,20))
    comments_r = {}
    if answers:
        for answer in answers:
            comments_r[answer.id]=(db(db.comments_r.answer == answer).select(orderby=(~db.comments_r.votes), limitby=(0,20)))
    return response.render('default/post.html', locals())
    
def new_post():
    '''Accept a new post'''
    path_to=session.path_to
    post_id = db.posts.insert(
        title = request.vars["title"],
        message = request.vars["message"]
    )
    #post = db.posts[post_id]
    return "true"

def new_response():
    '''Accept a new response'''
    path_to=session.path_to
    post=db(db.posts.id == request.args[0]).select().first()
    post_id = db.answers.insert(
        message = request.vars["message"],
        post = post
    )
    #post = db.posts[post_id]
    return "true"

def new_comment():
    '''Accept a new comment for a post'''
    path_to=session.path_to
    post=db(db.posts.id == request.args[0]).select().first()
    post_id = db.comments.insert(
        message = request.vars["message"],
        post = post
    )
    #post = db.posts[post_id]
    return "true"
def new_comment_r():
    '''Accept a new comment for an answer'''
    path_to=session.path_to
    answer=db(db.answers.id == request.args[0]).select().first()
    db.comments_r.insert(
        message = request.vars["message"],
        answer = answer
    )
    return "true"
    
def vote():
    '''Add a vote'''
    if not session.user:    return user()
    path_to=session.path_to
    if request.vars["post"]:    var = db(db.posts.id == request.vars["post"]).select().first()
    elif request.vars["answer"]:    var = db(db.answers.id == request.vars["answer"]).select().first()
    elif request.vars["comment"]:    var = db(db.comments.id == request.vars["comment"]).select().first()
    elif request.vars["comment_r"]:    var = db(db.comments_r.id == request.vars["comment_r"]).select().first()
    else: return None
    inc = 0
    in2 = 0
    add = [session.user.id]
    if not var.v_up:    var.v_up = []
    if not var.v_dn:    var.v_dn = []
    if int(request.vars["up"])==1:
        inc=1
        if session.user.id in var.v_dn:
            var.v_dn.remove(session.user.id)
            in2 = 1
        if session.user.id in var.v_up:
            var.v_up.remove(session.user.id)
            inc = 0
            in2 = -1
            add = []
        var.update_record(
            votes=var.votes+inc+in2,
            v_up = var.v_up+add,
            v_dn = var.v_dn
        )
    elif int(request.vars["up"])==0:
        inc=-1
        if session.user.id in var.v_up:
            var.v_up.remove(session.user.id)
            in2 = -1
        if session.user.id in var.v_dn:
            var.v_dn.remove(session.user.id)
            inc = 0
            in2 = 1
            add = []
        var.update_record(
            votes=var.votes+inc+in2,
            v_dn = var.v_dn+add,
            v_up = var.v_up
        )
    return json.dumps({"votes":var.votes, "status":inc})
    
def user():
    '''Handle all things User-Auth related during dev'''
    path_to=session.path_to
    if request.vars["name"]:
        name = db(db.users.name == request.vars["name"].lower()).select()
        password = db(db.users.password == request.vars["password"]).select()
        if name:
            if password:
                session.user = name.first()
                return index()
        else:
            id = db.users.insert( name = request.vars["name"].lower(), password = request.vars["password"] )
            session.user = db.users[id]
            return index()
    if session.user:
        session.user = None
        return index()
    return response.render('default/user.html', locals())