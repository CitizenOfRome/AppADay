def index():
    '''Display a post, its comments, its responses and allow for vote-up'''
    posts=db(db.posts).select(orderby=(~db.posts.votes), limitby=(0,20))
    return response.render('default/main.html', locals())
    
def get_post():
    '''Display a post, its comments, its responses and allow for vote-up'''
    post=db(db.posts.id == request.args[0]).select().first()
    responses=db(db.answers.post == post).select(orderby=(~db.answers.votes), limitby=(0,20)).first()
    comments=db(db.comments.post == post).select(orderby=(~db.comments.votes), limitby=(0,20)).first()
    comments_r = {}
    if responses:
        for resp in answer:
            comments_r[resp.id]=(db(db.comments_r.answer == resp).select(orderby=(~db.comments_r.votes), limitby=(0,20)).first())
    return response.render('default/post.html', locals())
    
def new_post():
    '''Accept a new post'''
    post_id = db.posts.insert(
        title = request.vars["title"],
        message = request.vars["message"]
    )
    #post = db.posts[post_id]
    return "true"

def new_response():
    '''Accept a new response'''
    post=db(db.posts.id == request.args[0]).select().first()
    post_id = db.answers.insert(
        message = request.vars["message"],
        post = post
    )
    #post = db.posts[post_id]
    return "true"

def new_comment():
    '''Accept a new comment for a post'''
    post=db(db.posts.id == request.args[0]).select().first()
    post_id = db.comments.insert(
        message = request.vars["message"],
        post = post
    )
    #post = db.posts[post_id]
    return "true"
def new_comment_r():
    '''Accept a new comment for a response'''
    answer=db(db.answers.id == request.args[0]).select().first()
    db.comments.insert(
        message = request.vars["message"],
        answer = answer
    )
    #response = db.answers[response_id]
    return "true"
    
def vote():
    '''Add a vote'''
    if request.vars["post"]:    var = db(db.posts.id == request.vars["post"]).select().first()
    elif request.vars["response"]:    var = db(db.answers.id == request.vars["response"]).select().first()
    elif request.vars["comment"]:    var = db(db.comments.id == request.vars["comment"]).select().first()
    elif request.vars["comment_r"]:    var = db(db.comments_r.id == request.vars["comment_r"]).select().first()
    else: return None
    inc = 0
    if int(request.vars["up"])==1:  inc=1
    elif int(request.vars["up"])==0:   inc=-1
    var.update_record(votes=var.votes+inc)
    return var.votes