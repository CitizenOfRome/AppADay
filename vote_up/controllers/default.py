import json

session.path_to = {}
session.path_to["static"] = "/"+request.application+"/static"
session.path_to["default"] = "/"+request.application+"/default"
session.delta = 5
#TODO:Tags, Edit, Profiles, Search
def index():
    '''Display the list of posts'''
    if not session.user: redirect(session.path_to['default']+"/user")
    #print db(db.users).select()
    path_to=session.path_to
    posts=db(db.posts).select(orderby=(~db.posts.votes), limitby=(0, session.delta))
    return response.render('default/main.html', locals())
    
def get_post():
    '''Display a post, its comments, its answers and allow for vote-up'''
    if not session.user: redirect(session.path_to['default']+"/user")
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
    if not session.user: redirect(session.path_to['default']+"/user")
    path_to=session.path_to
    post=db(db.posts.id == request.args[0]).select().first()
    if post.user!=session.user.id:  return json.dumps({"message":"This aint yer post"})
    if request.vars["title"]: 
        post.update_record()
    else:   return response.render('default/edit_post.html', locals())

def suggest_tags():
    '''Return a list of tags matching a partially complete name'''
    tag = request.vars["tag"].strip().lower()
    #db.tags.insert(name="banana", desc="A delicious tropical fruit that sustains a few economies.")
    def validate(row):
        try:
            return row.name.lower().index(tag)>-1
        except ValueError:
            try:
                return row.desc.lower().index(tag)>-1
            except ValueError:
                return False
        return False
    try:    tags = db(db.tags).select().find(validate)
    except ValueError:  tags=[]
    if not tags:    tags=[]
    ret = {}
    i = 1
    for tag in tags:
        ret[tag.id]=[tag.name, tag.desc]
        if i==6: break
        i += 1
    return json.dumps({"tags":ret})
    
def moar():
    '''Load moar posts/answers/comments for XHRs'''
    #if not session.user: return "You must be signed in to view this stuff"
    if request.vars["moar"]: moar = int(request.vars["moar"])
    else: moar = 0
    if request.vars["delta"]: session.delta = int(request.vars["delta"])
    path_to=session.path_to
    if request.vars["post"]:
        vars = db(db.posts).select(orderby=(~db.posts.votes), limitby=(moar,moar+session.delta))
        if not vars: vars=[]
        ret = ""
        for post in vars:
            ret = ret+'''<div class="post"><a href="'''+path_to["default"]+'''/get_post/'''+str(post.id)+'''">
                <span class="vote">'''+str(post.votes)+'''</span>
                <span class="title">'''+post.title+'''</span>
                <span class="name">-'''+db.users[post.user].name+'''</span>
                <span class="rep">('''+str(db.users[post.user].reputation)+''')</span>
                </a></div>'''
        return ret
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
        ret = ""
        for comment in comments:
            if comment.v_up and session.user.id in comment.v_up:   up = '_h'
            else: up = ''
            if comment.v_dn and session.user.id in comment.v_dn:   dn = '_h'
            else: dn = ''
            ret = ret+'''
                    <tr class="comment">
                        <td class="vote" id="'''+str(post.id)+'''_'''+str(comment.id)+'''">
                            <image class="vicon"src="'''+path_to['static']+'''/images/up'''+up+'''.png" onclick="submit(\''''+path_to['default']+'''/vote?up=1&comment='''+str(comment.id)+'''\', function(votes){vote(votes, \''''+str(post.id)+'''_'''+str(comment.id)+'''\')})" />
                            <p>'''+str(comment.votes)+'''</p>
                            <image class="vicon"src="'''+path_to['static']+'''/images/dn'''+dn+'''.png" onclick="submit(\''''+path_to['default']+'''/vote?up=0&comment='''+str(comment.id)+'''\', function(votes){vote(votes, \''''+str(post.id)+'''_'''+str(comment.id)+'''\')})" />
                        </td>
                        <td class="content">
                            <span class="title">'''+comment.message+'''</span>
                            -'''+db.users[comment.user].name+'''('''+str(db.users[comment.user].reputation)+''')
                            <hr/>
                        </td>
                    </tr>
            '''
        return ret
    elif request.vars["comment_r"]:
        post=db(db.answers.id == request.vars["comment_r"]).select().first()
        comments=db(db.comments_r.answer == post).select(orderby=(~db.comments_r.votes), limitby=(moar,moar+session.delta))
        if not comments: comments=[]
        ret = ""
        for comment in comments:
            if comment.v_up and session.user.id in comment.v_up:   up = '_h'
            else: up = ''
            if comment.v_dn and session.user.id in comment.v_dn:   dn = '_h'
            else: dn = ''
            ret = ret+'''
                    <tr class="comment">
                        <td class="vote" id="r'''+str(post.id)+'''_'''+str(comment.id)+'''">
                            <image class="vicon"src="'''+path_to['static']+'''/images/up'''+up+'''.png" onclick="submit(\''''+path_to['default']+'''/vote?up=1&comment='''+str(comment.id)+'''\', function(votes){vote(votes, \'r'''+str(post.id)+'''_'''+str(comment.id)+'''\')})" />
                            <p>'''+str(comment.votes)+'''</p>
                            <image class="vicon"src="'''+path_to['static']+'''/images/dn'''+dn+'''.png" onclick="submit(\''''+path_to['default']+'''/vote?up=0&comment='''+str(comment.id)+'''\', function(votes){vote(votes, \'r'''+str(post.id)+'''_'''+str(comment.id)+'''\')})" />
                        </td>
                        <td class="content">
                            <span class="title">'''+comment.message+'''</span>
                            -'''+db.users[comment.user].name+'''('''+str(db.users[comment.user].reputation)+''')
                            <hr/>
                        </td>
                    </tr>
            '''
        return ret
    else: return None
    
def new_post():
    '''Accept a new post'''
    path_to=session.path_to
    if not request.vars.has_key("message"): return response.render('default/new_post.html', locals())
    if not session.user: redirect(session.path_to['default']+"/user")
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
    if not session.user: redirect(session.path_to['default']+"/user")
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
    if not session.user: redirect(session.path_to['default']+"/user")
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
    if not session.user: redirect(session.path_to['default']+"/user")
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
    '''Handle all things User-Auth related during dev'''
    path_to=session.path_to
    if request.vars["name"]:
        name = db(db.users.name == request.vars["name"].lower()).select()
        password = db(db.users.password == request.vars["password"]).select()
        if name:
            if password:
                session.user = name.first()
                redirect(session.path_to['default'])
        else:
            id = db.users.insert( name = request.vars["name"].lower(), password = request.vars["password"] )
            session.user = db.users[id]
            redirect(session.path_to['default'])
    if session.user:
        session.user = None
        redirect(session.path_to['default'])
    return response.render('default/user.html', locals())