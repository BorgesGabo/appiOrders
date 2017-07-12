def ppal (queryBase):
    # 1. CALL getNames
    names = getNames(queryBase)


    # 2. CALL  getIds & pass through charGenerator
    ids = getIds(queryBase)
    #ids_dic = chartGenerator(ids)

    # 3. CALL productsPerPo
    pdcts = productsPerPo(queryBase)

    # 4. CALL chartGenertator
    chart = chartGenerator(ids, pdcts['a'])

    print "estos son los products.name sin repetir"
    print names
    print "\n"
    print "esto son los products.ids sin repetir"
    print ids
    print "\n"
    print "los pos.ids sin repetir"

    print pdcts['b']
    print "\n"
    print "products by po"
    print pdcts['a']
    print "\n"
    #print "esta es a lista preliminar de subtotales"
    #print ids_dic

    print "\n"
    print "este es el cuadro"
    print chart
    return

def chartGenerator(pdctId_lst, productsPerPo_lst, pdctName_lst):

    # INPUT pdctNames_lst: all the product names grouped by name w.o. repetition

    # GENERATES  a dic with lists named as each product id
    totals_dic = {}
    for pdct in pdctId_lst:
        name = "producto_" + str(pdct)
        totals_dic[name] = []
'''
    for j in range(len(productsPerPo_lst)):  # loops over ea purchase order
        for k in range(len(productsPerPo_lst[j])):  # loops over ea product
            print productsPerPo_lst[j][k]['po_detail'].values()
            for ids in pdctId_lst:
                exist = ids in productsPerPo_lst[j][k][
                    'po_detail'].values()  # check if the product.id of the list is in the product "k" of purchase order "j"
                pres = productsPerPo_lst[j][k]['product']['pres']
                qty = productsPerPo_lst[j][k]['po_detail']['quantity']
                print ("for j: ", j, " k: ", k, "id is:", ids, "exist is: ")
                print exist
                if exist != False:
                    totals_dic["producto_" + str(ids)].append(int(pres) * int(qty))
                if ids == pdctId_lst[-1]:
                    print "este es el ultimo"
                totals_dic["producto_" + str(ids)].append(sum(totals_dic))'''

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
                    totals_dic["producto_" + str(ids)].append(int(pres) * int(qty))  # Incluye en la lista subtotales

    # ADDS product's names and adds up the sublist elements
    for i in range(len(pdctNames_lst)):
        pdctName = str(pdctNames_lst[i])
        totals_lst = totals_dic["producto_" + str(pdctId_lst[i])]
        #print "pdctName[i]: "
        #print pdctNames_lst[i]
        #print "totals_dic"
        #print totals_dic["producto_" + str(pdctId_lst[i])]
        totals_lst.insert(0,pdctNames_lst[i])
        totals_lst.insert(len(totals_lst), sum(totals_lst[1:]))
        totals = totals_dic.values() # Convierte el diccionario en lista de sublistas
    return totals

    return totals_dic

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