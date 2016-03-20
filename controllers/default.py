def index():
    login = A("login", _href=URL("user/login"))
    return dict(login=login)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

def about():
    return dict()

def registration():
    return dict()

def activities():
    return dict()

def nurses():
    return dict()

def checkout():
    form = SQLFORM(db.pending, formstyle='divs', submit_button='Buy')
    if form.process().accepted:
        response.flash = 'form accepted'
        session.pending = form.vars
        redirect(URL('default', 'paypal'))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form)

def all():
    return dict(grid=SQLFORM.smartgrid(db.pending))

def pending():
    return dict(grid=SQLFORM.smartgrid(db.confirmed_trans))

def paypal():
    if not session.pending:
        redirect(URL('default', 'index'))
    return dict()

def success():
    # log_file(str(request.vars), 'tmp/paypal.return')
    if request.args(0) == 'paypal':
        if response:
            message = 'Thank you! You payment is complete and your order is being prepared.'
        else:
            message = 'Sorry. An error has occured and you payment did not go through.'
    return dict(message=message)

def staff():
    return dict()

@auth.requires_login()
def staff_app():
    form = SQLFORM(db.staff)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form)

def counselor():
    return dict()

@auth.requires_login()
def counselor_app():
    form = SQLFORM(db.counselor)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form)

def camper():
    return dict()

@auth.requires_login()
def camper_app():
    form = SQLFORM(db.camper)
    if form.process().accepted:
        response.flash = 'form accepted'
        redirect(URL('default', 'guardian'))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form)

@auth.requires_login()
def guardian():
    form = SQLFORM(db.guardian)
    if form.process().accepted:
        response.flash = 'form accepted'
        redirect(URL('default', 'medical_information'))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form)

@auth.requires_login()
def medical_information():
    form = SQLFORM(db.medical_information)
    if form.process().accepted:
        response.flash = 'form accepted'
        redirect(URL('default', 'eating'))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form)

@auth.requires_login()
def eating():
    form = SQLFORM(db.eating)
    if form.process().accepted:
        response.flash = 'form accepted'
        redirect(URL('default', 'behavior'))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form)

@auth.requires_login()
def behavior():
    form = SQLFORM(db.behavior)
    if form.process().accepted:
        response.flash = 'form accepted'
        redirect(URL('default', 'transportation'))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form)

@auth.requires_login()
def transportation():
    form = SQLFORM(db.transportation)
    if form.process().accepted:
        response.flash = 'form accepted'
        redirect(URL('default', 'new_camper_information'))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form)

@auth.requires_login()
def new_camper_information():
    form = SQLFORM(db.new_camper_information)
    if form.process().accepted:
        response.flash = 'form accepted'
        redirect(URL('default', 'camp_parent_questionnaire'))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form)

@auth.requires_login()
def camp_parent_questionnaire():
    form = SQLFORM(db.camp_parent_questionnaire)
    if form.process().accepted:
        response.flash = 'form accepted'
        redirect(URL('default', 'pay'))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form)

def donate():
    return dict()

def wishlist():
    return dict()

def questions():
    return dict()

@cache.action()
def download():
    return response.download(request, db)

def search():
     """an ajax wiki search page"""
     return dict(form=FORM(INPUT(_id='keyword',_name='keyword',
              _onkeyup="ajax('callback', ['keyword'], 'target');")),
              target_div=DIV(_id='target'))


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
