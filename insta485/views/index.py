"""
Insta485 index (main) view.

URLs include:
/
"""
import flask
import insta485
import arrow


@insta485.app.route('/')
def show_index():
    """Display / route."""

    # Connect to database
    connection = insta485.model.get_db()

    # Query database
    logname = "awdeorio"
    users = connection.execute(
        "SELECT username, fullname "
        "FROM users "
        "WHERE username != ?",
        (logname, )
    )
    users = users.fetchall()

    following_posts = (
        "SELECT p.postid, p.filename, p.owner, p.created "
        "FROM posts p "
        "JOIN following f ON f.username1 = ? AND f.username2 = p.owner "
    )
    user_posts = (
        "SELECT p.postid, p.filename, p.owner, p.created "
        "FROM posts p "
        "WHERE p.owner = ? "
    )
    final_query = f"{following_posts} UNION {user_posts} ORDER BY created DESC"

    posts = connection.execute(final_query, (logname, logname))
    posts = posts.fetchall()

    for post in posts:
        post_id = post['postid']
        post_owner = post['owner']
        print(post_owner)

        owner = connection.execute(
            "SELECT filename FROM users WHERE username = ?", 
            (post_owner,)
        )
        owner = owner.fetchone()
        post['owner_img_url'] = owner['filename']

        likes = connection.execute(
            "SELECT * FROM likes WHERE postid = ?", 
            (post_id,)
        )
        likes = likes.fetchall()
        post['likes'] = len(likes)

        current_liked = connection.execute(
            "SELECT * FROM likes WHERE postid = ? AND owner = ?", 
            (post_id, logname)
        )
        if current_liked:
            post['current_liked'] = True
        else:
            post['current_liked'] = False

        comments = connection.execute(
            "SELECT owner, text FROM comments WHERE postid = ? ORDER BY created ASC", 
            (post_id,)
        )
        comments = comments.fetchall()
        post['comments'] = comments

        time = arrow.get(post['created']).to('US/Eastern')
        post['created'] = time.humanize()
        # print(posts)

    context = {
        "users": users,
        "posts": posts
    }
    return flask.render_template("index.html", **context)

@insta485.app.route('/users/<user_url_slug>/')
def show_user(user_url_slug):

    connection = insta485.model.get_db()

    logname = "awdeorio"

    context = {}
    user_data = connection.execute(
        "SELECT username, fullname FROM users WHERE username = ?",
        (user_url_slug, )
    ).fetchone()

    # if user_data is None:
    #     flask.abort(404)
    context["logname"] = logname
    context["username"] = user_data["username"]
    context["fullname"] = user_data["fullname"]

    following = connection.execute(
        "SELECT * FROM following WHERE username1 = ? AND username2 = ?",
        (logname, user_url_slug)
    )
    following = following.fetchone()
    if logname == user_url_slug:
        context["following"] = ""
    elif following:
        context["following"] = "following"
    else:
        context["following"] = "not following"
    
    posts = connection.execute(
        "SELECT * FROM posts WHERE owner = ?",
        (user_url_slug, )
    )
    posts = posts.fetchall()
    context["num_posts"] = len(posts)

    followers = connection.execute(
        "SELECT * FROM following WHERE username2 = ?",
        (user_url_slug, )
    )
    followers = followers.fetchall()
    context["num_followers"] = len(followers)

    following = connection.execute(
        "SELECT * FROM following WHERE username1 = ?",
        (user_url_slug, )
    )
    following = following.fetchall()
    context["num_following"] = len(following)

    posts = connection.execute(
        "SELECT postid, filename FROM posts WHERE owner = ?",
        (user_url_slug, )
    )
    posts = posts.fetchall()
    context["posts"] = posts

    print(context["posts"])
    


    
    
    return flask.render_template("user.html", **context)