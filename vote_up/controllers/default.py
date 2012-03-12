import json

session.path_to = {}
session.path_to["static"] = "/"+request.application+"/static"
session.path_to["default"] = "/"+request.application+"/default"
session.delta = 10
session.title_length = 100
#TODO:Tags, Edit, Profiles, Search
def index():
    '''Display the list of posts'''
    if not session.user: redirect(session.path_to['default']+"/auth")
    #print db(db.users).select()
    path_to=session.path_to
    posts=db(db.posts).select(orderby=(~db.posts.votes), limitby=(0, session.delta))
    return response.render('default/main.html', locals())
    
def get_post():
    '''Display a post, its comments, its answers and allow for vote-up'''
    if not session.user: redirect(session.path_to['default']+"/auth")
    path_to=session.path_to
    post=db(db.posts.id == request.args[0]).select().first()
    answers=db(db.answers.post == post).select(orderby=(~db.answers.votes), limitby=(0, session.delta))
    comments=db(db.comments.post == post).select(orderby=(~db.comments.votes), limitby=(0, session.delta))
    comments_r = {}
    if answers:
        for answer in answers:
            comments_r[answer.id]=(db(db.comments_r.answer == answer).select(orderby=(~db.comments_r.votes), limitby=(0, session.delta)))
    return response.render('default/post.html', locals())
    
def edit_post():
    '''Display a post, its comments, its answers and allow for vote-up'''
    if not session.user: redirect(session.path_to['default']+"/auth")
    path_to=session.path_to
    post=db(db.posts.id == request.args[0]).select().first()
    if post.user!=session.user.id:  return json.dumps({"message":"This aint yer post"})
    if request.vars["title"]: 
        post.update_record()
    else:   return response.render('default/edit_post.html', locals())

import string
session.taggable = string.letters+string.digits
def suggest_tags():
    '''Return a list of tags matching a partially complete name'''
    tag = request.vars["tag"].strip().lower()
    if request.vars["ptags"]:   ptags = [int(x) for x in filter(bool, request.vars["ptags"].lower().split(","))]
    else:   ptags = []
    limit = 6
    #db.tags.insert(name="carrot", desc="A vegetable with an edible, reddish-orange root.")
    def validate_name(row):
        try:
            return (int(row.id) not in ptags) and row.name.lower().index(tag)>-1
        except ValueError:
            return False
        return False
    def validate_desc(row):
        try:
            return (int(row.id) not in ptags) and (row not in tags) and row.desc.lower().index(tag)>-1
        except ValueError:
            return False
        return False
    sel = db(db.tags).select()
    desc_lt = int(session.title_length*0.5)
    if request.vars["new"]=="1":
        #if session.user.reputation<100:    return json.dumps({"message":"You need atleast 100 rep to create a tag"})
        tag = "".join(filter(bool, [x for x in tag if x in session.taggable]))
        if tag=="":    return json.dumps({"message":"Why are you trying to create an empty tag?"})
        tid = db.tags.insert(name=tag, desc="A new tag created by "+session.user.name)
        tag = db.tags[tid]
        print db.tags[12]
        if len(tag.desc)>desc_lt:  ext = "..."
        else:   ext = ""
        return json.dumps({"tags":[tag.name, tag.desc[:desc_lt]+ext, tag.id]})
    tags = list(sel.find(validate_name))
    if not tags:    tags=[]
    if len(tags)<limit: tags+=(sel.find(validate_desc))
    ret = {}
    i = 1
    for tag in tags:
        if len(tag.desc)>desc_lt:  ext = "..."
        else:   ext = ""
        ret[i]=[tag.name, tag.desc[:desc_lt]+ext, tag.id]
        if i==limit: break
        i += 1
    return json.dumps({"tags":ret})
    
def moar():
    '''Load moar posts/answers/comments for XHRs'''
    if not session.user: return "You must be signed in to view this stuff"
    if request.vars["moar"]: moar = int(request.vars["moar"])
    else: moar = 0
    if request.vars["delta"]: session.delta = int(request.vars["delta"])
    path_to=session.path_to
    if request.vars["post"]:
        posts = db(db.posts).select(orderby=(~db.posts.votes), limitby=(moar,moar+session.delta))
        if not posts: posts=[]
        return response.render('default/main_delta.html', locals())
    elif request.vars["answer"]:
        post=db(db.posts.id == request.vars["answer"]).select().first()
        answers=db(db.answers.post == post).select(orderby=(~db.answers.votes), limitby=(moar,moar+session.delta))
        comments_r = {}
        if not answers: return ""
        for answer in answers:
            comments_r[answer.id]=(db(db.comments_r.answer == answer).select(orderby=(~db.comments_r.votes), limitby=(moar,moar+session.delta)))
        return response.render('default/post_delta.html', locals())
    elif request.vars["comment"]:
        post=db(db.posts.id == request.vars["comment"]).select().first()
        comments=db(db.comments.post == post).select(orderby=(~db.comments.votes), limitby=(moar,moar+session.delta))
        if not comments: comments=[]
        return response.render('default/comments_delta.html', locals())
    elif request.vars["comment_r"]:
        answer=db(db.answers.id == request.vars["comment_r"]).select().first()
        comments=db(db.comments_r.answer == answer).select(orderby=(~db.comments_r.votes), limitby=(moar,moar+session.delta))
        if not comments: comments=[]
        return response.render('default/comments_r_delta.html', locals())
        return ret
    else: return None
    
def new_post():
    '''Accept a new post'''
    path_to=session.path_to
    if not request.vars.has_key("message"): return response.render('default/new_post.html', locals())
    if not session.user: redirect(session.path_to['default']+"/auth")
    post_id = db.posts.insert(
        title = request.vars["title"],
        message = request.vars["message"],
        user = session.user.id,
        tags = request.vars["tags"].lower().split(",")
    )
    print(db.posts[post_id])
    redirect(session.path_to['default']+"/get_post/"+str(post_id))

def new_response():
    '''Accept a new response'''
    if not request.vars.has_key("message"): return "false"
    if not session.user: redirect(session.path_to['default']+"/auth")
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
    if not request.vars.has_key("message"): return json.dumps({"status":0,"message":"Bad Message"})
    if not session.user: redirect(session.path_to['default']+"/auth")
    path_to=session.path_to
    post=db(db.posts.id == request.args[0]).select().first()
    if post.user!=session.user.id and session.user.reputation<20:    return json.dumps({"status":0,"message":"You need atleast 20 rep to comment"})
    id = db.comments.insert(
        message = request.vars["message"],
        post = post,
        user = session.user.id
    )
    #post = db.posts[post_id]
    return json.dumps({"status":1,"message":"", "id":id, "ans_id":post.id})
def new_comment_r():
    '''Accept a new comment for an answer'''
    if not request.vars.has_key("message"): return json.dumps({"status":0,"message":"Bad Message"})
    if not session.user: redirect(session.path_to['default']+"/auth")
    path_to=session.path_to
    answer=db(db.answers.id == request.args[0]).select().first()
    if answer.user!=session.user.id and session.user.reputation<20:    return json.dumps({"status":0,"message":"You need atleast 20 rep to comment"})
    id = db.comments_r.insert(
        message = request.vars["message"],
        answer = answer,
        user = session.user.id
    )
    return json.dumps({"status":1,"message":"", "id":id, "ans_id":answer.id})

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
    user = db.users[var.user]
    if user.id==session.user.id:  return json.dumps({"votes":var.votes, "status":0, "message":"You cannot vote on your own content"})
    if session.user.reputation<15:    return json.dumps({"votes":var.votes, "status":0, "message":"You need atleast 15 rep to vote"})
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
    '''Display user-Profile'''
    if not session.user: redirect(session.path_to['default']+"/auth")
    try:    user = db.users[int(request.args[0])]
    except: redirect(session.path_to['default']+"/user/"+str(session.user.id))
    if not user:    redirect(session.path_to['default']+"/user/"+str(session.user.id))
    print user
    return response.render('default/profile.html', locals())
    
import hashlib
    
def auth():
    '''Handle all things User-Auth related during dev'''
    def get_hash(string):
        salt = "Some mythical salt"
        return hashlib.sha512(salt+string+salt).hexdigest()
    path_to=session.path_to
    if request.vars["name"]:
        user = db(db.users.name == request.vars["name"].lower()).select()
        if user:
            user = user.first()
            if user.password==get_hash(request.vars["password"]+str(user.id)):
                session.user = user
                redirect(session.path_to['default'])
        else:
            id = db.users.insert( name = request.vars["name"].lower())
            session.user = db.users[id]
            session.user.update_record(password = get_hash(request.vars["password"]+str(id)))
            redirect(session.path_to['default'])
    if session.user:
        session.user = None
        redirect(session.path_to['default'])
    return response.render('default/auth.html', locals())