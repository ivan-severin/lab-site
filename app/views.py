from app import app, object_list, get_object_or_404, database
from flask import  (abort, flash, Markup, redirect, render_template,
                   request, Response, session, url_for )
from app.models import Entry, User, datetime
from hashlib import md5

import functools


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/publications/')
def publications():
    return render_template('publications.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/contacts/')
def contacts():
    return render_template('contacts.html')

def login_required(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        if session.get('logged_in'):
            return fn(*args, **kwargs)
        return redirect(url_for('login', next=request.path))
    return inner


# flask provides a "session" object, which allows us to store information across
# requests (stored by default in a secure cookie).  this function allows us to
# mark a user as being logged-in by setting some values in the session data:
def auth_user(user):
    session['logged_in'] = True
    session['user_id'] = user.id
    session['username'] = user.username
    flash('You are logged in as %s' % (user.username))

# get the user from the session
def get_current_user():
    if session.get('logged_in'):
        return User.get(User.id == session['user_id'])




@app.route('/join/', methods=['GET', 'POST'])
def join():
    if request.method == 'POST' and request.form['username']:
        try:
            with database.transaction():
                # Attempt to create the user. If the username is taken, due to the
                # unique constraint, the database will raise an IntegrityError.
                user = User.create(
                    username=request.form['username'],
                    password=md5((request.form['password']).encode('utf-8')).hexdigest(),
                    email=request.form['email'],
                    join_date=datetime.datetime.now())

            # mark the user as being 'authenticated' by setting the session vars
            auth_user(user)
            return redirect(url_for('index'))

        # except IntegrityError:
        except Exception as e:
            flash(str(e))

    return render_template('join.html')



@app.route('/news/')
def news():
    search_query = request.args.get('q')
    if search_query:
        query = Entry.search(search_query)
    else:
        query = Entry.public().order_by(Entry.timestamp.desc())
    return object_list('news.html', query, search=search_query)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    next_url = request.args.get('next') or request.form.get('next')
    if request.method == 'POST' and request.form.get('password'):
        password = request.form.get('password')
        # TODO: If using a one-way hash, you would also hash the user-submitted
        # password and do the comparison on the hashed versions.
        if password == app.config['ADMIN_PASSWORD']:
            session['logged_in'] = True
            session.permanent = True  # Use cookie to store session.
            flash('You are now logged in.', 'success')
            return redirect(next_url or url_for('index'))
        else:
            flash('Incorrect password.', 'danger')
    return render_template('login.html', next_url=next_url)

@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('login'))
    return render_template('logout.html')



def _create_or_edit(entry, template):
    if request.method == 'POST':
        entry.title = request.form.get('title') or ''
        entry.content = request.form.get('content') or ''
        entry.published = request.form.get('published') or False
        if not (entry.title and entry.content):
            flash('Title and Content are required.', 'danger')
        else:
            # Wrap the call to save in a transaction so we can roll it back
            # cleanly in the event of an integrity error.
            try:
                with database.atomic():
                    entry.save()
            except IntegrityError:
                flash('Error: this title is already in use.', 'danger')
            else:
                flash('Entry saved successfully.', 'success')
                if entry.published:
                    return redirect(url_for('detail', slug=entry.slug))
                else:
                    return redirect(url_for('edit', slug=entry.slug))

    return render_template(template, entry=entry)

@app.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
    return _create_or_edit(Entry(title='', content=''), 'create.html')

@app.route('/drafts/')
@login_required
def drafts():
    query = Entry.drafts().order_by(Entry.timestamp.desc())
    return object_list('index.html', query, check_bounds=False)

@app.route('/<slug>/')
def detail(slug):
    if session.get('logged_in'):
        query = Entry.select()
    else:
        query = Entry.public()
    entry = get_object_or_404(query, Entry.slug == slug)
    return render_template('detail.html', entry=entry)

@app.route('/<slug>/edit/', methods=['GET', 'POST'])
@login_required
def edit(slug):
    entry = get_object_or_404(Entry, Entry.slug == slug)
    return _create_or_edit(entry, 'edit.html')

@app.template_filter('clean_querystring')
def clean_querystring(request_args, *keys_to_remove, **new_values):
    # We'll use this template filter in the pagination include. This filter
    # will take the current URL and allow us to preserve the arguments in the
    # querystring while replacing any that we need to overwrite. For instance
    # if your URL is /?q=search+query&page=2 and we want to preserve the search
    # term but make a link to page 3, this filter will allow us to do that.
    querystring = dict((key, value) for key, value in request_args.items())
    for key in keys_to_remove:
        querystring.pop(key, None)
    querystring.update(new_values)
    return urllib.urlencode(querystring)

@app.errorhandler(404)
def not_found(exc):
    return Response('<h3>Not found</h3>'), 404
