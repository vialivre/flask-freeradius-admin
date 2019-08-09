from app import app, db
from flask import render_template, flash, redirect, url_for

from app.forms.radius import NasForm
from app.models.radius import Nas

@app.route('/nas')
def list_nas():
    table_headers = ("#", "Name", "Short name", "Server", "Ports",
                     "Secret", "Type", "Community", "Description")

    records = db.session.query(Nas).all()

    return render_template(
        'radius/list_nas.html',
        table_headers=table_headers,
        table_records=records
    )

@app.route('/nas/new', methods=['GET', 'POST'])
def new_nas():
    form = NasForm()

    if form.validate_on_submit():
        db.session.add(Nas(
            nasname=form.name.data,
            shortname=form.short_name.data,
            type=form.type.data,
            ports=form.ports.data,
            secret=form.secret.data,
            server=form.server.data,
            community=form.community.data,
            description=form.description.data
        ))
        db.session.commit()
        flash('New NAS added')
        return redirect(url_for('list_nas'))
    elif form.errors:
        flash('Form has errors')
    
    return render_template(
        'radius/nas_form.html',
        form=form,
        form_errors=form.errors
    )