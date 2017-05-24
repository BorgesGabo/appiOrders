# -*- coding: utf-8 -*-
import os
db = DAL('sqlite://storage.sqlite')

db.define_table('wp',
    Field('name', requires=IS_NOT_EMPTY()),
    Field('json_file', 'upload'))

# ----------------------------------------------
# define single tables
# ----------------------------------------------

# define customer
db.define_table(
    'customer',
    Field('full_name'),
    Field('phone'),
    format='%(full_name)s')

# define category
db.define_table(
    'category',
    Field('name', label='categoria'),
    Field('odoo_cat', label='id de odoo categoria'),
    format='%(name)s')

# define supplier
db.define_table(
    'supplier',
    Field('name', label='proveedor'),
    Field('odoo_seller', label='id odoo proveedor'),
    format='%(name)s')
# -----------------------------------------------
# define related tables
# -----------------------------------------------


# define po
db.define_table(
    'po',
    Field('po_number', type='integer'),
    Field('date', type='datetime'),
    Field('customer_id', 'reference customer'),
    format='%(po_number)s')

# define product
db.define_table(
    'product',
    Field('name'),
    Field('woo_ref'),
    Field('pres'),
    Field('unit'),
    Field('sku'),
    Field('odoo_ref'),
    Field('category_id', 'reference category'),
    Field('supplier_id', 'reference supplier'),
    Field('odoo_ref'),
    format='%(name)s')

db.define_table(
    'po_detail',
    Field('po_id', 'reference po'),
    Field('product_id', 'reference product'),
    Field('quantity', default='1'),
    )

# -----------------------------
# category table validation
# -----------------------------
db.category.name.requires = [IS_NOT_EMPTY(),IS_MATCH('^\w+( \w+)*$', error_message='Introduce a valid name just alphabets')]

# -----------------------------
# supplier table validation
# -----------------------------
db.supplier.name.requires = [IS_NOT_EMPTY(),IS_MATCH('^\w+( \w+)*$', error_message='Introduce a valid name just alphabets')]

# ------------------------------
# Customer's table validation
# ------------------------------
# using a regex expression to validate numbers input
db.customer.phone.requires = [IS_NOT_IN_DB(db, db.customer.phone),IS_MATCH('^[0-9]*$', error_message='Introduce a valid document just numbers')]

# using a regex expression validates words only
db.customer.full_name.requires = [IS_NOT_EMPTY(),IS_MATCH('^\w+( \w+)*$', error_message='Introduce a valid name just alphabets')]


# using a regex expression validates the phone number format
# see more at... "http://stackoverflow.com/questions/16699007/regular-expression-to-match-standard-10-digit-phone-number"
db.customer.phone.requires = IS_MATCH('^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})?[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$',
         error_message='not a phone number. Introduce a valid number neither spaces nor dots')


# -----------------------------
# po's table validation
# -----------------------------

# validates not empty, regex valid number and, is not already in db 
db.po.po_number.requires=[IS_NOT_EMPTY(),IS_MATCH('^[0-9]*$', error_message='Introduce a valid document just numbers'), IS_NOT_IN_DB(db,db.po.po_number)]
# validates the date format
db.po.date.requires = IS_DATETIME(format=T('%Y-%m-%d %H:%M:%S'),error_message='must be YYYY-MM-DD HH:MM:SS!')

# ------------------------------
# product's table validation
# ------------------------------
# using regex expression to validate just one o more words
db.product.name.requires = IS_MATCH('^\w.+( \w.+)*$', error_message='Introduce a valid name just alphabets')
db.product.pres.requires = [IS_NOT_EMPTY(error_message='add a quantity' ),IS_MATCH('^[0-9]*$', error_message='Introduce a valid document just numbers')]
db.product.unit.requires =[ IS_IN_SET(['g','un'], error_message='must be g or un')]
db.product.sku.requires = [IS_NOT_IN_DB(db, db.product.sku),IS_MATCH('^[0-9,a-z]*$', error_message='Introduce a valid sku code')]

#--------------------------------
# po's_detail's table validation
#--------------------------------
# verifies that the quantity is a number not empty
db.po_detail.quantity.requires=[IS_NOT_EMPTY(error_message='add a quantity'),IS_MATCH('^[0-9]*$', error_message='Introduce a valid quantity a number')]
