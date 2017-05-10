# -*- coding: utf-8 -*-
import os
db = DAL('sqlite://storage.sqlite')

db.define_table('wp',
    Field('name', requires=IS_NOT_EMPTY()),
    Field('json_file', 'upload'))

db.define_table(
    'customer',
    Field('doc',label='No. Documento'),
    Field('full_name'),
    Field('user_mail'),
    Field('phone'),
    format='%(full_name)s')

db.define_table(
    'po',
    Field('po_number', type='integer'),
    Field('date', type='datetime'),
    Field('customer_id', 'reference customer'),
    format='%(po_number)s')

db.define_table(
    'product',
    Field('name'),
    Field('woo_ref'),
    Field('txt'),
    Field('pres'),
    Field('unit'),
    Field('sku'),
    Field('category'),
    Field('status'),
    format='%(name)s')

db.define_table(
    'po_detail',
    Field('po_id', 'reference po'),
    Field('product_id', 'reference product'),
    Field('quantity', default='1'),
    )



#------------------------------
#Customer's table constraints
#------------------------------
#using a regex expression validates the just numbers
db.customer.doc.requires = [IS_NOT_IN_DB(db, db.customer.doc),IS_MATCH('^[0-9]*$', error_message='Introduce a valid document just numbers')]

#using a regex expression validates words only
db.customer.full_name.requires = [IS_NOT_EMPTY(),IS_MATCH('^\w+( \w+)*$', error_message='Introduce a valid name just alphabets')]
db.customer.user_mail.requires = IS_EMAIL()

#using a regex expression validates the phone number format
# see more at... "http://stackoverflow.com/questions/16699007/regular-expression-to-match-standard-10-digit-phone-number"
db.customer.phone.requires = IS_MATCH('^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})?[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$',
         error_message='not a phone number. Introduce a valid number neither spaces nor dots')


#-----------------------------
#po's table constraints
#----------------------------

# validates not empty, regex valid number and, is not already in db 
db.po.po_number.requires=[IS_NOT_EMPTY(),IS_MATCH('^[0-9]*$', error_message='Introduce a valid document just numbers'), IS_NOT_IN_DB(db,db.po.po_number)]
# validates the date format
db.po.date.requires = IS_DATETIME(format=T('%Y-%m-%d %H:%M:%S'),error_message='must be YYYY-MM-DD HH:MM:SS!')

#------------------------------
# product's table constraints
#------------------------------
#using regex expression to validate just one o more words 
db.product.name.requires = IS_MATCH('^\w.+( \w.+)*$', error_message='Introduce a valid name just alphabets')
db.product.txt.requires = IS_NOT_EMPTY(error_message='copy here what is on product presentation in woocommerce' )
db.product.pres.requires = [IS_NOT_EMPTY(error_message='add a quantity' ),IS_MATCH('^[0-9]*$', error_message='Introduce a valid document just numbers')]
db.product.unit.requires =[ IS_IN_SET(['g','un', 'ml'], error_message='must be g or un')]
db.product.sku.requires = [IS_NOT_IN_DB(db, db.product.sku),IS_MATCH('^[0-9]*$', error_message='Introduce a valid document just numbers')]
db.product.category.requires =[ IS_IN_SET(['aceites y aderezos','bebidas','condimentos y especias', 'frutas', 'frutos secos', 'harinas hojuelas y pastas', 'hortalizas', 'huevos','nueces y semillas','pa picar y endulzar','panaderia','proteina de  origen vegetal'], error_message='must be one of the existing categories')]
db.product.status.requires =[ IS_IN_SET(['disponible','descontinuado','agotado'], error_message='must be disponible, descontinuado o agotado')]

#--------------------------------
# po's_detail's table constrains
#--------------------------------
# verifies that the quantity is a number not empty
db.po_detail.quantity.requires=[IS_NOT_EMPTY(error_message='add a quantity'),IS_MATCH('^[0-9]*$', error_message='Introduce a valid quantity a number')]
