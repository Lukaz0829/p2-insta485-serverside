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

    if user_data is None:
        flask.abort(404)
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

    return flask.render_template("user.html", **context)

@insta485.app.route('/users/<user_url_slug>/followers/')
def show_followers(user_url_slug):
    # Initialize database connection
    connection = insta485.model.get_db()

    logname = "awdeorio"

    context = {}

    user_data = connection.execute(
        "SELECT username FROM users WHERE username = ?",
        (user_url_slug,)
    )
    user_data = user_data.fetchone()

    if user_data is None:
        flask.abort(404)

    followers = connection.execute(
        "SELECT username1 FROM following WHERE username2 = ?",
        (user_url_slug,)
    )
    followers = followers.fetchall()

    follower_data = []
    for follower in followers:

        username1 = follower["username1"]
        following = connection.execute(
            "SELECT * FROM following WHERE username1 = ? AND username2 = ?",
            (logname, username1)
        )
        following = following.fetchone()

        pic = connection.execute(
            "SELECT filename FROM users WHERE username = ?", 
            (username1, )
        )
        pic = pic.fetchone()

        if(following):
            is_following = "following"
        else:
            is_following = "not following"

        follower_data.append({'username': username1, 'is_following': is_following, 'url': pic['filename']})

    context["followers"] = follower_data
    context["logname"] = logname

    return flask.render_template("followers.html", **context)

@insta485.app.route('/users/<user_url_slug>/following/')
def show_following(user_url_slug):
    connection = insta485.model.get_db()
    logname = "awdeorio"

    context = {}

    user_data = connection.execute(
        "SELECT username FROM users WHERE username = ?",
        (user_url_slug,)
    )
    user_data = user_data.fetchone()

    if user_data is None:
        flask.abort(404)

    following = connection.execute(
        "SELECT username2 FROM following WHERE username1 = ?",
        (user_url_slug,)
    )
    following = following.fetchall()

    following_data = []
    for user in following:
        username2 = user["username2"]

        is_following = connection.execute(
            "SELECT * FROM following WHERE username1 = ? AND username2 = ?",
            (logname, username2)
        )
        is_following = is_following.fetchone()

        pic = connection.execute(
            "SELECT filename FROM users WHERE username = ?", 
            (username2, )
        )
        pic = pic.fetchone()

        if is_following:
            status = "following"
        else:
            status = "not following"

        following_data.append({'username': username2, 'is_following': status, 'url': pic['filename']})

    context["following_users"] = following_data
    context["logname"] = logname

    return flask.render_template("following.html", **context)

@insta485.app.route('/posts/<postid_url_slug>/')
def show_post(postid_url_slug):
    connection = insta485.model.get_db()
    logname = "awdeorio"

    post = connection.execute(
        "SELECT * FROM posts WHERE postid = ?",
        (postid_url_slug, )
    )
    post = post.fetchone()

    # if post is None:
    #     flask.abort(404, "Post not found")

    owner = connection.execute(
        "SELECT filename FROM users WHERE username = ?", 
        (post['owner'], )
    )
    owner = owner.fetchone()

    # if owner is None:
    #     flask.abort(404, "Owner not found")

    likes = connection.execute(
        "SELECT * FROM likes WHERE postid = ?", 
        (postid_url_slug, )
    )
    likes = likes.fetchall()
    
    current_liked = connection.execute(
        "SELECT * FROM likes WHERE postid = ? AND owner = ?", 
        (postid_url_slug, logname)
    )
    current_liked = current_liked.fetchone()

    comments = connection.execute(
        "SELECT owner, text FROM comments WHERE postid = ? ORDER BY created ASC", 
        (postid_url_slug, )
    )
    comments = comments.fetchall()

    humanized_time = arrow.get(post['created']).to('US/Eastern').humanize()

    context = {
        'logname': logname,
        'postid': postid_url_slug,
        'owner': post['owner'],
        'post': post,
        'likes': len(likes),
        'current_liked': current_liked,
        'comments': comments,
        'owner_img_url': owner['filename'],
        'humanized_time': humanized_time
    }

    return flask.render_template('post.html', **context)

@insta485.app.route('/explore/')
def show_explore():
    connection = insta485.model.get_db()
    logname = "awdeorio"

    context = {}

    all_users = connection.execute(
        "SELECT username FROM users WHERE username != ?",
        (logname, )
    )
    all_users = all_users.fetchall()

    following_users = connection.execute(
        "SELECT username2 FROM following WHERE username1 = ?",
        (logname,)
    )
    following_users = following_users.fetchall()

    following = set()
    for user in following_users:
        following.add(user['username2'])
    not_following = []

    for user in all_users:
        username = user['username']
        if username not in following:
            not_following.append(user)

    data = []
    for user in not_following:
        user_data = connection.execute(
            "SELECT username, filename FROM users WHERE username = ?",
            (user['username'], )
        )
        user_data = user_data.fetchone()
        data.append({
            'username': user_data['username'],
            'user_img_url': user_data['filename']
        })
    context = {
        'logname': logname,
        'not_following': data
    }
    print("Context is ")

    return flask.render_template("explore.html", **context)

@insta485.app.route('/accounts/login/', methods=['GET'])
def login_page():
    if 'username' in flask.session:
        return flask.redirect('/')
    return flask.render_template('login.html')

@insta485.app.route('/accounts/logout/', methods=['POST'])
def logout():
    flask.session.pop('username', None)
    return flask.redirect('/accounts/login/')

@insta485.app.route('/accounts/create/', methods=['GET'])
def create_account():
    if 'username' in flask.session: 
        return flask.redirect('/accounts/edit/')
        
    if flask.request.method == 'POST':
        file = flask.request.files['file']
        fullname = flask.request.form['fullname']
        username = flask.request.form['username']
        email = flask.request.form['email']
        password = flask.request.form['password']

        return flask.redirect('/')

    return flask.render_template('create_account.html')

@insta485.app.route('/accounts/edit/')
def edit_account():
    if 'username' not in flask.session:
        return flask.redirect('/accounts/login/')
    
    username = flask.session['username']

    connection = insta485.model.get_db()

    context = {}

    user_detail = connection.execute(
        "SELECT * FROM users WHERE username = ?",
        (username, )
    )
    user_detail = user_detail.fetchone()

    context = {"user_detail": user_detail}

    
    return flask.render_template('edit_account.html', **context)

@insta485.app.route('/accounts/delete/', methods=['GET'])
def delete_account():
    if 'username' not in flask.session:
        return flask.redirect('/accounts/login/')
        
    if flask.request.method == 'POST':
        flask.session.pop('username', None)
        return flask.redirect('/accounts/create/')

    username = flask.session['username']
    return flask.render_template('delete_account.html', username=username)

@insta485.app.route('/accounts/password/')
def change_password():
    if 'username' not in flask.session:
        return flask.redirect('/accounts/login/')
    
    return flask.render_template('change_password.html')

@insta485.app.route('/accounts/auth/')
def auth():
    if 'username' in flask.session:
        return '', 200
    else:
        flask.abort(403)

@insta485.app.route('/likes/', methods=['POST'])
def like_unlike_post():
    # Check if the user is logged in
    username = "awdeorio"
    if 'username' not in flask.session:
        flask.abort(403)
    
    username = flask.session['username']
    postid = flask.request.form.get('postid')
    operation = flask.request.form.get('operation')
    target = flask.request.args.get('target', '/')
    
    connection = insta485.model.get_db()
    if operation == 'like':
        connection.execute(
            "INSERT INTO likes (owner, postid) VALUES (?, ?)",
            (username, postid)
        )
    elif operation == 'unlike':
        connection.execute(
            "DELETE FROM likes WHERE owner = ? AND postid = ?",
            (username, postid)
        )
    else:
        flask.abort(400)
    
    return flask.redirect(target)
