from app import app, db
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required

from app.forms.radius import NasForm, GroupForm
from app.models.radius import (
    Nas, RadUserGroup, RadGroupCheck, RadGroupReply
)
from app.models.auth import Group

# NAS pages
@app.route('/nas')
@login_required
def list_nas():
    table_headers = ("#", "Name", "Short name", "Server", "Ports",
                     "Secret", "Type", "Community", "Description",
                     "Actions")

    page = int(request.args.get('page', 1))
    records = db.session.query(Nas).paginate(page=page)

    return render_template(
        'radius/list_nas.html',
        table_headers=table_headers,
        table_records=records.items,
        pagination=records
    )

@app.route('/nas/new', methods=['GET', 'POST'])
@login_required
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
        form_errors=form.errors,
        action='add'
    )

@app.route('/nas/edit/<int:nas_id>', methods=['GET', 'POST'])
@login_required
def edit_nas(nas_id):
    nas = db.session.query(Nas).get_or_404(nas_id)
    form = NasForm()

    if form.validate_on_submit():
        nas.nasname = form.name.data
        nas.shortname = form.short_name.data
        nas.type = form.type.data
        nas.ports = form.ports.data
        nas.secret = form.secret.data
        nas.server = form.server.data
        nas.community = form.community.data
        nas.description = form.description.data
        db.session.commit()
        flash('NAS data updated')
        return redirect(url_for('list_nas'))
    elif form.errors:
        flash('Form has errors')
    elif request.method == 'GET':
        form.name.data = nas.nasname
        form.short_name.data = nas.shortname
        form.type.data = nas.type
        form.ports.data = nas.ports
        form.secret.data = nas.secret
        form.server.data = nas.server
        form.community.data = nas.community
        form.description.data = nas.description
    
    return render_template(
        'radius/nas_form.html',
        form=form,
        form_errors=form.errors,
        action='edit'
    )

@app.route('/nas/delete/<int:nas_id>')
@login_required
def delete_nas(nas_id):
    nas = db.session.query(Nas).get_or_404(nas_id)
    db.session.delete(nas)
    db.session.commit()
    return redirect(url_for('list_nas'))

# Groups pages
@app.route('/groups')
@login_required
def list_groups():
    table_headers = ("#", "Group Name", "Description",
                     "Checks Count", "Replies Count",
                     "Actions")

    page = int(request.args.get('page', 1))
    records = Group.query.paginate(page=page)
    
    for record in records.items:
        record.checks = db.session.query(RadGroupCheck).filter_by(
            groupname=record.name
        ).count()
        record.replies = db.session.query(RadGroupReply).filter_by(
            groupname=record.name
        ).count()

    return render_template(
        'radius/list_groups.html',
        table_headers=table_headers,
        table_records=records.items,
        pagination=records
    )

@app.route('/groups/new', methods=['GET', 'POST'])
@login_required
def new_group():
    form = GroupForm()

    if form.validate_on_submit():
        db.session.add(Group(
            name=form.name.data,
            description=form.description.data
        ))
        db.session.commit()
        flash('New group added')
        return redirect(url_for('list_groups'))
    elif form.errors:
        flash('Form has errors')

    return render_template(
        'radius/group_form.html',
        form=form,
        form_errors=form.errors,
        action='add'
    )

@app.route('/groups/edit/<int:group_id>', methods=['GET', 'POST'])
@login_required
def edit_group(group_id):
    group = Group.query.get_or_404(group_id)
    form = GroupForm()

    if form.validate_on_submit():
        group.name = form.name.data
        group.description = form.description.data
        db.session.commit()
        flash('Group data updated')
        return redirect(url_for('list_groups'))
    elif form.errors:
        flash('Form has errors')
    elif request.method == 'GET':
        form.name.data = group.name
        form.description.data = group.description
    
    return render_template(
        'radius/group_form.html',
        form=form,
        form_errors=form.errors,
        action='edit'
    )

@app.route('/groups/delete/<int:group_id>')
@login_required
def delete_group(group_id):
    group = Group.query.get_or_404(group_id)
    db.session.delete(group)
    db.session.commit()
    return redirect(url_for('list_groups'))

# Group checks and replies pages
@app.route('/groups/<int:group_id>')
@login_required
def group_details(group_id):
    group = Group.query.get_or_404(group_id)
    checks = db.session.query(RadGroupCheck).all()
    replies = db.session.query(RadGroupReply).all()
    return render_template(
        'radius/group_details.html',
        group=group,
        checks=checks,
        replies=replies
    )