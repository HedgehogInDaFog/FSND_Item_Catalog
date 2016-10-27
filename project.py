#clietn_id = 718036307480-s9kjb30rc4ltodh5bvsgikletiqc4mm2.apps.googleusercontent.com
#client_secret zhLjG8JUcOUCejpzpUfnL-QZ

from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, BookItem, User

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Category book app"

app = Flask(__name__)

engine = create_engine('sqlite:///categorybookwithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/')
@app.route('/category/')
@app.route('/categories/')
def showCategories():
    categories = session.query(Category)
    if 'username' not in login_session:
        login_str = "You are not logged in"
    else:
        login_str = "You logged in as %s" % login_session['username']
    return render_template('categories.html', categories=categories, login_str=login_str)


@app.route('/categories/<int:category_id>/')
def categoryBooks(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(BookItem).filter_by(category_id=category.id)
    if 'username' not in login_session:
        login_str = "You are not logged in"
        current_user_id = 0
    else:
        login_str = "You logged in as %s" % login_session['username']
        current_user_id = login_session['user_id']
    return render_template('books.html', category=category, items=items, login_str=login_str, current_user_id=current_user_id)


@app.route('/categories/<int:category_id>/JSON')
def categoryBooksJSON(category_id):
    items = session.query(BookItem).filter_by(
        category_id=category_id).all()
    return jsonify(BookItems=[i.serialize for i in items])


@app.route('/categories/<int:category_id>/book/JSON')
def bookItemJSON(category_id, book_id):
    bookItem = session.query(BookItem).filter_by(id=book_id).one()
    return jsonify(BookItem=bookItem.serialize)


@app.route('/category/<int:category_id>/new/', methods=['GET', 'POST'])
def newBookItem(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    else:
        login_str = "You logged in as %s" % login_session['username']
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        newItem = BookItem(name=request.form['name'],
                           description=request.form['description'],
                           year=request.form['year'],
                           author=request.form['author'],
                           category_id=category_id,
                           user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash("new book item created!")
        return redirect(url_for('categoryBooks', category_id=category_id, login_str=login_str))
    else:
        return render_template('newbookitem.html', category_id=category_id, login_str=login_str)


@app.route('/category/<int:category_id>/<int:book_id>/edit/', methods=['GET', 'POST'])
def editBookItem(category_id, book_id):
    if 'username' not in login_session:
        return redirect('/login')
    else:
        login_str = "You logged in as %s" % login_session['username']
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(BookItem).filter_by(category_id=category.id, id=book_id).one()
    if item.user_id != login_session['user_id']:
        return "You are not Authorized!"
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        if request.form['year']:
            item.year = request.form['year']
        if request.form['author']:
            item.author = request.form['author']
        session.commit()
        flash("book item edited!")
        return redirect(url_for('categoryBooks', category_id=category_id, login_str=login_str))
    else:
        return render_template('editbookitem.html', category_id=category_id, book_id=book_id, item=item, login_str=login_str)


@app.route('/category/<int:category_id>/<int:book_id>/delete/', methods=['GET', 'POST'])
def deleteBookItem(category_id, book_id):
    if 'username' not in login_session:
        return redirect('/login')
    else:
        login_str = "You logged in as %s" % login_session['username']
    category = session.query(Category).filter_by(id=category_id).one()
    book = session.query(BookItem).filter_by(id=book_id).one()
    if book.user_id != login_session['user_id']:
        return "You are not Authorized!"
    item = session.query(BookItem).filter_by(category_id=category.id, id=book_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("book item deleted!")
        return redirect(url_for('categoryBooks', category_id=category_id, login_str=login_str))
    else:
        return render_template('deletebookitem.html', item=item, login_str=login_str)


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():

    access_token = login_session.get('credentials') #.access_token #['access_token']

    print('In gdisconnect access token is %s' % access_token)
    print 'User name is: '
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
