
import web, datetime
from datetime import timedelta

# db = web.database(dbn='mysql', db='test', user='')
db = web.database(dbn='sqlite', db='../sqlite.db')

def get_items():
    return db.select('items', order='id DESC')

def get_select_items(id, category, title, description, price, open):
    if price == '' and id != '':
        return db.select('items', order='id DESC', where='id like \'%' + id + '%\'' + 'and category like \'%' + category + '%\' and description like \'%' + description + '%\'' + ' and title like \'%' + title + '%\''  + ' and open like \'%' + open + '%\'')
    if price != '' and id == '':
        return db.select('items', order='id DESC', where='category like \'%' + category + '%\' and description like \'%' + description + '%\'' + ' and title like \'%' + title + '%\'' + ' and open like \'%' + open + '%\'' + ' and price' + price )
    if price == '' and id == '':
        return db.select('items', order='id DESC', where='category like \'%' + category + '%\' and description like \'%' + description + '%\'' + ' and title like \'%' + title + '%\'' + ' and open like \'%' + open + '%\'')    
    else:
        return db.select('items', order='id DESC', where='id like \'%' + id + '%\'' + 'and category like \'%' + category + '%\' and description like \'%' + description + '%\'' + ' and title like \'%' + title + '%\'' + ' and open like \'%' + open + '%\'' + ' and price' + price )

def get_item(id):
    try:
        return db.select('items', where='id=$id', vars=locals())[0]
    except IndexError:
        return None

def new_item(category, title, description, price, duration):
    date = datetime.datetime.utcnow() + datetime.timedelta(hours=duration)
    db.insert('items', category=category, title=title, description=description, price=price, open=True, end_date=date.strftime("%Y-%m-%d %H:%M:%S"), winner='Pending')

def new_bid(id, buyer, price):
    results = db.query('SELECT MAX(bids.price) AS max_price FROM bids WHERE bids.id='+id)
    state = db.query('SELECT items.open AS status FROM items WHERE items.id='+id)
    bidprice = db.query('SELECT items.price FROM items WHERE items.id='+id)
    winningprice = bidprice[0].price
    bidstatus = state[0].status
    maxprice = results[0].max_price
    tempprice = float(price)
    if bidstatus:
        if tempprice > maxprice:        
            db.insert('bids', id=id, buyer=buyer, price=price, time=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
        if tempprice >= winningprice:
            winnertemp = db.query('SELECT bids.buyer FROM bids WHERE bids.id='+id+' AND bids.price=(SELECT MAX(bids.price) FROM bids WHERE bids.id='+id+')')
            winnername = winnertemp[0].buyer
            db.query('UPDATE items SET winner="'+winnername+'" WHERE items.id='+id)
            db.query('UPDATE items SET open=0 WHERE items.id='+id)

def get_bids(id):
    return db.select('bids', where='id=$id', vars=locals(), order='price DESC')

def del_post(id):
    db.delete('entries', where="id=$id", vars=locals())

def update_post(id, title, text):
    db.update('entries', where="id=$id", vars=locals(),
        title=title, content=text)