import os.path
import uuid
import csv

from app import app, db
from flask import (
    render_template, flash, redirect,
    url_for, request, send_from_directory
)
from flask_babel import _
from sqlalchemy.sql.expression import desc

from app.forms.radius import (
    NasForm, GroupForm, AttributeForm,
    UserForm
)
from app.models.radius import (
    Nas, RadUserGroup, RadGroupCheck, RadGroupReply,
    RadCheck, RadReply, RadPostAuth
)
from app.models.auth import Group, User
from app.utils import has_access


# Dashboard
@app.route('/')
@has_access()
def index():
    auth_info = db.session.query(RadPostAuth)\
        .order_by(desc('authdate'))\
        .limit(20).all()

    return render_template(
        'radius/dashboard.html',
        auth_info=auth_info
    )

# NAS pages
@app.route('/nas')
@has_access()
def list_nas():
    table_headers = ("#", _("Name"), _("Short name"), _("Server"), _("Ports"),
                     _("Secret"), _("Type"), _("Community"), _("Description"),
                     _("Actions"))

    page = int(request.args.get('page', 1))
    records = db.session.query(Nas).paginate(page=page)

    return render_template(
        'radius/list_nas.html',
        table_headers=table_headers,
        table_records=records.items,
        pagination=records
    )

@app.route('/nas/csv')
@has_access()
def download_nas_csv():
    filedir = '/tmp'
    filename = str(uuid.uuid4()) + '.csv'
    filepath = os.path.join(filedir, filename)

    nas_list = db.session.query(Nas).all()

    if not len(nas_list):
        flash(_('There are no records to export.'), 'error')
        return redirect(url_for('list_nas'))
    
    with open(filepath, 'w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';', quotechar='"')
        headers = [
            'id', 'nasname', 'shortname',
            'type', 'ports', 'secret',
            'server', 'community', 'description'
        ]
        csv_writer.writerow(headers)

        for row in nas_list:
            csv_writer.writerow([
                row.id, row.nasname, row.shortname,
                row.type, row.ports, row.secret,
                row.server, row.community, row.description
            ])
        
    return send_from_directory(
        filedir,
        filename,
        as_attachment=True
    )

@app.route('/nas/new', methods=['GET', 'POST'])
@has_access()
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
        flash(_('New NAS added'), 'success')
        return redirect(url_for('list_nas'))
    elif form.errors:
        print(form.errors)
        flash(_('Form has errors'), 'error')
    
    return render_template(
        'radius/nas_form.html',
        form=form,
        form_errors=form.errors,
        action='add'
    )

@app.route('/nas/edit/<int:nas_id>', methods=['GET', 'POST'])
@has_access()
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
        flash(_('NAS data updated'), 'success')
        return redirect(url_for('list_nas'))
    elif form.errors:
        flash(_('Form has errors'), 'error')
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
@has_access()
def delete_nas(nas_id):
    nas = db.session.query(Nas).get_or_404(nas_id)
    db.session.delete(nas)
    db.session.commit()
    return redirect(url_for('list_nas'))

# Groups pages
@app.route('/groups')
@has_access()
def list_groups():
    table_headers = ("#", _("Group Name"), _("Description"),
                     _("Checks Count"), _("Replies Count"),
                     _("Actions"))

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
@has_access()
def new_group():
    form = GroupForm()

    if form.validate_on_submit():
        db.session.add(Group(
            name=form.name.data,
            description=form.description.data
        ))
        db.session.commit()
        flash(_('New group added'), 'success')
        return redirect(url_for('list_groups'))
    elif form.errors:
        flash(_('Form has errors'), 'error')

    return render_template(
        'radius/group_form.html',
        form=form,
        form_errors=form.errors,
        action='add'
    )

@app.route('/groups/edit/<int:group_id>', methods=['GET', 'POST'])
@has_access()
def edit_group(group_id):
    group = Group.query.get_or_404(group_id)
    form = GroupForm()

    if form.validate_on_submit():
        group.name = form.name.data
        group.description = form.description.data
        db.session.commit()
        flash(_('Group data updated'), 'success')
        return redirect(url_for('list_groups'))
    elif form.errors:
        flash(_('Form has errors'), 'error')
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
@has_access()
def delete_group(group_id):
    group = Group.query.get_or_404(group_id)

    users_group = db.session.query(RadUserGroup).filter_by(
        groupname=group.name
    ).all()
    for user_group in users_group:
        db.session.delete(user_group)

    group_checks = db.session.query(RadGroupCheck).filter_by(
        groupname=group.name
    ).all()
    for check in group_checks:
        db.session.delete(check)

    group_replies = db.session.query(RadGroupReply).filter_by(
        groupname=group.name
    ).all()
    for reply in group_replies:
        db.session.delete(reply)

    db.session.delete(group)
    db.session.commit()
    return redirect(url_for('list_groups'))

# Group checks and replies pages
@app.route('/groups/<int:group_id>')
@has_access()
def group_details(group_id):
    group = Group.query.get_or_404(group_id)

    checks_page = int(request.args.get('checks_page', 1))
    check_records = db.session.query(RadGroupCheck).filter_by(
        groupname=group.name
    ).paginate(
        page=checks_page,
        per_page=10
    )

    replies_page = int(request.args.get('replies_page', 1))
    reply_records = db.session.query(RadGroupReply).filter_by(
        groupname=group.name
    ).paginate(
        page=replies_page,
        per_page=10
    )

    return render_template(
        'radius/group_details.html',
        group=group,
        checks=check_records.items,
        replies=reply_records.items,
        checks_pagination=check_records,
        replies_pagination=reply_records
    )

@app.route('/groups/<int:group_id>/checks/new', methods=['GET', 'POST'])
@has_access()
def new_group_check(group_id):
    group = Group.query.get_or_404(group_id)
    form = AttributeForm()

    if form.validate_on_submit():
        data_type = form.processed_fields.data

        if data_type == 'ca-cv':
            db.session.add(RadGroupCheck(
                groupname=group.name,
                attribute=form.custom_attribute.data,
                op=form.operation.data,
                value=form.custom_value.data
            ))
            db.session.commit()
        elif data_type == 'sa-cv':
            db.session.add(RadGroupCheck(
                groupname=group.name,
                attribute=form.attribute.data,
                op=form.operation.data,
                value=form.custom_value.data
            ))
            db.session.commit()
        elif data_type == 'sa-sv':
            db.session.add(RadGroupCheck(
                groupname=group.name,
                attribute=form.attribute.data,
                op=form.operation.data,
                value=form.value.data
            ))
            db.session.commit()
        else:
            flash(_('Unable to process attribute'), 'error')
            return redirect(url_for('new_group_check', group_id=group_id))
        return redirect(url_for('group_details', group_id=group_id))
    elif form.errors:
        flash(_('Form has errors'), 'error')

    return render_template(
        'radius/group_attribute_form.html',
        group=group,
        form=form,
        form_errors=form.errors,
        type='check'
    )

@app.route('/groups/<int:group_id>/replies/new', methods=['GET', 'POST'])
@has_access()
def new_group_reply(group_id):
    group = Group.query.get_or_404(group_id)
    form = AttributeForm()

    if form.validate_on_submit():
        data_type = form.processed_fields.data

        if data_type == 'ca-cv':
            db.session.add(RadGroupReply(
                groupname=group.name,
                attribute=form.custom_attribute.data,
                op=form.operation.data,
                value=form.custom_value.data
            ))
            db.session.commit()
        elif data_type == 'sa-cv':
            db.session.add(RadGroupReply(
                groupname=group.name,
                attribute=form.attribute.data,
                op=form.operation.data,
                value=form.custom_value.data
            ))
            db.session.commit()
        elif data_type == 'sa-sv':
            db.session.add(RadGroupReply(
                groupname=group.name,
                attribute=form.attribute.data,
                op=form.operation.data,
                value=form.value.data
            ))
            db.session.commit()
        else:
            flash(_('Unable to process attribute'), 'error')
            return redirect(url_for('new_group_reply', group_id=group_id))
        return redirect(url_for('group_details', group_id=group_id))
    elif form.errors:
        flash(_('Form has errors'), 'error')

    return render_template(
        'radius/group_attribute_form.html',
        group=group,
        form=form,
        form_errors=form.errors,
        type='reply'
    )

@app.route('/groups/<int:group_id>/checks/<int:group_check_id>/delete', methods=['GET', 'POST'])
@has_access()
def delete_group_check(group_id, group_check_id):
    group_check = db.session.query(RadGroupCheck).get_or_404(group_check_id)
    db.session.delete(group_check)
    db.session.commit()
    return redirect(url_for('group_details', group_id=group_id))

@app.route('/groups/<int:group_id>/replies/<int:group_reply_id>/delete', methods=['GET', 'POST'])
@has_access()
def delete_group_reply(group_id, group_reply_id):
    group_reply = db.session.query(RadGroupReply).get_or_404(group_reply_id)
    db.session.delete(group_reply)
    db.session.commit()
    return redirect(url_for('group_details', group_id=group_id))

# Users pages
@app.route('/users')
@has_access()
def list_users():
    table_headers = ("#", _("Username"), _("Group"),
                     _("Checks Count"), _("Replies Count"),
                     _("Status"), _("Access"), _("Actions"))

    page = int(request.args.get('page', 1))
    records = User.query.paginate(page=page)
    
    for record in records.items:
        user_group = db.session.query(RadUserGroup).filter_by(
            username=record.username
        ).first()
        if user_group:
            record.group = Group.query.filter_by(
                name=user_group.groupname
            ).first()
        else:
            record.group = None

        record.checks = db.session.query(RadCheck).filter_by(
            username=record.username
        ).count()
        record.replies = db.session.query(RadReply).filter_by(
            username=record.username
        ).count()

    return render_template(
        'radius/list_users.html',
        table_headers=table_headers,
        table_records=records.items,
        pagination=records
    )

@app.route('/users/new', methods=['GET', 'POST'])
@has_access()
def new_user():
    groups = Group.query.all()
    
    form = UserForm()
    form.group.choices = [(group.name, group.name) for group in groups]

    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            active=form.active.data,
            name=form.name.data,
            phone=form.phone.data,
            address=form.address.data,
            has_access=form.has_access.data
        )
        user.hash_password()
        db.session.add(user)

        db.session.add(RadUserGroup(
            username=form.username.data,
            groupname=form.group.data,
            priority=0
        ))
        
        db.session.add(RadCheck(
            username=form.username.data,
            attribute='Cleartext-Password',
            op=':=',
            value=form.password.data
        ))

        if not form.active.data:
            db.session.add(RadCheck(
                username=form.username.data,
                attribute='Auth-Type',
                op=':=',
                value='Reject'
            ))

        db.session.commit()

        flash(_('New user added'), 'success')
        return redirect(url_for('list_users'))
    elif form.errors:
        flash(_('Form has errors'), 'error')

    return render_template(
        'radius/user_form.html',
        form=form,
        form_errors=form.errors,
        action='add'
    )

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@has_access()
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    user_group = db.session.query(RadUserGroup).filter_by(
        username=user.username
    ).first()
    groups = Group.query.all()

    if user_group:
        filter_groups = [g for g in groups if g.name == user_group.groupname]
        group = filter_groups[0] if len(filter_groups) else None
    else:
        group = None

    form = UserForm()
    form.group.choices = [(group.name, group.name) for group in groups]
    form.username.render_kw = {'readonly': True}

    if form.validate_on_submit():
        user.email = form.email.data
        user.active = form.active.data
        user.name = form.name.data
        user.phone = form.phone.data
        user.address = form.address.data
        user.has_access = form.has_access.data
        
        # update password
        if len(form.password.data):
            user.password = form.password.data
            user.hash_password()
            
            pass_att = db.session.query(RadCheck).filter(
                RadCheck.username == user.username,
                RadCheck.attribute == 'Cleartext-Password'
            ).first()
            pass_att.value = form.password.data

        # insert or update group
        if not group and form.group.data:
            db.session.add(RadUserGroup(
                username=form.username.data,
                groupname=form.group.data,
                priority=0
            ))
        elif group and group.name != form.group.data:
            db.session.delete(user_group)
            db.session.add(RadUserGroup(
                username=form.username.data,
                groupname=form.group.data,
                priority=0
            ))

        # update access
        user_access_list = db.session.query(RadCheck).filter(
            RadCheck.username == user.username,
            RadCheck.attribute == 'Auth-Type'
        ).all()
        if not len(user_access_list) and not form.active.data:
            # user is disabled and auth-type is default
            # should change auth-type to 'reject'
            db.session.add(RadCheck(
                username=user.username,
                attribute='Auth-Type',
                op=':=',
                value='Reject'
            ))
        elif not len(user_access_list) and form.active.data:
            # user is enabled and auth-type is default
            pass
        elif len(user_access_list):
            # auth-type is not default
            is_disabled = 'Reject' in [a.value for a in user_access_list]
            if not form.active.data and not is_disabled:
                # auth-type is 'accept' but user is disabled
                db.session.add(RadCheck(
                    username=user.username,
                    attribute='Auth-Type',
                    op=':=',
                    value='Reject'
                ))
            elif not form.active.data and is_disabled:
                # auth-type is 'reject' and user is disabled
                pass
            elif form.active.data and not is_disabled:
                # auth-type is 'accept' and user is not disabled
                pass
            elif form.active.data and is_disabled:
                # auth-type is 'reject' but user is not disabled
                for access in user_access_list:
                    if access.value == 'Reject':
                        db.session.delete(access)

        db.session.commit()

        flash(_('User data updated'), 'success')
        return redirect(url_for('list_users'))
    elif form.errors:
        flash(_('Form has errors'), 'error')
    else:
        form.username.data = user.username
        form.email.data = user.email
        form.active.data = user.active
        form.name.data = user.name
        form.phone.data = user.phone
        form.address.data = user.address
        form.has_access.data = user.has_access
        
        if group:
            form.group.data = group.name

    return render_template(
        'radius/user_form.html',
        form=form,
        form_errors=form.errors,
        action='edit'
    )

@app.route('/users/<int:user_id>/delete')
@has_access()
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    user_group = db.session.query(RadUserGroup).filter_by(
        username=user.name
    ).first()
    if user_group:
        db.session.delete(user_group)

    user_checks = db.session.query(RadCheck).filter_by(
        username=user.username
    ).all()
    for check in user_checks:
        db.session.delete(check)

    user_replies = db.session.query(RadReply).filter_by(
        username=user.username
    ).all()
    for reply in user_replies:
        db.session.delete(reply)

    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('list_users'))

# User checks and replies pages
@app.route('/users/<int:user_id>')
@has_access()
def user_details(user_id):
    user = User.query.get_or_404(user_id)

    checks_page = int(request.args.get('checks_page', 1))
    check_records = db.session.query(RadCheck).filter_by(
        username=user.username
    ).paginate(
        page=checks_page,
        per_page=10
    )

    replies_page = int(request.args.get('replies_page', 1))
    reply_records = db.session.query(RadReply).filter_by(
        username=user.username
    ).paginate(
        page=replies_page,
        per_page=10
    )

    return render_template(
        'radius/user_details.html',
        user=user,
        checks=check_records.items,
        replies=reply_records.items,
        checks_pagination=check_records,
        replies_pagination=reply_records
    )

@app.route('/users/<int:user_id>/checks/new', methods=['GET', 'POST'])
@has_access()
def new_user_check(user_id):
    user = User.query.get_or_404(user_id)
    form = AttributeForm()

    if form.validate_on_submit():
        data_type = form.processed_fields.data

        if data_type == 'ca-cv':
            db.session.add(RadCheck(
                username=user.username,
                attribute=form.custom_attribute.data,
                op=form.operation.data,
                value=form.custom_value.data
            ))
            db.session.commit()
        elif data_type == 'sa-cv':
            db.session.add(RadCheck(
                username=user.username,
                attribute=form.attribute.data,
                op=form.operation.data,
                value=form.custom_value.data
            ))
            db.session.commit()
        elif data_type == 'sa-sv':
            db.session.add(RadCheck(
                username=user.username,
                attribute=form.attribute.data,
                op=form.operation.data,
                value=form.value.data
            ))
            db.session.commit()
        else:
            flash(_('Unable to process attribute'), 'error')
            return redirect(url_for('new_user_check', user_id=user_id))
        return redirect(url_for('user_details', user_id=user_id))
    elif form.errors:
        flash(_('Form has errors'), 'error')

    return render_template(
        'radius/user_attribute_form.html',
        user=user,
        form=form,
        form_errors=form.errors,
        type='check'
    )

@app.route('/users/<int:user_id>/replies/new', methods=['GET', 'POST'])
@has_access()
def new_user_reply(user_id):
    user = User.query.get_or_404(user_id)
    form = AttributeForm()

    if form.validate_on_submit():
        data_type = form.processed_fields.data

        if data_type == 'ca-cv':
            db.session.add(RadReply(
                username=user.username,
                attribute=form.custom_attribute.data,
                op=form.operation.data,
                value=form.custom_value.data
            ))
            db.session.commit()
        elif data_type == 'sa-cv':
            db.session.add(RadReply(
                username=user.username,
                attribute=form.attribute.data,
                op=form.operation.data,
                value=form.custom_value.data
            ))
            db.session.commit()
        elif data_type == 'sa-sv':
            db.session.add(RadReply(
                username=user.username,
                attribute=form.attribute.data,
                op=form.operation.data,
                value=form.value.data
            ))
            db.session.commit()
        else:
            flash(_('Unable to process attribute'), 'error')
            return redirect(url_for('new_user_reply', user_id=user_id))
        return redirect(url_for('user_details', user_id=user_id))
    elif form.errors:
        flash(_('Form has errors'), 'error')

    return render_template(
        'radius/user_attribute_form.html',
        user=user,
        form=form,
        form_errors=form.errors,
        type='reply'
    )

@app.route('/user/<int:user_id>/checks/<int:user_check_id>/delete', methods=['GET', 'POST'])
@has_access()
def delete_user_check(user_id, user_check_id):
    user_check = db.session.query(RadCheck).get_or_404(user_check_id)
    if user_check.attribute == 'Auth-Type' and user_check.value == 'Reject':
        user = User.query.get(user_id)
        user.active = True
        db.session.delete(user_check)
        db.session.commit()
    elif not user_check.attribute in ['Cleartext-Password']:
        db.session.delete(user_check)
        db.session.commit()
    return redirect(url_for('user_details', user_id=user_id))

@app.route('/users/<int:user_id>/replies/<int:user_reply_id>/delete', methods=['GET', 'POST'])
@has_access()
def delete_user_reply(user_id, user_reply_id):
    user_reply = db.session.query(RadReply).get_or_404(user_reply_id)
    if not user_reply.attribute in ['Cleartext-Password']:
        db.session.delete(user_reply)
        db.session.commit()
    return redirect(url_for('user_details', user_id=user_id))
