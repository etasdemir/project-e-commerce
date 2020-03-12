import mysql.connector
from datetime import date

my_db = mysql.connector.connect(host="localhost", user="root", password="")
"""
BEFORE STARTING APPLICATION PLEASE IMPORT SQL FILE TO THE DATABASE
"""
db_create = my_db.cursor()
db_create.execute("create database if not exists snb")
my_db.database = "snb"
"""
BEFORE STARTING APPLICATION PLEASE IMPORT SQL FILE TO THE DATABASE
"""


def add_user(email, password, nickname, name, last_name, address, phone, birth_date, kind):
    cursor = my_db.cursor()
    insert_query = "CALL insert_person(%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    parameters = (email, password, nickname, name, last_name, address, phone, birth_date, kind)
    for element in parameters:
        if element == "":
            return 0
    cursor.execute(insert_query, parameters)
    return 1


def find_user(email, nickname, password):
    cursor = my_db.cursor()
    user_query = "select person.nickname from registration, person  where person.reg_e_mail = registration.e_mail and registration.e_mail = %s and registration.password = %s"
    parameters = (email, password)
    for element in parameters:
        if element == "":
            return 0
    cursor.execute(user_query, parameters)
    for items in cursor:
        if nickname == items[0]:
            return nickname
        else:
            return 0


def kind_finder(nickname):
    cursor1 = my_db.cursor()
    buyer_query = "select count(*) from buyer where buyer.nickname = %(nick)s"
    cursor1.execute(buyer_query, {'nick': nickname})
    for a in cursor1:
        if int(a[0]) > 0:
            return "buyer"

    cursor2 = my_db.cursor()
    seller_query = "select count(*) from seller where seller.nickname = %(nick)s "
    cursor2.execute(seller_query, {'nick': nickname})
    for b in cursor2:
        if int(b[0]) > 0:
            return "seller"


def products(key):
    cursor = my_db.cursor()
    query = "select product.id, category.name, product.brand, product.name, seller_nickname, stock,price  \
            from product, category, stock_product \
            where product.category_id = category.id and product.id = stock_product.product_id"
    order = ""
    if key == 0:
        order = " order by product.id"
    elif key == 1:
        order = " order by category.name"
    elif key == 2:
        order = " order by product.brand"
    elif key == 3:
        order = " order by product.name"
    elif key == 4:
        order = " order by seller_nickname"
    elif key == 5:
        order = " order by stock desc"
    elif key == 6:
        order = " order by price"
    query = query + order
    cursor.execute(query)
    str = ""
    for id, cat, brand, name, seller, stock, price in cursor:
        str = str + f"{id}      |       {cat.upper()}       |          {brand.upper()}      |       {name.upper()}      |       {seller}      |       {stock}      |       {price}\n"
    return str


def sort_products(order):
    cursor = my_db.cursor()
    query = "select product.id, category.name, product.brand, product.name, seller_nickname, stock,price from product, category, stock_product where product.category_id = category.id and product.id = stock_product.product_id" + f" order by {order}"
    cursor.execute(query)
    str = ""
    for id, cat, brand, name, seller, stock, price in cursor:
        str = str + f"{id}      |       {cat}       |          {brand}      |       {name}      |       {seller}      |       {stock}      |       {price}\n"
    return str

def find_sellers_products(nickname):
    cursor = my_db.cursor()
    query = "select product.id, category.name, brand, product.name, stock, price from product, stock_product,category where stock_product.product_id = product.id and product.category_id = category.id and stock_product.seller_nickname = %(nick)s"
    cursor.execute(query, {'nick': nickname})
    str = ""
    for id, cat, brand, name, stock, price in cursor:
        str = str + f"{id}      |       {cat.upper()}       |          {brand.upper()}      |       {name.upper()}      |       {stock}      |       {price}\n"
    return str

def product_deleter(id,seller_nickname):
    cursor = my_db.cursor()
    query = "select count(*) from product, stock_product where stock_product.product_id = product.id and stock_product.seller_nickname = %s and product.id = %s"
    parameters = (seller_nickname, id)
    cursor.execute(query, parameters)
    cursor.fetchall()
    for elements in cursor:
        if elements == 0:
            return 0
    query1 = "delete from product where id = %(nick)s"
    cursor1 = my_db.cursor()
    query2 = "delete from stock_product where stock_product.seller_nickname = %s and product_id = %s"
    cursor2 = my_db.cursor()
    cursor1.execute(query1,{'nick': seller_nickname})
    cursor2.execute(query2,(seller_nickname,id))
    return 1

def product_updater_adder(brand,name,cat,nickname,stock,price,id):
    cursor = my_db.cursor()
    parameters = (brand,name,cat,nickname,stock,price,id)
    for elements in parameters:
        if elements == "":
            return 0
    query = "CALL update_the_stock_and_price(%s,%s,%s,%s,%s,%s,%s);"
    cursor.execute(query,parameters)
    return 1

def category_show():
    cursor = my_db.cursor()
    query = "select name from category"
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows

def bucket_adder(nickname,id,seller,amount):
    cursor = my_db.cursor()
    parameter = (nickname,id,seller,amount)
    query = "call add_to_bucket(%s,%s,%s,%s);"
    cursor.execute(query, parameter)

def bucket_finder(nickname):
    cursor = my_db.cursor()
    cur_date = date.today()
    query = "select product.id, brand, product.name, bucket.seller_nickname, amount, price from product, stock_product, bucket where bucket.buyer_nickname = %s and adding_date = %s and bucket.product_id = product.id and bucket.seller_nickname = stock_product.seller_nickname and stock_product.product_id = product.id "
    parameters = (nickname, cur_date)
    cursor.execute(query, parameters)
    str = ""
    for elements in cursor:
        total_price = elements[4] * elements[5]
        str = str + f"{elements[0]}    ||    {elements[1].upper()}    ||    {elements[2].upper()}    ||    {elements[3]}    ||    {elements[4]}    ||    {elements[5]} TL    ||    {total_price} TL\n"

    return str

def remove_from_bucket(nickname):
    cursor = my_db.cursor()
    cur_date = date.today()
    query = "DELETE FROM bucket WHERE bucket.buyer_nickname = %s AND bucket.adding_date = %s"
    parameters = (nickname, cur_date)
    cursor.execute(query, parameters)
    return 1

def payment_maker(nickname, pay_type, name, no, cvc):
    cursor = my_db.cursor()
    cur_date = date.today()
    query = "call make_payment(%s, %s, %s, %s, %s, %s);"
    parameters = (nickname, cur_date, pay_type, name, no, cvc)
    cursor.execute(query, parameters)
    return 1

def seller_profile(nickname):
    cursor = my_db.cursor()
    query = "select name, lastname, person.nickname, reg_e_mail, address, phone, DoB, rate from person, seller where person.nickname = %(nick)s and person.nickname = seller.nickname"
    cursor.execute(query, {'nick': nickname})
    values = cursor.fetchall()
    values = values[0]
    return values

def buyer_profile(nickname):
    cursor = my_db.cursor()
    query = "select name, lastname, person.nickname, reg_e_mail, address, phone, DoB, ranking from person, buyer where person.nickname = %(nick)s and person.nickname = buyer.nickname "
    cursor.execute(query, {'nick': nickname})
    values = cursor.fetchall()
    values = values[0]
    return values

def paid_bucket_finder(nickname):
    cursor = my_db.cursor()
    cur_date = date.today()
    query = "select product.id, brand, product.name, backup_bucket.seller_nickname, amount, price from product, stock_product, backup_bucket where backup_bucket.buyer_nickname = %s and adding_date = %s and backup_bucket.product_id = product.id and backup_bucket.seller_nickname = stock_product.seller_nickname and stock_product.product_id = product.id "
    parameters = (nickname, cur_date)
    cursor.execute(query, parameters)
    str = ""
    for elements in cursor:
        total_price = elements[4] * elements[5]
        str = str + f"{elements[0]}    ||    {elements[1].upper()}    ||    {elements[2].upper()}    ||    {elements[3]}    ||    {elements[4]}    ||    {elements[5]} TL    ||    {total_price} TL\n"

    return str

def rate_giver(id,seller,buyer,comment,rate):
    cursor2 = my_db.cursor()
    cur_date = date.today()
    query2 = "select count(*) from product_rate where product_id = %s and seller_nickname = %s and buyer_nickname = %s and rate_date = %s"
    parameters = (id,seller,buyer,cur_date)
    cursor2.execute(query2,parameters)
    rows = cursor2.fetchall()
    if rows[0][0] != 0:
        return 0
    else:
        cursor = my_db.cursor()
        query = "call add_rate_to_product(%s,%s,%s,%s,%s,1);"
        params = (id, seller,buyer,comment,rate)
        cursor.execute(query,params)
        return 1

def statistic_finder(key, table_name):
    cursor = my_db.cursor()
    if key == 0:
        query = "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'snb';"
        cursor.execute(query)
        result = cursor.fetchall()
        return result[0]
    elif key == 1:
        query = "SELECT COUNT(*) from backup_bucket"
        cursor.execute(query)
        result = cursor.fetchall()
        return result[0]
    elif key == 2:
        query = "SELECT COUNT(*) from bucket"
        cursor.execute(query)
        result = cursor.fetchall()
        return result[0]
    elif key == 3:
        query = "SELECT COUNT(*) from buyer"
        cursor.execute(query)
        result = cursor.fetchall()
        return result[0]
    elif key == 4:
        query = "SELECT COUNT(*) from category"
        cursor.execute(query)
        result = cursor.fetchall()
        return result[0]
    elif key == 5:
        query = "SELECT COUNT(*) from creditcard"
        cursor.execute(query)
        result = cursor.fetchall()
        return result[0]
    elif key == 6:
        query = "SELECT COUNT(*) from eft"
        cursor.execute(query)
        result = cursor.fetchall()
        return result[0]
    elif key == 7:
        query = "SELECT COUNT(*) from payment"
        cursor.execute(query)
        result = cursor.fetchall()
        return result[0]
    elif key == 8:
        query = "SELECT COUNT(*) from paypal"
        cursor.execute(query)
        result = cursor.fetchall()
        return result[0]
    elif key == 9:
        query = "SELECT COUNT(*) from person"
        cursor.execute(query)
        result = cursor.fetchall()
        return result[0]
    elif key == 10:
        query = "SELECT COUNT(*) from product"
        cursor.execute(query)
        result = cursor.fetchall()
        return result[0]
    elif key == 11:
        query = "SELECT COUNT(*) from product_rate"
        cursor.execute(query)
        result = cursor.fetchall()
        return result[0]
    elif key == 12:
        query = "SELECT COUNT(*) from registration"
        cursor.execute(query)
        result = cursor.fetchall()
        return result[0]
    elif key == 13:
        query = "SELECT COUNT(*) from seller"
        cursor.execute(query)
        result = cursor.fetchall()
        return result[0]
    elif key == 14:
        query = "SELECT COUNT(*) from stock_product"
        cursor.execute(query)
        result = cursor.fetchall()
        return result[0]