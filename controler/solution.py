def ppal(queryBase):
    print "\n"* 4
    print "***** +-+-+-+-+-+-+-+-+-+-+-+ NUEVO CALCULO +-+-+-+-+-+-+-+-+-+-+-+-+ ***"
    # 0. CALL getPo
    po = getPo(queryBase)
    print "estas son las pos: ","\n", po, "\n"
    # 1. CALL getNames
    names = getNames(queryBase)
    print "estos son los products.name sin repetir: ","\n", names, "\n"

    # 2. CALL  getIds & pass through charGenerator
    ids = getIds(queryBase)
    # ids_dic = chartGenerator(ids)
    print "esto son los products.ids sin repetir: ","\n", ids, "\n"


    # 3. CALL productsPerPo
    pdcts = productsPerPo(queryBase)
    print "los pos.ids sin repetir: ","\n", pdcts['b'], "\n"
    print "products by po", "\n", pdcts['a'], "\n"

    # 4. CALL chartGenertator
    chart = chartGenerator(ids, pdcts['a'], names)
    print "este es el cuadro","\n", chart, "\n"


    # 5. CALL  filterPerSupplier
    ids2 = filterPerSupplier(queryBase, 0, chart)
    print "estos son los productos filtrados por proveedor 0: ","\n", ids2, "\n"

    ids3 = filterPerSupplier(queryBase, 1, chart)
    print "estos son los productos filtrados por proveedor 1: ","\n", ids3, "\n"

    ids4 = filterPerSupplier(queryBase, 2, chart)
    print "estos son los productos filtrados por proveedor 2: ", "\n", ids4, "\n"

    #6. CALL htmlGenerator
    htmlGenerator(len(pos), chart)
    #htmlGenerator(ids2, 0, po)
    #htmlGenerator(ids3, 1, po)
    #htmlGenerator(ids4, 2, po)

    return

def htmlGenerator(numberOfPos, totals_dic):
    # esta funcion genera el cuadro consolidado de pedidos en formato html
    # INPUT:
    #       numberOfPos: int es el numero de pedidos
    #           chart: dic -> es el consolidado de productos de los productos
    #                  ejemplo: {'producto_567': ['Papa criolla organica', 1500, 1500], 'producto_481': ['Acelga organica', 1000, 500, 1500], 'producto_493': ['Banano Bocadillo organico', 6, 6],....}
    # OUTPUT:
    #        archivo html de nombre ConsolidadoEssencia.html
    #        summaryChartRows: list -> consolidado en forma de lista y con un espacio "  " en el subtotal para un producto que no tiene cantidad
    #                   ejemplo: [['Papa criolla organica', 1500,"  ", 1500], ['Acelga organica', 1000, 500, 1500], ['Banano Bocadillo organico', 6,"  ", 6], ...]
    print "+++++++++++++++++  STARTING htmlGenerator  ++++++++++++++++++++++++++"
    header = ["producto", "1111", "1112", "total"] # TODO header auto
    consolidado = totals_dic.values()
    print ("consolidado es: ", consolidado)
    for x in range(len(totals_dic)):  # iterando sobre los productos
        if x == 0:
            inicio = 0
            fin = 0 + numberOfPos
        else:
            inicio = x * numberOfPos
            fin = inicio + numberOfPos

        print ("inicio ", inicio)
        print ("fin es: ", fin)
        summaryCharRows = []
        #summaryCharRows.append(a_lst[x])
        for y in range(inicio, fin):
            #summaryCharRows.append(z_lst[y])
            summaryCharRows.append("        ")

        #summaryCharRows.append(sum(z_lst[inicio:fin]))
        summaryCharRows.append("        ")
        #table.append(summaryCharRows)
    htmlcode = HTML.table(consolidado, header_row=header)  # crea el codigo html de la tabla
    # print htmlcode                                                        # impresion de prueba codigo html de la tabla
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
    f = open("consolidadoDePedidos", "w")  # crea archivo html
    f.write(html)  # Escribe en el archivo html
    f.close()  # Guarda archivo html

    return

'''
def htmlGenerator(s_lst, proveedorI, poNumber_lst):
    # esta funcion genera un archivo html (consolidadoDePedidos.html) a partir del consolidado de productos (s_lst)
    # INPUTS:
    #
    # OUTPUTS:

    print "+++++++++++++++++  STARTING htmlGenerator  ++++++++++++++++++++++++++"
'''
    # GENERA el header de la tabla html
    header = ["PRODUCTO"]    # crea la lista que contiene el header
    for x in poNumber_lst:
        header.append(str(x))
        header.append("ENTREGADO ")
    header.append("TOTAL")
    header.append("ENTREGADO")'''
    header = ["producto", "1111", "1112", "total"]
    # AGREGA los espacios necesarios para crear la columna ENTREGADO
    for item in s_lst:
        print ("el tamano de item-i es: ", len(item))
        for x in range(len(item)-1):

            if x != 0:
                print ("x es:", x)
                item.insert(2*x,"aqui va")
                print ("item es: ", item)

    print s_lst


    htmlcode = HTML.table(s_lst, header_row=header)  # crea el codigo html de la tabla
    # print htmlcode                                                        # impresion de prueba codigo html de la tabla
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
    f = open("consolidadoEssencia.html", "w")  # crea archivo html
    f.write(html)  # Escribe en el archivo html
    f.close()  # Guarda archivo html
    return'''


def filterPerSupplier(queryBase, proveedorI, chart):
    # esta funcion filtra el consolidado de productos (chart) de la funcion charGenerator() y produce un consolidado de productos para el proveedorI
    # INPUTS:
    #       queryBase: str -> es query tipo DAL web2py con el listado de los productos entre las fechas ingresadas
    #                      ejemplo: ((((po.id = po_detail.po_id) AND (po_detail.product_id = product.id)) AND (po.date >= '2017-05-23 17:43:11')) AND (po.date <= '2017-05-26 15:16:00'))
    #       proveedorI: int -> es un entero que representa el ID de la tabla: db.supplier.id (0-2)
    #       chart: dic -> es el consolidado de productos de los productos
    #                  ejemplo: {'producto_567': ['Papa criolla organica', 1500, 1500], 'producto_481': ['Acelga organica', 1000, 500, 1500], 'producto_493': ['Banano Bocadillo organico', 6, 6],....}
    # OUTPUT
    #       s:list -> es el consolidado por proveedor como una lista
    #               ejemplo: []
    #                        [['Acelga organica', 1000, 500, 1500], ['Huevos de granja organica', 12, 12]]
    #                        [['Papa criolla organica', 1500, 1500], ['Banano Bocadillo organico', 6, 6], ...]

    print "+++++++++++++++++  STARTING filterPerSupplier  ++++++++++++++++++++++++++"
    # SACA listado de Ids de los productos por proveedor
    #print ("esta es la queryBase", queryBase)
    # EJECUTA la query y obtiene los productos para el proveedorI
    queryBaseSupplier = queryBase
    queryBaseSupplier &= db.product.supplier_id == proveedorI
    pdctId_lst_dic = db(queryBaseSupplier).select(db.po_detail.product_id, groupby='product_id').as_list()
    pdct_Id_lst = []

    # OBTIENE el id de cada producto y los almacena en una lista simple
    for i in range(len(pdctId_lst_dic)):
        pdct_Id_lst.append(pdctId_lst_dic[i]['product_id'])

    # CREA una copia del diccionario que contiene los resultados
    r = dict(chart)
    #print ("esta es la lista de los ids filtrados por proveedor", pdct_Id_lst)
    #print ("este es el diccionario: ", chart)

    # REPETIR para cada producto de chart
    for key in chart:
        esta = int(key[9:]) in pdct_Id_lst  # VERIFICA si cada producto de chart esta en la lista
                                            # de los productos filtrados por proveedor
        #print ("key is: ", key)
        #print ("esta ? ", esta)
        if esta == False:  # SI no existe para ese proveedor...
            del r[key]     # BORRA el producto (key) del chart
    s_lst = r.values()         # CONVIERTE a formato lista de sublistas
    return s_lst

def chartGenerator(pdctId_lst, productsPerPo_lst, pdctNames_lst):
    # esta funcion genera un consolidado de productos por orden de compra y suma los subtotales por producto
    # INPUT:
    #       queryBase:     str -> es query tipo DAL web2py con el listado de los productos entre las fechas ingresadas
    #                      ejemplo: ((((po.id = po_detail.po_id) AND (po_detail.product_id = product.id)) AND (po.date >= '2017-05-23 17:43:11')) AND (po.date <= '2017-05-26 15:16:00'))
    #       productsPerPo_lst: -> es el agregado de todos los productos del (queryBase) organizados por orden de compra
    #                       -> es una lista con n elementos donde n es el numero de pedidos
    #                       -> cada elemento contiene m diccionarios donde m es el numero de productos
    #                       ejemplo:
    #                       [[{'product': {'name': 'Acelga organica', 'pres': '500'}, 'po_detail': {'product_id': 481L, 'quantity': '2'}, 'po': {'po_number': 1111L, 'customer_id': 1L}},
    #                        {'product': {'name': 'Huevos de granja organica', 'pres': '6'}, 'po_detail': {'product_id': 542L, 'quantity': '2'}, 'po':
    #                       {'po_number': 1111L, 'customer_id': 1L}}, {'product': {'name': 'Papa criolla organica', 'pres': '500'}, 'po_detail': {'product_id': 567L, 'quantity': '3'},
    #                       'po': {'po_number': 1111L, 'customer_id': 1L}}, {'product': {'name': 'Banano organico', 'pres': '6'}, 'po_detail': {'product_id': 494L, 'quantity': '3'},
    #                       'po': {'po_number': 1111L, 'customer_id': 1L}}],
    #                       [{'product': {'name': 'Banano Bocadillo organico', 'pres': '6'}, 'po_detail': {'product_id': 493L, 'quantity': '1'}, 'po': {'po_number': 1112L, 'customer_id': 18L}},
    #                       ......]]
    #
    #       pdctNames_lst: es una lista con que contiene los numeros de pedido
    #                       ejemplo:
    #                       [1111L, 1112L]
    # OUTPUT:
    #       totals_dic: es un diccionario que contiene el consolidado
    #                       ejemplo:
    #                       {'producto_567': ['Papa criolla organica', 1500, 1500], 'producto_481': ['Acelga organica', 1000, 500, 1500], 'producto_493': ['Banano Bocadillo organico', 6, 6],
    #                       'producto_542': ['Huevos de granja organica', 12, 12], 'producto_590': ['Tomate chonto organico', 2000, 2000], 'producto_497': ['Brocoli organico', 500, 500], ...}

    # GENERATES  a dic with lists named as each product id
    totals_dic = {}
    for pdct in pdctId_lst:
        name = "product_" + str(pdct)
        totals_dic[name] = []

    for ids in pdctId_lst:   # loops over ea consolidated produc Id
        for j in range(len(productsPerPo_lst)): # loops over ea PO
            #print productsPerPo_lst[j][k]['po_detail'].values()
            for k in range(len(productsPerPo_lst[j])):  # loops over ea product
                exist = ids in productsPerPo_lst[j][k][
                    'po_detail'].values()  # check if the product.id of the list is in the product "k" of purchase order "j"
                pres = productsPerPo_lst[j][k]['product']['pres']
                qty = productsPerPo_lst[j][k]['po_detail']['quantity']
                print ("for j: ", j, " k: ", k, "id is:", ids, "exist is: ")
                print exist
                if exist != False:
                    totals_dic["product_" + str(ids)].append(int(pres) * int(qty))
                    print "tamano"
                    print len(totals_dic)

    # AGREGA el texto con el nombre del producto y el total para cada uno de estos
    for i in range(len(pdctNames_lst)):
        pdctName = str(pdctNames_lst[i])
        pdctKey = totals_dic["product_" + str(pdctId_lst[i])] # Ubica la lista correspondiente a cada producto dentro del diccionario por su key
        #print "pdctName[i]: "
        #print pdctNames_lst[i]
        #print "totals_dic"
        #print totals_dic["product_" + str(pdctId_lst[i])]
        pdctKey.insert(0,pdctNames_lst[i]) # A cada lista agrega el nombre
        pdctKey.insert(len(pdctKey), sum(pdctKey[1:])) # En cada lista agrega su total

    return totals_dic

def getPo(queryBase):
    # THIS function gets po numbers
    # INPUT queryBase: str
    # OUTPUT poNumber_lst
    # -----------------------------------------------------
    print "+++++++++++++++++  STARTING GET PO NUMBER FUNCTION   ++++++++++++++++++++++++++"
    poNumber_lst_dic = db(queryBase).select(db.po.po_number, groupby='po_number').as_list()
    poNumber_lst=[]

    # GET all the names of e.a. product
    for i in range(len(poNumber_lst_dic)):
        poNumber_lst.append(poNumber_lst_dic[i]['po_number'])

    return poNumber_lst

def getNames(queryBase):
    # THIS function gets all the names with no repetition
    # INPUT queryBase: str
    # OUTPUT pdctName_lst
    # -----------------------------------------------------
    print "+++++++++++++++++  STARTING GET NAMES FUNCTION   ++++++++++++++++++++++++++"
    pdctNames_lst_dic = db(queryBase).select(db.product.name, groupby='name').as_list()
    pdctNames_lst=[]

    # GET all the names of e.a. product
    for i in range(len(pdctNames_lst_dic)):
        pdctNames_lst.append(pdctNames_lst_dic[i]['name'])

    return pdctNames_lst

def getIds(queryBase):
    # THIS function gets all the productIds with no repetition
    # INPUT queryBase
    # OUTPUT pdctId_lst
    print "+++++++++++++++++  STARTING GET IDS FUNCTION  ++++++++++++++++++++++++++"
    pdctId_lst_dic = db(queryBase).select(db.po_detail.product_id, groupby='product_id').as_list()
    pdct_Id_lst = []

    # GET all the ids of e.a. product
    for i in range(len(pdctId_lst_dic)):
        pdct_Id_lst.append(pdctId_lst_dic[i]['product_id'])

    return pdct_Id_lst

def productsPerPo(queryBase):
    # THIS function produces a list of products per purchase order
    # INPUT orders_lst, queryBase: query by dates
    # OUTPUT productsPerPo_lst, pos_lst
    # --------------------------------------------------------------
    print "+++++++++++++++++  STARTING PRODUCTS PER PO FUNCITON   ++++++++++++++++++++++++++"
    pos_lst_dic = db(queryBase).select(db.po.id,
                                groupby='po_number').as_list()  # GET the number of pos in the queryBase
    # pos_lst_dic es: [{'po.id': 1L}, {'po.id': 2L}]
    pos_lst = []
    productsPerPo_lst = []

    # GET the po.id of e.a.
    for i in range(len(pos_lst_dic)):
        pos_lst.append(pos_lst_dic[i]['id'])
    # pos_lst es: [1L, 2L]

    # GET the products grouped by po
    for i in range(len(pos_lst)):
        poi = pos_lst[i]   # GET ea po.id from list
        # print ("poi es: ", poi)
        queryPos = queryBase
        queryPos &= db.po_detail.po_id == poi
        # print ("querypos es:", queryPos)
        products_lst = db(queryPos).select(db.po.po_number,db.po_detail.product_id,
                                                      db.po_detail.quantity,
                                                      db.product.name,
                                                      db.product.pres, db.po.customer_id).as_list()
        productsPerPo_lst.append(products_lst)

    return {'a': productsPerPo_lst, 'b':pos_lst}

def productsPerSupplier(query):
    # THIS function produces a listing of products per supplier
    # INPUT query: str
    # OUTPUT {'a':productsPerSupplier, 'b':querySupplier}
    # ------------------------------------------------------------

    print "+++++++++++++++++  STARTING QUERY SUPPLIER FUNCITON   ++++++++++++++++++++++++++"
    for i in range(0, 4):
        if i == 0:
            querySupplier = query
        else:
            querySupplier = query
            querySupplier &= db.product.supplier_id == i
       productsPerSupplier = db(querySupplier).select(db.po.po_number, db.po_detail.product_id,
                                                  db.po_detail.quantity, db.product.name,
                                                 db.product.pres, db.po.customer_id, orderby='po_number').as_list()
        # queryPo(productsPerSupplier, querySupplier)
        # print querySupplier
        # print productsPerSupplier
    return {'a':productsPerSupplier, 'b':querySupplier}

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
    queryGen(query)