# coding: utf-8

import copy

from flask.ext import login
from flask.ext import wtf
from google.appengine.ext import ndb
import flask
import wtforms

import auth
import cache
import config
import model
import task
import util

from main import app


###############################################################################
# User List
###############################################################################
@app.route('/admin/users/')
@auth.admin_required
def user_list():
    user_dbs, user_cursor = model.User.get_dbs(email=util.param('email'))
    permissions = list(UserUpdateForm._permission_choices)
    permissions += util.param('permissions', list) or []
    return flask.render_template(
        'user/user_list.html',
        html_class='user-list',
        title=u'Хэрэглэгчийн жагсаалт',
        user_dbs=user_dbs,
        next_url=util.generate_next_url(user_cursor),
        api_url=flask.url_for('api.users'),
        permissions=sorted(set(permissions)),
    )


###############################################################################
# User Update
###############################################################################
class UserUpdateForm(wtf.Form):
    username = wtforms.StringField(
        'Username',
        [wtforms.validators.required(), wtforms.validators.length(min=3)],
        filters=[util.email_filter],
    )
    name = wtforms.StringField(
        'Name',
        [wtforms.validators.required()], filters=[util.strip_filter],
    )
    email = wtforms.StringField(
        'Email',
        [wtforms.validators.optional(), wtforms.validators.email()],
        filters=[util.email_filter],
    )
    admin = wtforms.BooleanField('Admin')
    active = wtforms.BooleanField('Active')
    verified = wtforms.BooleanField('Verified')
    permissions = wtforms.SelectMultipleField(
        'Permissions',
        filters=[util.sort_filter],
    )

    _permission_choices = set()

    def __init__(self, *args, **kwds):
        super(UserUpdateForm, self).__init__(*args, **kwds)
        self.permissions.choices = [
            (p, p) for p in sorted(UserUpdateForm._permission_choices)
        ]

    @auth.permission_registered.connect
    def _permission_registered_callback(sender, permission):
        UserUpdateForm._permission_choices.add(permission)


@app.route('/admin/user/create/', methods=['GET', 'POST'])
@app.route('/admin/user/<int:user_id>/update/', methods=['GET', 'POST'])
@auth.admin_required
def user_update(user_id=0):
    if user_id:
        user_db = model.User.get_by_id(user_id)
    else:
        user_db = model.User(name='', username='')
    if not user_db:
        flask.abort(404)

    form = UserUpdateForm(obj=user_db)
    for permission in user_db.permissions:
        form.permissions.choices.append((permission, permission))
    form.permissions.choices = sorted(set(form.permissions.choices))
    if form.validate_on_submit():
        if not util.is_valid_username(form.username.data):
            form.username.errors.append(u'Хэрэглэгчийн нэр буруу байна.')
        elif not model.User.is_username_available(form.username.data, user_db.key):
            form.username.errors.append(u'Хэрэглэгчийн нэр ашиглагдаж байна.')
        else:
            form.populate_obj(user_db)
            if auth.current_user_key() == user_db.key:
                user_db.admin = True
                user_db.active = True
            user_db.put()
            return flask.redirect(flask.url_for(
                'user_list', order='-modified', active=user_db.active,
            ))

    return flask.render_template(
        'user/user_update.html',
        title=user_db.name or u'Шинэ Хэрэглэгч',
        html_class='user-update',
        form=form,
        user_db=user_db,
        api_url=flask.url_for('api.user', user_key=user_db.key.urlsafe()) if user_db.key else ''
    )


###############################################################################
# User Verify
###############################################################################
@app.route('/user/verify/<token>/')
@auth.login_required
def user_verify(token):
    user_db = auth.current_user_db()
    if user_db.token != token:
        flask.flash(u'Холбоос буруу эсвэл хугацаа нь дууссан байна.', category='danger')
        return flask.redirect(flask.url_for('profile'))
    user_db.verified = True
    user_db.token = util.uuid()
    user_db.put()
    flask.flash(u'Баярлалаа! Таны цахим шуудан баталгаажлаа.', category='success')
    return flask.redirect(flask.url_for('profile'))


###############################################################################
# User Forgot
###############################################################################
class UserForgotForm(wtf.Form):
    email = wtforms.StringField(
        u'Цахим шуудан',
        [wtforms.validators.required(), wtforms.validators.email()],
        filters=[util.email_filter],
    )
    recaptcha = wtf.RecaptchaField()


@app.route('/user/forgot/', methods=['GET', 'POST'])
def user_forgot(token=None):
    if not config.CONFIG_DB.has_email_authentication:
        flask.abort(418)

    form = auth.form_with_recaptcha(UserForgotForm(obj=auth.current_user_db()))
    if form.validate_on_submit():
        cache.bump_auth_attempt()
        email = form.email.data
        user_dbs, _ = util.get_dbs(
            model.User.query(), email=email, active=True, limit=2,
        )
        count = len(user_dbs)
        if count == 1:
            task.reset_password_notification(user_dbs[0])
            return flask.redirect(flask.url_for('welcome'))
        elif count == 0:
            form.email.errors.append(u'Имэйл хаяг олдсонгүй')
        elif count == 2:
            task.email_conflict_notification(email)
            form.email.errors.append(
                u'''Уучлаарай таны дансанд давхардал үүссэн байна. Бид нэн даруй хариуцсан
                ажилтанд мэдэгдсэн болно. Тусламжийн ажилтан тантай аль болох хурдан
                холбогдох болно.'''
            )

    if form.errors:
        cache.bump_auth_attempt()

    return flask.render_template(
        'user/user_forgot.html',
        title=u'Нууц үгээ мартсан уу?',
        html_class='user-forgot',
        form=form,
    )


###############################################################################
# User Reset
###############################################################################
class UserResetForm(wtf.Form):
    new_password = wtforms.StringField(
        u'Шинэ нууц үг',
        [wtforms.validators.required(), wtforms.validators.length(min=6)],
    )


@app.route('/user/reset/<token>/', methods=['GET', 'POST'])
@app.route('/user/reset/')
def user_reset(token=None):
    user_db = model.User.get_by('token', token)
    if not user_db:
        flask.flash(u'Холбоос буруу эсвэл хугацаа нь дууссан байна.', category='danger')
        return flask.redirect(flask.url_for('welcome'))

    if auth.is_logged_in():
        login.logout_user()
        return flask.redirect(flask.request.path)

    form = UserResetForm()
    if form.validate_on_submit():
        user_db.password_hash = util.password_hash(user_db, form.new_password.data)
        user_db.token = util.uuid()
        user_db.verified = True
        user_db.put()
        flask.flash(u'Таны нууц үг амжилттай солигдлоо.', category='success')
        return auth.signin_user_db(user_db)

    return flask.render_template(
        'user/user_reset.html',
        title=u'Нууц үгээ солих',
        html_class='user-reset',
        form=form,
        user_db=user_db,
    )


###############################################################################
# User Activate
###############################################################################
class UserActivateForm(wtf.Form):
    name = wtforms.StringField(
        'Name',
        [wtforms.validators.required()], filters=[util.strip_filter],
    )
    password = wtforms.StringField(
        'Password',
        [wtforms.validators.required(), wtforms.validators.length(min=6)],
    )


@app.route('/user/activate/<token>/', methods=['GET', 'POST'])
def user_activate(token):
    if auth.is_logged_in():
        login.logout_user()
        return flask.redirect(flask.request.path)

    user_db = model.User.get_by('token', token)
    if not user_db:
        flask.flash(u'Холбоос буруу эсвэл хугацаа нь дууссан байна.', category='danger')
        return flask.redirect(flask.url_for('welcome'))

    form = UserActivateForm(obj=user_db)
    if form.validate_on_submit():
        form.populate_obj(user_db)
        user_db.password_hash = util.password_hash(user_db, form.password.data)
        user_db.token = util.uuid()
        user_db.verified = True
        user_db.put()
        return auth.signin_user_db(user_db)

    return flask.render_template(
        'user/user_activate.html',
        title=u'Дансаа идэвхижүүлэх',
        html_class='user-activate',
        user_db=user_db,
        form=form,
    )


###############################################################################
# User Merge
###############################################################################
class UserMergeForm(wtf.Form):
    user_key = wtforms.StringField('User Key', [wtforms.validators.required()])
    user_keys = wtforms.StringField('User Keys', [wtforms.validators.required()])
    username = wtforms.StringField('Username', [wtforms.validators.optional()])
    name = wtforms.StringField(
        'Name (merged)',
        [wtforms.validators.required()], filters=[util.strip_filter],
    )
    email = wtforms.StringField(
        'Email (merged)',
        [wtforms.validators.optional(), wtforms.validators.email()],
        filters=[util.email_filter],
    )


@app.route('/admin/user/merge/', methods=['GET', 'POST'])
@auth.admin_required
def user_merge():
    user_keys = util.param('user_keys', list)
    if not user_keys:
        flask.abort(400)

    user_db_keys = [ndb.Key(urlsafe=k) for k in user_keys]
    user_dbs = ndb.get_multi(user_db_keys)
    if len(user_dbs) < 2:
        flask.abort(400)

    user_dbs.sort(key=lambda user_db: user_db.created)
    merged_user_db = user_dbs[0]
    auth_ids = []
    permissions = []
    is_admin = False
    is_active = False
    for user_db in user_dbs:
        auth_ids.extend(user_db.auth_ids)
        permissions.extend(user_db.permissions)
        is_admin = is_admin or user_db.admin
        is_active = is_active or user_db.active
        if user_db.key.urlsafe() == util.param('user_key'):
            merged_user_db = user_db

    auth_ids = sorted(list(set(auth_ids)))
    permissions = sorted(list(set(permissions)))
    merged_user_db.permissions = permissions
    merged_user_db.admin = is_admin
    merged_user_db.active = is_active
    merged_user_db.verified = False

    form_obj = copy.deepcopy(merged_user_db)
    form_obj.user_key = merged_user_db.key.urlsafe()
    form_obj.user_keys = ','.join(user_keys)

    form = UserMergeForm(obj=form_obj)
    if form.validate_on_submit():
        form.populate_obj(merged_user_db)
        merged_user_db.auth_ids = auth_ids
        merged_user_db.put()

        deprecated_keys = [k for k in user_db_keys if k != merged_user_db.key]
        merge_user_dbs(merged_user_db, deprecated_keys)
        return flask.redirect(
            flask.url_for('user_update', user_id=merged_user_db.key.id()),
        )

    return flask.render_template(
        'user/user_merge.html',
        title='Merge Users',
        html_class='user-merge',
        user_dbs=user_dbs,
        merged_user_db=merged_user_db,
        form=form,
        auth_ids=auth_ids,
        api_url=flask.url_for('api.users', user_keys=','.join(user_keys)),
    )


@ndb.transactional(xg=True)
def merge_user_dbs(user_db, deprecated_keys):
    # TODO: Merge possible user data before handling deprecated users
    deprecated_dbs = ndb.get_multi(deprecated_keys)
    for deprecated_db in deprecated_dbs:
        deprecated_db.auth_ids = []
        deprecated_db.active = False
        deprecated_db.verified = False
        if not deprecated_db.username.startswith('_'):
            deprecated_db.username = '_%s' % deprecated_db.username
    ndb.put_multi(deprecated_dbs)
