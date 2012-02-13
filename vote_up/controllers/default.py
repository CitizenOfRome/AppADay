def index():
    '''Display a post, its comments, its responses and allow for vote-up'''
    posts=db(db.posts).select(orderby=(db.posts.votes))
    return response.render('default/index.html', locals())
    
def new_post():
    '''Accept a new post'''
    post_id = db.posts.insert(
        title = request.vars["title"],
        message = request.vars["message"]
    )
    #post = db.posts[post_id]
    return index()
    
def vote():
    '''Add a vote'''
    post = db(db.posts.id == request.vars["post"]).select().first()
    if int(request.vars["up"])==1:  inc=1
    else:   inc=-1
    post.update_record(votes=post.votes+inc)
    return index()