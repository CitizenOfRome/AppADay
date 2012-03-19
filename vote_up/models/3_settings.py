settings = Storage()

#paths
settings.path_to = Storage()
settings.path_to.static = "/"+request.application+"/static"
settings.path_to.default = "/"+request.application+"/default"

#Display
settings.app_name = "Vote Up!" # The application name/title
settings.delta = 20 # Number of Posts to display at once
settings.delta_answers = 10 # Number of Answers to display at once
settings.delta_comments = 5 # Number of comments to display at once
settings.title_length = 100 # Length of the post/answer desc to be displayed as a title
settings.sub_length = 50 # Used for tag desc, etc
settings.tags_lt = 6 # Max tags to display when suggesting

#Backend
settings.taggable = string.letters+string.digits+"_-" # Used to filter out characters in tag_names
settings.salt = "Some mythical salt!" # Used in hashing the password
settings.max_tags = 5 # Max tags allowed in a post

# Selection-OrderBy Criteria
settings.sel = Storage()
settings.sel.posts = (~db.posts.votes)
settings.sel.answers = (~db.answers.votes)
settings.sel.comments = (~db.comments.votes)
settings.sel.comments_r = (~db.comments_r.votes)

#Permissions
settings.create_tag = 100 # Rep required for Tag-creation
settings.add_comment = 20 # Rep required for adding a comment