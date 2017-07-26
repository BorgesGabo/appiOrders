def ppal(queryBase):
    # esta funcion controla el algoritmo para sacar todos los consolidados
    # en otras palabras este es el nucleo del programa
    #--------------------------------------
    # Se llama consolidado a un listado que contiene la variable mencionada de todos los productos que fueron comprados o pedidos entre
    # del rango de fechas. El listado no contiene repeticiones
    #---------------------------------------
    print "\n"* 4
    print "*****                    NUEVO CALCULO                    *****"
    # OBTIENE el listado de las pos
    po_lst = getPo(queryBase)
    print "estas son las pos: ","\n", po_lst, "\n"

    # OBTIENE el consolidado de los po.ids_lst alfabeticamente por nombre
    ids_lst = getIds(queryBase)
    # ids_dic = chartGenerator(ids)
    print "esto son los product.id sin repetir: ", "\n", ids_lst, "\n"

    # OBTIENE el consolidado de los product.names alfabeticamente
    names_lst = getNames(queryBase)
    print "estos son los product.name sin repetir: ","\n", names_lst, "\n"

    # OBTIENE el consolidado total de los pedidos
    chart_lst = chartGenerator2(queryBase, po_lst, ids_lst, names_lst)
    print "este es el consolidado: ","\n", chart_lst, "\n"

    # FILTRA los nombres por proveeedor
    for i in range(1,4):
        pdctsFiltered = filterSup(queryBase, i, chartGenerator2(queryBase, po_lst, ids_lst, names_lst))
        excel_lst = excelTables(pdctsFiltered, i)

     # GENERA el archivo html
    html_lst = htmlGenerator(po_lst,chartGenerator2(queryBase, po_lst, ids_lst, names_lst))

    return

def excelTables(chartPerSupplier_lst, supplierId):
    # Esta funcion crea la tabla en excel de los productos por proveedor
    #   INPUT:
    #           chartPerSupplier_lst ->
    #                   ejemplo: [['Acelga organica', 1000, 500, 1500], ['Banano Bocadillo organico', 0, 6, 6], ['Banano organico', 18, 0, 18], ['Brocoli organico', 0, 500, 500], ...]
    # CREA el libro de excel y toma la hoja como activa
    wb = Workbook()
    ws = wb.active

    # CREA el header de la tabla en excel
    header = ["PRODUCTO"]
    header.append("TOTAL")
    header.append("LBS")

    data = [
        ['Apples', 10000, 5000, 8000, 6000],
        ['Pears', 2000, 3000, 4000, 5000],
        ['Bananas', 6000, 6000, 6500, 6000],
        ['Oranges', 500, 300, 200, 700],
    ]
    lastCell = str(len(chartPerSupplier_lst) + 1)  # Find the last row with data
    lastCell = "C" + lastCell  # Add the column by concatenating
    lastCell = "A1:" + lastCell  # Produce the range of cells which contains the data
    print lastCell
    # add column headings. NB. these must be strings
    # AGREGA los header de la tabla Excel
    ws.append(header)
    for row in chartPerSupplier_lst:
        ws.append(row)

    tab = Table(displayName="Table1", ref=lastCell)

    # Add a default style with striped rows and banded columns
    style = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False,
                           showLastColumn=False, showRowStripes=True, showColumnStripes=True)
    tab.tableStyleInfo = style
    ws.add_table(tab)
    if supplierId == 1:
        wb.save("Lista de Eduardo.xlsx")
    elif supplierId ==2:
        wb.save("Lista de Floro.xlsx")
    elif supplierId ==3:
        wb.save("Lista de Otros Proveedores.xlsx")
    return


def filterSup(queryBase, supplierId, summaryChart_lst):
    print "*" * 20, "STARTING filterPerSup", "*" * 20
    # esta funcion filtra el consolidado por proveedor
    # INPUT:
    #       queryBase: str -> es query tipo DAL web2py con el listado de los productos entre las fechas ingresadas
    #                      ejemplo: ((((po.id = po_detail.po_id) AND (po_detail.product_id = product.id)) AND (po.date >= '2017-05-23 17:43:11')) AND (po.date <= '2017-05-26 15:16:00'))
    #       supplierId: int -> es el product.supplier_id
    #       summaryChart_lst: -> es el consolidado de productos para todos los pedidos

    # OBTIENE los product.name de los pedidos dentro de las fechas pero adicionalmente los filtra por proveedor
    querySupplier = queryBase
    querySupplier &= db.product.supplier_id == supplierId
    pdctNamesSupplier_lst_dic = db(querySupplier).select(db.product.name, orderby='product.name', groupby='product.name').as_list()
    pdctNamesSupplier_lst =[]

    # OBTIENE los nombres como una lista simple
    for j in range(len(pdctNamesSupplier_lst_dic)):
        pdctNamesSupplier_lst.append(pdctNamesSupplier_lst_dic[j]['name'])
    print "\n", "estos son los nombres del productos para este proveedor", pdctNamesSupplier_lst

    chartPerSupplier_lst = summaryChart_lst
    print "\n", "este es el consolidado chartPerSupplier_lst: ",chartPerSupplier_lst

    # CREA la lista para guardar posiciones a borrar
    position_lst=[]

    # OBTIENE las posiciones de los elementos a borrar y los guarda en la lista
    for j in range(len(chartPerSupplier_lst)):
        exist = chartPerSupplier_lst[j][0] in pdctNamesSupplier_lst
        if exist == False:
            position_lst.append(j)

    print "\n", "esta son las posiciones de los elementos a eliminar position_lst es: ", position_lst

    # EJECUTA el filtro
    for position in sorted(position_lst, reverse=True):
        del chartPerSupplier_lst[position]
    print  "este es el listado filtrado: ", chartPerSupplier_lst
    print "*" * 20, "ENDING filterPerSup", "*" * 20

    return chartPerSupplier_lst

def chartGenerator2(queryBase, poNumber_lst, pdctId_lst, pdctNames_lst):
    # esta funcion genera un arreglo de listas con el consolidado de los pedidos
    # INPUT:
    #       queryBase: str -> es query tipo DAL web2py con el listado de los productos entre las fechas ingresadas
    #                      ejemplo: ((((po.id = po_detail.po_id) AND (po_detail.product_id = product.id)) AND (po.date >= '2017-05-23 17:43:11')) AND (po.date <= '2017-05-26 15:16:00'))
    #       poNumber_lst: -> contiene un listado con los po.po_number entre las fechas especificadas queryBase
    #                        ejemplo: [1111L, 1112L]
    #       pdctNames_lst -> contiene el listado con los product.name entre las fechas especificadas queryBase
    #                        ejemplo: ['Acelga organica', 'Banano Bocadillo organico', 'Banano organico', 'Brocoli organico', ...]
    #       pdctId_lst  ->   contiene los product.id entre las fechas especificadas por queryBase
    #                        ejemplo: [481L, 493L, 494L, 497L, 542L, 567L, 583L, 590L]
    # OUTPUT:
    #       summaryChart_lst -> es un listado de listas que contiene el consolidado de todos los pedidos entreg las fechas del queryBase con nombre de producto y total
    #                        ejemplo: [['Acelga organica', 1000, 500, 1500], ['Banano Bocadillo organico', 0, 6, 6], ['Banano organico', 18, 0, 18],...]


    # CREA la lista donde guarda el consolidado como lista de sublistas
    summaryChart_lst =[]

    for i in range(len(pdctId_lst)):  # REPETIR para cada product.id de la lista
        # CREA la lista donde guardara todos los datos del consolidado o reinicia la lista con cada pdctIds_lst
        summaryChartRow_lst = [] # esta lista guardara el product.name, qty*pres y totales
        summaryChartRow_lst.append(pdctNames_lst[i]) # OBTIENE el nombre y lo ingresa en summaryChartRow_lst

        for poNumber in poNumber_lst:  # REPETIR para cada po.po_number de la lista
            poProductId_lst = []
            poProductPres_lst=[]
            poProductQty_lst=[]
            queryPos = queryBase
            queryPos &= db.po.po_number == poNumber  # CONSULTE el listado de productos para el po.poNumber del loop
            products_lst = db(queryPos).select(db.po.po_number, db.po_detail.product_id,
                                                   db.po_detail.quantity,
                                                   db.product.name,
                                                   db.product.pres, db.po.customer_id, orderby="product.name",
                                                   groupby='product.id').as_list()

            print "\n","    los detalles del pedido son: ", products_lst

            # OBTIENE LOS product.id de los que hacen parte del pedido
            productsId_lst = db(queryPos).select(db.po_detail.product_id, groupby='po_detail.product_id').as_list()
            print "\n", "     los ids de los del pedido son: ", productsId_lst
            # CONVIERTE la lista que contiene product.id lo demas lo elimina
            for j in range(len(productsId_lst)):
                poProductId_lst.append(productsId_lst[j]['product_id'])
            print "\n","    estos son los ids por pedido", poProductId_lst

            # OBTIENE los product.pres de los que hacen parte del pedido
            productsPres_lst = db(queryPos).select(db.product.pres, groupby='po_detail.product_id').as_list()
            for j in range(len(productsPres_lst)):
                poProductPres_lst.append(productsPres_lst[j]['pres'])
            print "\n","    este es el listado de presentaciones", poProductPres_lst

            # OBTIENE los po_detail.qty de los que hacen parte del pedido
            productsQty_lst = db(queryPos).select(db.po_detail.quantity, groupby='po_detail.product_id').as_list()
            for j in range(len(productsQty_lst)):
                poProductQty_lst.append(productsQty_lst[j]['quantity'])
            print  "\n","    este es el listado de cantidades: ", poProductQty_lst
            print "\n", "    el product.id a buscar es:", pdctId_lst[i]
            if pdctId_lst[i] in poProductId_lst: # SI el product.id del consolidado esta en los de ese pedido...
                position_lst = [k for k, x in enumerate(poProductId_lst) if x ==pdctId_lst[i]] # BUSQUE donde esta y devuelva la posicion como entero
                position = position_lst[0] # CONVIERTE el resultado anterior a un entero
                print "\n","la posicion del product.id en la lista de los ids del pedido es: ", position
                summaryChartRow_lst.append(int(poProductQty_lst[position])*int(poProductPres_lst[position])) # OBTIENE la cantidad y presentacion, las multiplica y las agrega al consolidado
            else:
                print "\n", "       no esta"
                summaryChartRow_lst.append(0) # SI el product.id no esta en ese pedido agregue un cero a la lista
            print "\n", "la lista por producto es: ", summaryChartRow_lst
        summaryChartRow_lst.append(int(sum(summaryChartRow_lst[1:]))) # TOTALIZA la cantidades por producto y lo agrega a la lista
        summaryChart_lst.append(summaryChartRow_lst) # AGREGA ese producto en el consolidado total
    print "\n"*2, "el consolidado total es: summaryChart_lst ", summaryChart_lst
    print "*"*10, "FIN DE CHART GENERATOR","*"*10

    return summaryChart_lst

def htmlGenerator(po_lst, chart_lst):
    # esta funcion convierte el consolidado de los pedidos a una tabla en html
    # INPUT:
    #       pos_lst: -> contiene un listado con los po.po_number entre las fechas especificadas queryBase
    #                   ejemplo: [1111L, 1112L]
    #       chart_lst:  -> es el consolidado de productos de los productos
    #                  ejemplo: [['Acelga organica', 1000, 500, 1500], ['Banano Bocadillo organico', 0, 6, 6], ['Banano organico', 18, 0, 18],...]
    # OUTPUT:
    #        archivo html de nombre Consolidado-Pedidos.html con una columna entre cada pedido titulada "ENTREGADO" que contiene un espacio

    print "+++++++++++++++++  STARTING htmlGenerator  ++++++++++++++++++++++++++"
    header_lst = po_lst
    header_lst.insert(0,"PRODUCTO")
    header_lst.insert(len(po_lst), "TOTAL")
    #header_lst = ["producto", "1111", "ENTREGADO", "1112","ENTREGADO", "total", "ENTREGADO"] # TODO header_lst auto

    consolidado_lst = chart_lst
    print ("consolidado_lst es: ", chart_lst)

    for i in range(len(header_lst)):
        if i != 0:
            position = 2*i
            header_lst.insert(position, "ENTREGADO")


    for  consolidado in consolidado_lst:
        for i in range(len(consolidado)):
            if i !=0:
                position = 2*i
                consolidado.insert(position, "     ")
                #header_lst.insert(position, "ENTREGADO")
    htmlcode = HTML.table(consolidado_lst, header_row=header_lst)  # crea el codigo html de la tabla
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
    f = open("consolidado-Pedidos", "w")  # crea archivo html
    f.write(html)  # Escribe en el archivo html
    f.close()  # Guarda archivo html
    print "*" * 10, "FIN HTML GENERATOR", "*" * 10
    return consolidado_lst

def getPo(queryBase):
    # esta funcion obtiene un listado con todos los po.po_number consolidados
    # INPUT:
    #       queryBase str -> es query tipo DAL web2py con el listado de los productos entre las fechas ingresadas
    #                      ejemplo: ((((po.id = po_detail.po_id) AND (po_detail.product_id = product.id)) AND (po.date >= '2017-05-23 17:43:11')) AND (po.date <= '2017-05-26 15:16:00'))
    # OUTPUT pdctName_lst -> es la lista con str que product.name
    #                       ejemplo: [1111L, 1112L]

    print "+++++++++++++++++  STARTING GET PO NUMBER FUNCTION   ++++++++++++++++++++++++++"
    poNumber_lst_dic = db(queryBase).select(db.po.po_number, groupby='po_number').as_list()
    poNumber_lst =[]
    for poNumber in range(len(poNumber_lst_dic)):
        poNumber_lst.append(poNumber_lst_dic[poNumber]['po_number'])

    return poNumber_lst

def getNames(queryBase):
    # esta funcion obtiene el listado de todos los nombres de los productos solicitados de forma consolidada y alfabeticamente
    # INPUT:
    #       queryBase str -> es query tipo DAL web2py con el listado de los productos entre las fechas ingresadas
    #                      ejemplo: ((((po.id = po_detail.po_id) AND (po_detail.product_id = product.id)) AND (po.date >= '2017-05-23 17:43:11')) AND (po.date <= '2017-05-26 15:16:00'))
    # OUTPUT pdctName_lst -> es la lista con str que product.name
    #                       ejemplo: ['Acelga organica', 'Banano Bocadillo organico', 'Banano organico', 'Brocoli organico', ...]

    print "+++++++++++++++++  STARTING GET NAMES FUNCTION   ++++++++++++++++++++++++++"
    # CONSULTA  para tener un listado consolidado de product.name y product.id solicitados y en orden alfabetico
    pdctNames_lst_dic = db(queryBase).select(db.po_detail.product_id, db.product.name, orderby='product.name', groupby='product.id').as_list()
    # CREA una lista que albergara todos los nombres de la conulta
    pdctNames_lst=[]

    # OBTIENE los product.name desechando lo demas
    for i in range(len(pdctNames_lst_dic)):
        pdctNames_lst.append(pdctNames_lst_dic[i]['product']['name'])

    return pdctNames_lst

def getIds(queryBase):
    # esta funcion obtiene una lista de todos los product.id solicitados consolidados y en orden alfabetico por nombre de producto
    # INPUT:
    #       queryBase str -> es query tipo DAL web2py con el listado de los productos entre las fechas ingresadas
    #                      ejemplo: ((((po.id = po_detail.po_id) AND (po_detail.product_id = product.id)) AND (po.date >= '2017-05-23 17:43:11')) AND (po.date <= '2017-05-26 15:16:00'))
    # OUTPUT: pdctId_lst -> es una lista con int que contiene los product.id
    #                       ejemplo: [481L, 493L, 494L, 497L, 542L, 567L, 583L, 590L]

    print "+++++++++++++++++  STARTING GET IDS FUNCTION  ++++++++++++++++++++++++++"
    # CONSULTA para obtener una listado ordenado de los productos solicitados sin repeticiones
    pdctId_lst_dic = db(queryBase).select(db.po_detail.product_id, db.product.name, orderby='product.name',  groupby='product.id').as_list()
    # CREA la lista que contendra todos los ids de la consulta
    pdctId_lst = []

    # OBTIENE todos los ids de la consulta desechando lo demas
    for i in range(len(pdctId_lst_dic)):
        pdctId_lst.append(pdctId_lst_dic[i]['po_detail']['product_id'])

    return pdctId_lst

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