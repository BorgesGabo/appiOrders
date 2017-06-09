# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
import datetime
import pytablewriter
import HTML

from prettytable import PrettyTable
from prettytable import ALL


def processPo():
    # this function generates a form with date types and query the db between the 2 dates
    # this function is an extract from http://brunorocha.org/python/web2py/search-form-with-web2py.html
    # default values to keep the form when submitted
    # if you do not want defaults set all below to None
    date_initial_default = \
        datetime.datetime.strptime(request.vars.date_initial, "%Y-%m-%d %H:%M:%S") \
            if request.vars.date_inicial else None
    date_final_default = \
        datetime.datetime.strptime(request.vars.date_final, "%Y-%m-%d %H:%M:%S") \
            if request.vars.date_final else None
    # The search form created with .factory
    form = SQLFORM.factory(
        Field("date_initial", "datetime", default=date_initial_default),
        Field("date_final", "datetime", default=date_final_default),
        formstyle='divs',
        submit_button="Search",
    )
    # The base query to fetch all orders of db.po, db.po_details, db.product
    query = db.po.id == db.po_detail.po_id
    query &= db.po_detail.product_id == db.product.id
    # testing if the form was accepted
    if form.process().accepted:
        # gathering form submitted values
        date_initial = form.vars.date_initial
        date_final = form.vars.date_final
        # more dynamic conditions in to query
        if date_initial:
            query &= db.po.date >= date_initial
        if date_final:
            query &= db.po.date <= date_final
    count = db(query).count()
    results = db(query).select(db.po.po_number, db.po.date, db.po_detail.product_id, db.po_detail.quantity,
                               db.product.pres, db.po.customer_id, orderby='po_number')
    msg = T("%s registros encontrados" % count)
    summaryChart(query)
    return dict(form=form, msg=msg, results=results)


def summaryChart(query):
    # Esta corre metiendo el siguiente codigo c:\Python27\python.exe c:\web2py\web2py.py -S EssenciaAPI24/default/ABCD
    b_lst = []  # crea lista de b con los subtotales
    c_lst = []  # crea lista de c contiene los totales por producto
    qty_lst = []  # crea lista de cantidades
    pres_lst = []  # crea lista de presentaciones
    # **************************************QUERY BASE **************************************
    # define el query base -> DAL > query
    '''query = db.po.id==db.po_detail.po_id
    query &= db.po_detail.product_id==db.product.id
    query &= db.po.po_number<2432'''  # quitar comillas si quiere probar desde la linea de comandos

    orders_query_lst = db(query).select(db.po.id, db.po.po_number,
                                        groupby='po.po_number').as_list()  # obtiene id de los pedidos del query
    n = len(orders_query_lst)  # obtiene el numero de pedidos de query
    d_lst = [str(x['po_number']) + '|Recibido' for x in
             orders_query_lst]  # obtiene las referencias de los pedidos del query
    # print orders_query_lst                                                                 #impresion de prueba
    print '\n'
    # print d_lst                                                                            #impresion de prueba

    # ***************************************QUERY A,B *****************************************
    a_product_id_lst = db(query).select(db.product.id, db.product.name,
                                        groupby='product.name').as_list()                       # obtiene id, nombre productos query sin repetir
    for i in range(len(a_product_id_lst)):                                                      # iterando sobre A: a_products_lst
        query_a = query                                                                         # saca una copia del query original query_a
        query_a &= db.product.id == a_product_id_lst[i]['id']                                   # agrega una columna a a_query con el product_id
        for j in range(n):                                                                      # iterando sobre orders_query_lstb "lista de pedidos"
            query_b = query_a                                                                   #saca copia del query_a y agrega el po_id
            query_b &= db.po.id == orders_query_lst[j]['id']
            # print query_b                                                                     # impresion de prueba
            bj_lst = db(query_b).select(db.po_detail.quantity, orderby='po.po_number',          # imprime la cantidad por producto
                                        groupby='po.po_number').as_list()                       # obtiene cantidad
            qtyj_lst = db(query_b).select(db.po_detail.quantity, orderby='po.po_number',
                                          groupby='po.po_number').as_list()                     # obtiene cantidad
            presj_lst = db(query_b).select(db.product.pres, orderby='po.po_number',
                                           groupby='po.po_number').as_list()                    # obtiene pres por producto
            if len(bj_lst) == 0:                                                                # si el pedido no tiene este producto ponga 0
                bj_lst = 0
                b_lst.append(0)
            else:
            b_lst.append(int(bj_lst[0]['quantity']))                                            # de lo contrario ponga el valor de bj_lst de la col. quantity

            if len(qtyj_lst) == 0:  # si no hay cantidad en ese pedido ponga un cero
                qtyj_lst = 0
                presj_lst = 0  # ponga un cero en la presentacion
                qty_lst.append(0)  # ingreselo en la lista de cantidad
                pres_lst.append(0)  # ingreselo en la lista de presentacion
            else:  # en caso contrario obtenga los valores de la consultas
                qty_lst.append(int(qtyj_lst[0]['quantity']))  # obtiene el numero de cantidad
                pres_lst.append(int(presj_lst[0]['pres']))  # obtiene el numero de la presentacion del producto
    # print qty_lst                                                       #impresion de prueba
    # print pres_lst                                                      #impresion de prueba
    z_lst = []
    z_lst = [qty_lst * pres_lst for qty_lst, pres_lst in
             zip(qty_lst, pres_lst)]  # calcula pres*qty para cada uno de los elementos de la lista
    # print z_lst
    # print (str('j is:'), j)                                     #impresion de prueba
    # print (str('bj_lst is:'), bj_lst)                           #impresion de prueba
    # print (str('b_lst is:'), b_lst)                             #impresion de prueba
    # ************************************* SACA LA TABLA EN VERSION HTML ******************************
    htmlTable(n,a_product_id_lst,z_lst)
    # ************************************* IMPRIME TABLA RESUMEN **************************************
    a_product_name_lst = db(query).select(db.product.name,
                                          groupby='product.name').as_list()  # obtiene lista de nombres productos no repetidos en rango
    field_names_lst = d_lst  # crea una lista con todos los numeros del pedido dentro del rango
    field_names_lst.insert(0, "Producto")  # agrega al inicio de la lista el titulo producto
    field_names_lst.insert(len(field_names_lst), "Total")  # Adiciona al final de la lista el titulo total
    summary_table = PrettyTable(field_names_lst)  # crea la tabla resumen con los titulos de cada columna
    total_lst = []
    for y in range(0, len(a_product_id_lst)):
        begining_slice = y * n  # definicion del inicio del intervalo de corte de la lista
        end_slice = begining_slice + n  # definicion del fin del intervalo de corte de la lista
        row_summary_lst = z_lst[
                          begining_slice:end_slice]  # Toma los totales entre el incio y fin del intervalo sin tocar el fin
        # si desea solo las cantidades del pedido sin multiplicar por los pesos usar b_lst por Z_lst
        total = sum(row_summary_lst)  # suma las cantidades de todos los pedidos del rango
        row_summary_lst.insert(0, a_product_name_lst[y]['name'])  # agrega el nombre al inicio de la lista
        row_summary_lst.insert(len(row_summary_lst), total)  # agrega el total al final de la lista
        summary_table.add_row(row_summary_lst)  # agrega filas a la tabla
        summary_table.align = 'l'
        # summary_table.align['Producto']='l'                 # alinea la a la izquierda la primera columna
        summary_table.align['Total'] = 'r'  # alinea a la derecha la ultima columna
    print summary_table  # imprime la tabla resumen
    with open('consolidado.txt', 'w') as w:  # escribe la tabla en un archivo txt
        w.write(str('ESTE ES EL CONSOLIDADO DE LOS SIGUIENTES PEDIDOS:'))
        w.write('\n')
        w.write(str(summary_table))
    writer = pytablewriter.HtmlTableWriter()
    writer.table_name = "consolidado"
    writer.header_list =
    return


def htmlTable(n, a_product_id_lst, z_lst):
    # *********************************************** HTML
    # esta funcion crea la tabla html

    # 0. obtiene el nombre de los pedidos para el headerRow
    header = ["PRODUCTO"]
    for x in orders_query_lst:
        header.append(str(x['po_number']))
        header.append("ENTREGADO ")
    header.append("TOTAL")
    header.append("ENTREGADO")
    # print header
    # 1. obtiene a_lst iterando sobre a_product_id_lst
    a_lst = []
    # print a_product_id_lst
    # print len(a_product_id_lst)
    for x in a_product_id_lst:
        a_lst.append(str(x['name']))
        # print x['name']
    print a_lst
    print ("n es: ", n)
    print ("tamano de z es: ", len(z_lst))
    print ("tamano de a es: ", len(a_lst))

    # 2. crea una lista de listas
    headerRow = []
    summaryCharRows = []
    table = []

    for x in range(len(a_lst)):  # iterando sobre los productos
        if x == 0:
            inicio = 0
            fin = 0 + n
        else:
            inicio = x * n
            fin = inicio + n

        print ("inicio ", inicio)
        print ("fin es: ", fin)
        summaryCharRows = []
        summaryCharRows.append(a_lst[x])
        for y in range(inicio, fin):
            summaryCharRows.append(z_lst[y])
            summaryCharRows.append("        ")

        summaryCharRows.append(sum(z_lst[inicio:fin]))
        summaryCharRows.append("        ")
        table.append(summaryCharRows)
        print ("table is:", table)

    # 3. crea el archivo html

    htmlcode = HTML.table(table, header_row=header)  # crea el codigo html de la tabla
    print htmlcode
    myText = "Este es el consolidado de la fecha"
    html = """
        <html> 
            <head>
                <title>Tabla consolidado de los pedidos a procesar</title>
                <style type="text/css">
                    /**/
                    h2 {font-family:Helvetica; color: #545454}
                    /* Changes the font family */
                    table {font-family:Helvetica;}

                    /* Make cells a bit taller and set border color */
                    td, th { border: 1px solid #696969; height: 30px; text-align: left;}

                    th {font-size: small; /*font size for header row*/
                    font-weight: bold; /* Make sure they're bold */
                    color:#696969; /*font color*/

    }

                    /* Changes the background color of every odd row to light gray */
                    /*table th:nth-child(1) { font-weight: bold}*/

                    /* Changes the background color of every odd row to light gray */
                    /*table tr:nth-of-type(odd) {  background-color: #dbdbdb;}*/

                    /* Changes the background color of every odd column to light gray */
                    table td:nth-of-type(even) {  background-color: #dbdbdb;}

                    /* Changes the weight of each td cell within each odd row to bold */
                    table tr:nth-of-type(odd) td {  font-weight: bold;}

                    /* Collapses table borders to make the table appear continuous */
                    table {  border-collapse: collapse;}
                    td:not(:first-child) {width:80px} /*all columns except the first*/


                </style>
            <head>
            <body>                 
                <h2>%s</h2>
                Aqui va texto adicional
                <strong> %s </strong>
            <body>
        <html>
        """ % (myText, htmlcode)  # Variable que sera reemplazada por %s en el orden que aparece
    f = open("file.html", "w")  # crea archivo
    f.write(html)  # Escribe en el archivo
    f.close()  # Guarda archivo
    # ***********************************************


def loadFormPoDetailQuery():
    # this function uploads and handles the form based on db.po_detail's table also uploads a query which select in reverse order all data in db.po_detail table
    ordenes = db(db.po_detail.id > 0).select(orderby=~db.po_detail.po_id)
    form = SQLFORM(db.po_detail, buttons=[TAG.button('guardar', _type="submit"),
                                          TAG.button('actualizar listado', _type="button",
                                                     _onClick="parent.location='%s' " % URL(loadFormPoDetailQuery))])

    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(ordenes=ordenes, form=form)


def loadFormPoQuery():
    # this function uploads and handles the form based on db.po's table also uploads a query which select in reverse order all data in db.po's table
    ordenes = db(db.po.id > 0).select(orderby=~db.po.id)
    form = SQLFORM(db.po, buttons=[TAG.button('guardar', _type="submit"),
                                   TAG.button('actualizar listado', _type="button",
                                              _onClick="parent.location='%s'" % URL(loadFormPoQuery)),
                                   TAG.button('siguiente', _type="button",
                                              _onClick=" parent.location='%s'" % URL(loadFormPoDetailQuery))])
    if form.process().accepted:
        response.flash = 'order accepted'
    elif form.errors:
        response.flash = 'check the data inserted'
    else:
        response.flash = 'please fill out the form'
    return dict(ordenes=ordenes, form=form)


def loadGridEditCustomer():
    # This function generates a grid form based on db.product's table
    grid = SQLFORM.grid(db.customer, user_signature=False)
    return locals()


def loadGridEditProduct():
    # This function generates a grid form based on db.product's table
    grid = SQLFORM.grid(db.product, user_signature=False)
    return locals()


def loadGridEditPoDetail():
    # This function generates a grid form based on db.product's table
    grid = SQLFORM.grid(db.po_detail, user_signature=False)
    return locals()


def loadFormProduct():
    # This function generates a form based on db.product's table
    form = SQLFORM(db.product, buttons=[TAG.button('guardar', _type="submit")])
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form)


def loadFormPoDetail():
    # This function generates a form db.po_detail's form
    form = SQLFORM(db.po_detail)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form)


def loadFormPo():
    # This function generates a form based on db.po's table
    form = SQLFORM(db.po, buttons=[TAG.button('save', _type="submit"), TAG.button('next', _type="button",
                                                                                  _onClick="parent.location='%s' " % URL(
                                                                                      loadFormPoDetail))])
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form)


def loadFormCustomer():
    # This function generates a form based on db.customer's table
    form = SQLFORM(db.customer, buttons=[TAG.button('guardar', _type="submit"), TAG.button('siguiente', _type="button",
                                                                                           _onClick="parent.location='%s' " % URL(
                                                                                               loadFormPoQuery))])

    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
