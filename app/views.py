import os
from app import app, db, login_manager
from flask import render_template, request, redirect, send_from_directory, url_for, flash, session, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from app.model import UserProfile, PropertyProfile
from app.forms import LoginForm, AddPropertyForm


###########################################################################################################################
## Normal Routes ##
###########################################################################################################################
@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Shadean Payton")

###########################################################################################################################
## Form and Database Upload ##
###########################################################################################################################
@app.route('/properties/create', methods=['POST', 'GET'])
@login_required
def new_property():
    form = AddPropertyForm()

    if form.validate_on_submit() and request.method == 'POST':
        property_title = form.title.data
        property_description = form.description.data
        number_rooms = form.num_rooms.data
        number_bathrooms = form.num_bathrooms.data
        property_price = form.price.data
        property_type = form.property_type.data
        property_location = form.location.data
        property_photo = form.photo.data
        
        #for photo
        filename = secure_filename(property_photo.filename)
        property_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        #add to database
        add_property = PropertyProfile(request.form['property_title'], request.form['property_description'], request.form['number_rooms'], 
                                       request.form['number_bathrooms'], request.form['property_price'], request.form['property_type'], 
                                       request.form['property_location'], filename)
        db.session.add(add_property)
        db.session.commit()

        #flash and redirect
        flash('Property was successfully added', 'success')
        return redirect(url_for('properties'))
    return render_template('add_properties.html', form=form)

@app.route('/properties')
#@login_required
def properties():
    all_properties = db.session.execute(db.select(PropertyProfile)).scalars()
    if all_properties is not None:
        return render_template('properties.html', all_properties=all_properties)
    flash('Not seeing Property', 'error')
    return redirect(url_for('new_property'))

@app.route('/properties/<propertyid>')
#@login_required
def get_property(propertyid):
    current_property = db.session.execute(db.select(PropertyProfile).filter_by(property_id=propertyid)).scalar_one()
    if current_property is not None:
        return render_template('full_property.html', current_property=current_property)
    flash('This property seems to be missing', 'error')
    return redirect(url_for('properties'))

@app.route('/uploads/<filename>')
def get_image(filename):
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, app.config['UPLOAD_FOLDER']), filename)

###########################################################################################################################
##Login and Logout User ##
###########################################################################################################################
@app.route('/login', methods=['POST', 'GET'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('properties'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = db.session.execute(db.select(UserProfile).filter_by(username=username)).scalar()
        if user is not None and check_password_hash(user.password, password):

        # Gets user id, load into session
            login_user(user)
            flash(f'User {username} has successfully logged in!!!')
            return redirect(url_for("properties"))
        else:
            flash(f'User {username} was not logged in !!')
            return redirect(url_for('home'))
    return render_template("login.html", form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are successfully logged out')
    return redirect(url_for('home'))

@login_manager.user_loader
def load_user(id):
    return db.session.execute(db.select(UserProfile).filter_by(id=id)).scalar()


######################################################################
###
# The functions below should be applicable to all Flask apps.
###

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
