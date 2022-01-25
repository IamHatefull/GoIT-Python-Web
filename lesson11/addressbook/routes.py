from flask import render_template, request, redirect, url_for
from addressbook import app, db
from addressbook.models import Contact
from datetime import datetime
#from addressbook.models import Session, Contact

'''@app.route('/')
@app.route('/about', methods=['GET', 'POST'])
def about():
    contacts = Contact.query.all()
    return render_template('about.html', contacts = contacts)'''






@app.route('/')
@app.route('/about', methods=['GET', 'POST'])
def about():
    contacts = Contact.query.all()
    return render_template('about.html', contacts = contacts)

@app.route('/about/new/', methods=['GET', 'POST'])
def new_contact():
    if request.method == 'POST':
        new_contact = Contact(name=request.form['name'], phone=request.form['phone'],
                             birthday=datetime.strptime(request.form['birthday'], '%Y-%m-%d').date(), email=request.form['email'],
                             address=request.form['address'])
        db.session.add(new_contact)
        db.session.commit()
        return redirect(url_for('about'))
    else:
        return render_template('add_contact.html')


@app.route("/about/<int:contact_id>/edit/", methods=['GET', 'POST'])
def update_contact(contact_id):
    editedContact = Contact.query.filter_by(id=contact_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedContact.name = request.form['name']
        if request.form['phone']:
            editedContact.phone = request.form['phone']
        if request.form['birthday']:
            editedContact.birthday = datetime.strptime(request.form['birthday'], '%Y-%m-%d').date()
        if request.form['email']:
            editedContact.email = request.form['email']
        if request.form['address']:
            editedContact.address = request.form['address']
        return redirect(url_for('about'))
    else:
        return render_template('update_contact.html', contact=editedContact)


@app.route('/about/<int:contact_id>/delete/')
def delete_contact(contact_id):
    contact_to_delete = Contact.query.filter_by(id=contact_id).one()
    db.session.delete(contact_to_delete)
    db.session.commit()
    return redirect(url_for('about', contact_id=contact_id))
    