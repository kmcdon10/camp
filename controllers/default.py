def index():
    login = A("login", _href=URL("user/login"))
    users = db(db.auth_user).select()
    images = db(db.image).select()
    pages = db(db.page).select()
    form = FORM(INPUT(_id='keyword',_name='keyword',_onkeyup="ajax('callback', ['keyword'], 'target');"))
    target_div = DIV(_id='target')
    return dict(pages=pages, users=users, images=images, login=login, form=form, target_div=target_div)

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

@cache.action()
def download():
    return response.download(request, db)

def search():
     """an ajax wiki search page"""
     return dict(form=FORM(INPUT(_id='keyword',_name='keyword',
              _onkeyup="ajax('callback', ['keyword'], 'target');")),
              target_div=DIV(_id='target'))

@auth.requires_login()
def createpage():
    from gluon.tools import Crud
    crud = Crud(db)
    form = crud.create(db.page) if auth.user else None
    return dict(form=form)

@auth.requires_login()
def editpage():
    this_page = db.page(request.args(0,cast=int)) or redirect(URL('index'))
    from gluon.tools import Crud
    crud = Crud(db)
    form = crud.update(db.page, this_page.id) if auth.user else None
    return dict(form=form)

@auth.requires_login()
def createpost():
    from gluon.tools import Crud
    crud = Crud(db)
    form = crud.create(db.blogpost) if auth.user else None
    return dict(form=form)

@auth.requires_login()
def editpost():
    this_post = db.blogpost(request.args(0,cast=int)) or redirect(URL('index'))
    from gluon.tools import Crud
    crud = Crud(db)
    form = crud.update(db.page, this_post.id) if auth.user else None
    return dict(form=form)

@auth.requires_login()
def editcomment():
    this_comment = db.comment(request.args(0,cast=int)) or redirect(URL('index'))
    from gluon.tools import Crud
    crud = Crud(db)
    form = crud.update(db.comment, this_comment.id) if auth.user else None
    return dict(form=form)

def callback():
     """an ajax callback that returns a <ul> of links to wiki pages"""
     query = db.page.title.contains(request.vars.keyword)
     pages = db(query).select(orderby=db.page.title)
     links = [A(p.title, _href=URL('show',args=p.id)) for p in pages]
     return UL(*links)

def show():
     """shows a wiki page"""
     this_page = db.page(request.args(0,cast=int)) or redirect(URL('index'))
     db.blogpost.blogpage_id.default = this_page.id
     form = SQLFORM(db.blogpost).process() if auth.user else None
     blogpost = db(db.blogpost.blogpage_id==this_page.id).select()
     users = db(db.auth_user).select()
     return dict(page=this_page, blogpost=blogpost, form=form, users=users)

def showpost():
    this_post = db.blogpost(request.args(0,cast=int)) or redirect(URL('index'))
    db.comment.blogpost_id.default = this_post.id
    comment = db(db.comment.blogpost_id==this_post.id).select()
    users = db(db.auth_user).select()
    form = SQLFORM(db.comment).process() if auth.user else None
    return dict(post=this_post, comment=comment, users=users, form=form)

def showuser():
    this_user = db.auth_user(request.args(0, cast=int)) or redirect(URL('index'))
    db.page.created_by.default = this_user.id
    pages = db(db.page.created_by==this_user.id).select()
    return dict(user=this_user, pages=pages)

def showusers():
    login = A("login", _href=URL("user/login"))
    users = db(db.auth_user).select()
    images = db(db.image).select()
    pages = db(db.page).select()
    form = FORM(INPUT(_id='keyword',_name='keyword',_onkeyup="ajax('callback', ['keyword'], 'target');"))
    target_div = DIV(_id='target')
    return dict(pages=pages, users=users, images=images, login=login, form=form, target_div=target_div)
    return dict()

def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
