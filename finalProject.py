from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, FastingStatus, MenuItem, Observations

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = scoped_session(DBSession)


# JSON list of all restaurants
@app.route('/restaurants/JSON')
def showRestaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(restaurants=[r.serialize for r in restaurants])


# JSON menu for a specific restaurant
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def showMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    fastingStatus = session.query(FastingStatus).filter_by(restaurant_id = restaurant_id)
    observat = session.query(Observations).filter_by(restaurant_id = restaurant_id)
    return jsonify(Menu=[i.serialize for i in items], FastingStatus=fastingStatus.serialize, \
    	Observations=observat.serialize)


# JSON list of specific menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=menuItem.serialize)

# JSON list of fasting status
@app.route('/restaurant/<int:restaurant_id>/fasting/JSON')
def fastingStatusJSON(restaurant_id):
    fastingStatus = session.query(FastingStatus).filter_by(restaurant_id = restaurant_id).one()
    return jsonify(FastingStatus=fastingStatus.serialize)

# JSON list of observations
@app.route('/restaurant/<int:restaurant_id>/observations/JSON')
def observatJSON(restaurant_id):
    observat = session.query(Observations).filter_by(restaurant_id = restaurant_id).one()
    return jsonify(Observations=observat.serialize)


#1 Root/home page which shows a list of all of the restaurants
@app.route('/')
@app.route('/restaurants')
def showRestaurants():
	restaurants = session.query(Restaurant).all()
	try:
		restaurants 
	except:
		return render_template('restaurants.html')	
	return render_template('restaurants.html', restaurants=restaurants)


#2 home page for a specific restaurant
@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	fastingStatus = session.query(FastingStatus).filter_by(restaurant_id = restaurant_id)
	observat = session.query(Observations).filter_by(restaurant_id = restaurant_id)
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
	try:
		fastingStatus
		observat
		items
	except:
		return render_template('menu.html', restaurant=restaurant) 
	return render_template('menu.html', restaurant=restaurant, items=items, \
		fastingStatus=fastingStatus, observat=observat)


#3 add new restaurant
@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
	if request.method == 'POST':
		newRestaurant=Restaurant(name=request.form['name'])
		session.add(newRestaurant)
		session.commit()
		flash("New restaurant created")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('newRestaurant.html')

	
#4 edit restaurant
@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	editedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		editedRestaurant.name=request.form['name']
		session.add(editedRestaurant)
		session.commit()
		flash("Restaurant name has been changed")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('editRestaurant.html', restaurant=editedRestaurant)



#5 delete restaurant
@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	deletedRestaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		session.delete(deletedRestaurant)
		session.commit()
		flash("Restaurant has been deleted")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('deleteRestaurant.html', restaurant=deletedRestaurant)


#6 add new menu item
@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':		
		newItem = MenuItem(name=request.form['name'], description=request.form['description'], \
			calories=request.form['calories'], course=request.form['course'], restaurant_id=restaurant_id)
		session.add(newItem)
		session.commit()
		flash("Menu item has been added")
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template('newMenuItem.html', restaurant=restaurant)

#7 edit fasting status
@app.route('/restaurant/<int:restaurant_id>/fasting', methods=['GET', 'POST'])
def editFastingStatus(restaurant_id):
	restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		newStatus = FastingStatus(fasting=request.form['fasting'], restaurant_id=restaurant_id)
		session.add(newStatus)
		session.commit()
		flash("Fasting status has been changed")
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template('editFastingStatus.html', restaurant=restaurant)

#8 add observations
@app.route('/restaurant/<int:restaurant_id>/observations', methods=['GET', 'POST'])
def addObservation(restaurant_id):
	restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		newObservation = Observations(description=request.form['description'], restaurant_id=restaurant_id)
		session.add(newObservation)
		session.commit()
		flash("Fasting status has been changed")
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template('addObservation.html', restaurant=restaurant)


#8 edit menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
	editedItem=session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name=request.form['name']
		if request.form['description']:
			editedItem.description=request.form['description']
		if request.form['calories']:
			editedItem.calories=request.form['calories']
		if request.form['course']:
			editedItem.course=request.form['course']
		session.add(editedItem)
		session.commit()
		flash("Menu item has been changed")
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template('editMenuItem.html', restaurant=restaurant, item=editedItem)


#9 delete menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
	deletedItem=session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		session.delete(deletedItem)
		session.commit()
		flash("Menu item has been deleted")
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template('deleteMenuItem.html', restaurant=restaurant, item=deletedItem)
	


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)