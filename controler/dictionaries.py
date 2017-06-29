selectedOrders_lst=[{'product': {'name': 'Acelga organica', 'pres': '500'}, 'po_detail': {'product_id': 481L, 'quantity': '2'}, 'po': {'po_number': 1111L, 'customer_id': 1L}}, {'product': {'name': 'Huevos de granja organica', 'pres': '6'}, 'po_detail': {'product_id': 542L, 'quantity': '2'}, 'po': {'po_number': 1111L, 'customer_id': 1L}}, {'product': {'name': 'Papa criolla organica', 'pres': '500'}, 'po_detail': {'product_id': 567L, 'quantity': '3'}, 'po': {'po_number': 1111L, 'customer_id': 1L}}, {'product': {'name': 'Banano organico', 'pres': '6'}, 'po_detail': {'product_id': 494L, 'quantity': '3'}, 'po': {'po_number': 1111L, 'customer_id': 1L}}, {'product': {'name': 'Banano Bocadillo organico', 'pres': '6'}, 'po_detail': {'product_id': 493L, 'quantity': '1'}, 'po': {'po_number': 1112L, 'customer_id': 18L}}, {'product': {'name': 'Brocoli organico', 'pres': '500'}, 'po_detail': {'product_id': 497L, 'quantity': '1'}, 'po': {'po_number': 1112L, 'customer_id': 18L}}, {'product': {'name': 'Pollo de huerta org.', 'pres': '1'}, 'po_detail': {'product_id': 583L, 'quantity': '2'}, 'po': {'po_number': 1112L, 'customer_id': 18L}}, {'product': {'name': 'Acelga organica', 'pres': '500'}, 'po_detail': {'product_id': 481L, 'quantity': '1'}, 'po': {'po_number': 1112L, 'customer_id': 18L}}, {'product': {'name': 'Tomate chonto organico', 'pres': '1000'}, 'po_detail': {'product_id': 590L, 'quantity': '2'}, 'po': {'po_number': 1112L, 'customer_id': 18L}}]
pos_lst=[{'po_number': 1111L}, {'po_number': 1112L}]
selectedOrders_dic = selectedOrders_lst[0]['product']
print ("selectedOrders are: ")
print selectedOrders_lst
print "\n"
print ("containing: ", len(selectedOrders_lst), "elements")
print "\n"
print ("selectedOrders_lst[0] is or in other words the product is: ")
print selectedOrders_lst[0]
print "\n"
print ("the values of a[0]['product'] are: ", selectedOrders_dic.values(), "\n")
print ("selectedOrders_lst[1] is: ", selectedOrders_lst[1])
b_dic = selectedOrders_lst[1]['po_detail']['product_id']
print ("selectedOrders_lst[1]['po_detail']['product_id'] is: ",b_dic, "\n")
print "*******filtering****"

c_lst = []
for i in range(len(selectedOrders_lst)):

    c = selectedOrders_lst[i]['po_detail']['product_id']
    c_lst.append(c)
    '''for j in range(len(pos_lst)):
        d = selectedOrders_lst[]
print ("c_dict es: ", c_lst)'''
'''
pos_lst = []
pos_lst_dic = [{'po_number': 1111L}, {'po_number': 1112L}]
for i in range(len(pos_lst_dic)):
    print i
    pos_lst.append(pos_lst_dic[i].values())
print pos_lst'''

''''def queryGen(query):
    # GET quantities and pres per product
    # INPUT query:str
    # OUTPUT

    pos_lst_dic = db(query).select(db.po.id,
                                   groupby='po_number').as_list()  # GET the number of pos in the range of dates
    print "******************"
    print pos_lst_dic
    # pos_lst_dic es: [{'po.id': 1L}, {'po.id': 2L}]
    pos_lst = []

    for i in range(len(pos_lst_dic)):
        pos_lst.append(pos_lst_dic[i]['id'])
    # print pos_lst
    # pos_lst es: [1L, 2L]
    for i in range(len(pos_lst)):
        poi = pos_lst[i]
        print ("poi es: ", poi)
        querypos = query
        querypos &= db.po_detail.po_id == poi
        print ("querypos es:", querypos)
        selectedOrdersPerPo_lst = db(querypos).select(db.po.po_number, db.po_detail.product_id, db.po_detail.quantity,
                                                      db.product.name,
                                                      db.product.pres, db.po.customer_id).as_list()
        print ("Orders per po", selectedOrdersPerPo_lst)

        # [{'product': {'name': 'Acelga organica', 'pres': '500'}, 'po_detail': {'product_id': 481L, 'quantity': '2'}, 'po': {'po_number': 1111L, 'customer_id': 1L}},
        # {'product': {'name': 'Huevos de granja organica', 'pres': '6'}, 'po_detail': {'product_id': 542L, 'quantity': '2'}, 'po': {'po_number': 1111L, 'customer_id': 1L}},
        # {'product': {'name': 'Papa criolla organica', 'pres': '500'}, 'po_detail': {'product_id': 567L, 'quantity': '3'}, 'po': {'po_number': 1111L, 'customer_id': 1L}},
        # {'product': {'name': 'Banano organico', 'pres': '6'}, 'po_detail': {'product_id': 494L, 'quantity': '3'}, 'po': {'po_number': 1111L, 'customer_id': 1L}}]

    return'''

def return_sum(x,y):
    c = x + y
    return c

res = return_sum(4,5)
print(res)

def mult(a):
    ans = a+2
    return ans
print mult(2)

def querySupplier(query):
    print "---------------------------------------"
    for i in range(0, 4):
        if i == 0:
            queryS = query
        else:
            queryS = query
            queryS &= db.product.supplier_id == i
        selectedOrderSup_lst = db(queryS).select(db.po.po_number, db.po_detail.product_id,
                                                  db.po_detail.quantity, db.product.name,
                                                 db.product.pres, db.po.customer_id, orderby='po_number').as_list()
        queryPo(selectedOrderSup_lst, queryS)
        #print queryS
        #print selectedOrderSup_lst
    return selectedOrderSup_lst

def queryPo(selectedOrderSup_lst ,queryS):
    if len(selectedOrderSup_lst) != 0:
        # GET quantities and pres per purchase order
        # INPUT selectedOrderSup_lst ,queryS: str
        # OUTPUT

        pos_lst_dic = db(queryS).select(db.po.id,
                                       groupby='po_number').as_list()  # GET the number of pos in the range of dates
        print "******************"
        print pos_lst_dic
        # pos_lst_dic es: [{'po.id': 1L}, {'po.id': 2L}]
        pos_lst = []

        for i in range(len(pos_lst_dic)):
            pos_lst.append(pos_lst_dic[i]['id'])
        # print pos_lst
        # pos_lst es: [1L, 2L]
        for i in range(len(pos_lst)):
            poi = pos_lst[i]
            print ("poi es: ", poi)
            querypos = queryS
            querypos &= db.po_detail.po_id == poi
            print ("querypos es:", querypos)
            selectedOrdersPerPo_lst = db(querypos).select(db.po.po_number, db.po_detail.product_id,
                                                          db.po_detail.quantity,
                                                          db.product.name,
                                                          db.product.pres, db.po.customer_id).as_list()
            print ("Orders per po", selectedOrdersPerPo_lst)

            # [{'product': {'name': 'Acelga organica', 'pres': '500'}, 'po_detail': {'product_id': 481L, 'quantity': '2'}, 'po': {'po_number': 1111L, 'customer_id': 1L}},
            # {'product': {'name': 'Huevos de granja organica', 'pres': '6'}, 'po_detail': {'product_id': 542L, 'quantity': '2'}, 'po': {'po_number': 1111L, 'customer_id': 1L}},
            # {'product': {'name': 'Papa criolla organica', 'pres': '500'}, 'po_detail': {'product_id': 567L, 'quantity': '3'}, 'po': {'po_number': 1111L, 'customer_id': 1L}},
            # {'product': {'name': 'Banano organico', 'pres': '6'}, 'po_detail': {'product_id': 494L, 'quantity': '3'}, 'po': {'po_number': 1111L, 'customer_id': 1L}}]

        return