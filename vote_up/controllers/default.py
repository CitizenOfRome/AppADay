import json

session.path_to = {}
session.path_to["static"] = "/"+request.application+"/static"
session.path_to["default"] = "/"+request.application+"/default"

def index():
    '''Display a post, its comments, its answers and allow for vote-up'''
    if not session.user: return user()
    #print db(db.users).select()
    path_to=session.path_to
    posts=db(db.posts).select(orderby=(~db.posts.votes), limitby=(0,20))
    return response.render('default/main.html', locals())
    
def get_post():
    '''Display a post, its comments, its answers and allow for vote-up'''
    if not session.user: return user()
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
    if not request.vars.has_key("message"): return "false"
    if not session.user: return user()
    path_to=session.path_to
    post_id = db.posts.insert(
        title = request.vars["title"],
        message = request.vars["message"],
        user = session.user.id
    )
    #post = db.posts[post_id]
    return "true"

def new_response():
    '''Accept a new response'''
    if not request.vars.has_key("message"): return "false"
    if not session.user: return user()
    path_to=session.path_to
    post=db(db.posts.id == request.args[0]).select().first()
    post_id = db.answers.insert(
        message = request.vars["message"],
        post = post,
        user = session.user.id
    )
    #post = db.posts[post_id]
    return "true"

def new_comment():
    '''Accept a new comment for a post'''
    if not request.vars.has_key("message"): return "false"
    if not session.user: return user()
    path_to=session.path_to
    post=db(db.posts.id == request.args[0]).select().first()
    if post.user!=session.user.id and session.user.reputation<20:    return json.dumps({"message":"You need atleast 20 rep to comment"})
    post_id = db.comments.insert(
        message = request.vars["message"],
        post = post,
        user = session.user.id
    )
    #post = db.posts[post_id]
    return "true"
def new_comment_r():
    '''Accept a new comment for an answer'''
    if not request.vars.has_key("message"): return "false"
    if not session.user: return user()
    path_to=session.path_to
    answer=db(db.answers.id == request.args[0]).select().first()
    if answer.user!=session.user.id and session.user.reputation<20:    return json.dumps({"message":"You need atleast 20 rep to comment"})
    db.comments_r.insert(
        message = request.vars["message"],
        answer = answer,
        user = session.user.id
    )
    return "true"
    
def vote():
    '''Add a vote'''
    if not session.user:    return json.dumps({"votes":0, "status":0, "message":"You must be logged on to post"})
    path_to=session.path_to
    factor = 0
    if request.vars["post"]:
        var = db(db.posts.id == request.vars["post"]).select().first()
        factor=5
    elif request.vars["answer"]:
        var = db(db.answers.id == request.vars["answer"]).select().first()
        factor=10
    elif request.vars["comment"]:
        var = db(db.comments.id == request.vars["comment"]).select().first()
        factor=2
    elif request.vars["comment_r"]:
        var = db(db.comments_r.id == request.vars["comment_r"]).select().first()
        factor=2
    else: return None
    if session.user.reputation<15:    return json.dumps({"votes":0, "status":0, "message":"You need atleast 15 rep to vote"})
    user = db.users[var.user]
    if user.id==session.user.id:  return json.dumps({"votes":var.votes, "status":0, "message":"You cannot vote on your own content"})
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
    user.update_record(
        reputation = user.reputation+(inc+in2)*factor
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