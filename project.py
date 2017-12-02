import httplib2
import json
from flask import make_response
import requests
from flask import Flask, g, render_template, request, redirect, url_for, \
    jsonify, flash
from sqlalchemy import create_engine, asc
from functools import wraps
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError


app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "ItemCatalog"

engine = create_engine('sqlite:///categoryitemlist.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# Authentication and login using google account.
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

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps("""Current user is already
        connected."""), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
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
    output += """ " style = "width: 300px; height: 300px;
     border-radius: 150px;-webkit-border-radius: 150px;
     -moz-border-radius: 150px;"> """
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


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


# JSON end point showing items under a category
@app.route('/categories/<int:category_id>/menu/JSON')
def itemCatalogJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(
        category_id=category_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


# JSON end point showing information of an item
@app.route('/categories/<int:id>/menu/JSON')
def itemJSON(id):
    item = session.query(Item).filter_by(item_name=item_name).one()
    return jsonify(MenuItems=item.serialize)


# logout using google account.
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Display Categories and newly added items of the categories.
@app.route('/')
@app.route('/categories/')
def categoriesList():
    print("hello")
    category_list = session.query(Category).all()
    items_list = session.query(Item).all()
    n = -1
    a = list()
    b = list()
    # adding items and their respective category name of
    # five newly added items in lists.
    while n > -6:
        a.append(items_list[n].item_name)
        catgory = session.query(Category).filter_by(
            id=items_list[n].category_id).one()
        b.append(catgory.category_name)
        n -= 1
    return render_template('homepage.html',
                           category_list=category_list, a=a, b=b)


# Display items under a particular category.
@app.route('/catalog/<string:category_name>/items/')
def viewItems(category_name):
    category_list = session.query(Category).all()
    category = session.query(Category).filter_by(
        category_name=category_name).one()
    items = session.query(Item).filter_by(category_id=category.id).all()
    return render_template('viewItems.html',
                           category_list=category_list,
                           items=items,
                           category_name=category_name)


# Display Item Information.
@app.route('/catalog/<string:category_name>/<string:item_name>/')
def viewItemInfo(category_name, item_name):
    item = session.query(Item).filter_by(item_name=item_name).one()
    return render_template('viewItemInfo.html', item_name=item_name, item=item)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in login_session:
            return f(*args, **kwargs)
        else:
            flash("You are not allowed to access there")
            return redirect('/login')
    return decorated_function


# Add Item.
@app.route('/catalog/addItem/', methods=['GET', 'POST'])
@login_required
def addItem():
    if request.method == 'POST':
        newItem = Item(
            item_name=request.form['title'],
            description=request.form['description'],
            category_id=request.form[str('comp_select')],
            user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash("Item Successfully added")
        return redirect(url_for('categoriesList'))
    else:
        category_list = session.query(Category).all()
        return render_template('newitem.html', category_list=category_list)


# Edit Item.
@app.route('/catalog/<string:item_name>/edit/', methods=['GET', 'POST'])
@login_required
def editItem(item_name):
    item = session.query(Item).filter_by(item_name=item_name).one()
    if item.user_id != login_session['user_id']:
        return render_template('editAlert.html')
        return redirect(url_for('categoriesList'))
    if request.method == 'POST':
        if request.form['title']:
            item.item_name = request.form['title']
        if request.form['description']:
            item.description = request.form['description']
        if request.form['comp_select']:
            item.category_id = request.form[str('comp_select')]
        session.add(item)
        session.commit()
        flash("Item Successfully Edited")
        return redirect(url_for('categoriesList'))
    else:
        category_list = session.query(Category).all()
        return render_template('editItem.html',
                               item=item,
                               category_list=category_list)


# Delete Item.
@app.route('/catalog/<string:item_name>/delete/', methods=['GET', 'POST'])
@login_required
def deleteItem(item_name):
    item = session.query(Item).filter_by(item_name=item_name).one()
    if item.user_id != login_session['user_id']:
        return render_template('deleteAlert.html')
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('categoriesList'))
    else:
        return render_template('deleteItem.html', item=item)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5656)
