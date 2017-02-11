import web
import datetime
import model 
from web import form

render = web.template.render('templates/', base='base')

urls = ('/', 'Index',
        '/view/(\d+)', 'View',
        '/bid', 'Bid',
        '/bid/(\d+)', 'Bid',
        '/bids/(\d+)', 'Bids',
        '/new', 'New'
)
app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'id': ''})

options = form.Form( 
    form.Textbox('id', form.regexp('\d*', 'Must be digits'), value=""), 
    form.Dropdown('category', ['']), 
    form.Textbox('title', form.regexp('[^\'^\"]*', 'Invalid text'), value=""), 
    form.Textbox('description', form.regexp('[^\'^\"]*', 'Invalid text'), value=""), 
    form.Textbox('price', form.regexp('[><]?[=]?\d*', 'Must be <, >, <=, or >=, followed by digits'), value=""), 
    form.Dropdown('open', ['', '1', '0'])
) 



class Index: 
    def GET(self): 
        columns = options()
        db = web.database(dbn='sqlite', db='../sqlite.db')
        categories = db.select('categories', what='name').list()
        for category in categories:
            columns.category.args = columns.category.args + [category.name]
        items = model.get_items()         
        current_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        return render.index(columns, items, current_time)

    def POST(self): 
        columns = options() 
        db = web.database(dbn='sqlite', db='../sqlite.db')
        categories = db.select('categories', what='name').list()
        for category in categories:
            columns.category.args = columns.category.args + [category.name]
        if not columns.validates():
            print columns.render_css()
            raise web.seeother('/')
        else:
            items = model.get_select_items(columns.d.id, columns.d.category, columns.d.title, columns.d.description, columns.d.price, columns.d.open)
            current_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            return render.index(columns, items, current_time)

class View: 
    def GET(self, id):
        item = model.get_item(int(id))
        current_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        return render.view(item, current_time)

bidForm = form.Form( 
       form.Textbox('buyer', form.notnull),
       form.Textbox('price', form.notnull),
)
class Bid: 
    def GET(self, id):
        bid = bidForm()
        bid.d.id=id
        item = model.get_item(int(id))
        web.setcookie('id', item.id)
        current_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        return render.bid(item, bid, current_time)

    def POST(self): 
        bid = bidForm() 
        id = web.cookies().get('id')
        if not bid.validates():
            raise web.seeother('/view/' + id)
        else:
            model.new_bid(id, bid.d.buyer, bid.d.price);
            raise web.seeother('/view/' + id)

class Bids: 
    def GET(self, id):
        bids = model.get_bids(int(id))
        current_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        return render.bids(id, bids, current_time)

newForm = form.Form( 
       form.Dropdown('category', []),
       form.Textbox('title', form.notnull, value=''),
       form.Textbox('description', form.notnull, value=''),
       form.Textbox('price', form.notnull, form.regexp('\d+', 'Must be a digit')),
       form.Textbox('duration', form.notnull, form.regexp('\d+', 'Must be a digit')))

class New: 
    def GET(self):
        form= newForm()
        db = web.database(dbn='sqlite', db='../sqlite.db')
        categories = db.select('categories', what='name').list()
        form.category.args=['']
        for category in categories:
            form.category.args = form.category.args + [category.name]
        current_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        return render.new(form, current_time)

    def POST(self): 
#        db = web.database(dbn='mysql', user='', pw='', db='test')
        db = web.database(dbn='sqlite', db='../sqlite.db')
        form= newForm() 
        if not form.validates():
            current_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            return render.new(form, current_time)
        else:
            print form['duration'].value
            model.new_item(form['category'].value, form['title'].value, form['description'].value, form['price'].value, int(form['duration'].value)) 
        raise web.seeother('/')

if __name__=="__main__":
    web.internalerror = web.debugerror
    app.run()
