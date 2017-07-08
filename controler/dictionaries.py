selectedOrders_lst=[{'product': {'name': 'Acelga organica', 'pres': '500'}, 'po_detail': {'product_id': 481L, 'quantity': '2'}, 'po': {'po_number': 1111L, 'customer_id': 1L}}, {'product': {'name': 'Huevos de granja organica', 'pres': '6'}, 'po_detail': {'product_id': 542L, 'quantity': '2'}, 'po': {'po_number': 1111L, 'customer_id': 1L}}, {'product': {'name': 'Papa criolla organica', 'pres': '500'}, 'po_detail': {'product_id': 567L, 'quantity': '3'}, 'po': {'po_number': 1111L, 'customer_id': 1L}}, {'product': {'name': 'Banano organico', 'pres': '6'}, 'po_detail': {'product_id': 494L, 'quantity': '3'}, 'po': {'po_number': 1111L, 'customer_id': 1L}}, {'product': {'name': 'Banano Bocadillo organico', 'pres': '6'}, 'po_detail': {'product_id': 493L, 'quantity': '1'}, 'po': {'po_number': 1112L, 'customer_id': 18L}}, {'product': {'name': 'Brocoli organico', 'pres': '500'}, 'po_detail': {'product_id': 497L, 'quantity': '1'}, 'po': {'po_number': 1112L, 'customer_id': 18L}}, {'product': {'name': 'Pollo de huerta org.', 'pres': '1'}, 'po_detail': {'product_id': 583L, 'quantity': '2'}, 'po': {'po_number': 1112L, 'customer_id': 18L}}, {'product': {'name': 'Acelga organica', 'pres': '500'}, 'po_detail': {'product_id': 481L, 'quantity': '1'}, 'po': {'po_number': 1112L, 'customer_id': 18L}}, {'product': {'name': 'Tomate chonto organico', 'pres': '1000'}, 'po_detail': {'product_id': 590L, 'quantity': '2'}, 'po': {'po_number': 1112L, 'customer_id': 18L}}]
pos_lst=[{'po_number': 1111L}, {'po_number': 1112L}]
selectedOrders_dic = selectedOrders_lst[0]['product']
productsPerPo_lst = [[{'product': {'name': 'Acelga organica', 'pres': '500'}, 'po_detail': {'product_id': 481L, 'quantity': '2'}, 'po': {'po_number': 1111L, 'customer_id': 1L}}, {'product': {'name': 'Huevos de granja organica', 'pres': '6'}, 'po_detail': {'product_id': 542L, 'quantity': '2'}, 'po': {'po_number': 1111L, 'customer_id': 1L}}, {'product': {'name': 'Papa criolla organica', 'pres': '500'}, 'po_detail': {'product_id': 567L, 'quantity': '3'}, 'po': {'po_number': 1111L, 'customer_id': 1L}}, {'product': {'name': 'Banano organico', 'pres': '6'}, 'po_detail': {'product_id': 494L, 'quantity': '3'}, 'po': {'po_number': 1111L, 'customer_id': 1L}}], [{'product': {'name': 'Banano Bocadillo organico', 'pres': '6'}, 'po_detail': {'product_id': 493L, 'quantity': '1'}, 'po': {'po_number': 1112L, 'customer_id': 18L}}, {'product': {'name': 'Brocoli organico', 'pres': '500'}, 'po_detail': {'product_id': 497L, 'quantity': '1'}, 'po': {'po_number': 1112L, 'customer_id': 18L}}, {'product': {'name': 'Pollo de huerta org.', 'pres': '1'}, 'po_detail': {'product_id': 583L, 'quantity': '2'}, 'po': {'po_number': 1112L, 'customer_id': 18L}}, {'product': {'name': 'Acelga organica', 'pres': '500'}, 'po_detail': {'product_id': 481L, 'quantity': '1'}, 'po': {'po_number': 1112L, 'customer_id': 18L}}, {'product': {'name': 'Tomate chonto organico', 'pres': '1000'}, 'po_detail': {'product_id': 590L, 'quantity': '2'}, 'po': {'po_number': 1112L, 'customer_id': 18L}}]]


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

print "esta es la prueba"
print selectedOrders_lst[0]['product']['pres']

'''
# este obtiene la presentacion de ea producto y lo guarda en un alista
lista =[]
for j in range(len(selectedOrders_lst)):
    lista.append(selectedOrders_lst[j]['product']['pres'])
print lista
'''
#This get the orders names repeated
pdctId = []
for j in range(len(selectedOrders_lst)):
    pdctId.append(selectedOrders_lst[j]['po_detail']['product_id'])
print "this is product id"
print pdctId

listNames = {}
for pdct in pdctId:
    name = "poducto_"+str(pdct)
    listNames[name] = []
print listNames

names = [1, 2, 3, 4, 5]
for name in names:
    print name

for i in range (len(names)):

    print "este es i: "
    print i
    print "\n"
    print "lista"+"A"


def return_sum(x,y):
    c = x + y
    return c

res = return_sum(4,5)
print(res)

def mult(a):
    ans = a+2
    return ans
print mult(2)

def controller(a,y):
    x = mult(a)
    z = return_sum(x,y)
    return z
print (controller(2,5))
print  "\n"

ids_lst = [481L, 493L, 494L, 497L, 542L, 567L, 583L, 590L]
print ("productsbypo are: ", productsPerPo_lst)

'''
for j in range(len(productsPerPo_lst)):  # loops over ea purchase order
    for k in range(len(productsPerPo_lst[j])): # loops over ea product
        print productsPerPo_lst[j][k]['po_detail'].values()
        for ids in ids_lst:
            exist = ids in productsPerPo_lst[j][k]['po_detail'].values()
            print ("for j: ", j, " k: ", k,"id is:", ids ,"exist is: ")
            print exist
'''
# loops over ea purchase order
for j in range(len(productsPerPo_lst)):  # loops over ea purchase order
    for k in range(len(productsPerPo_lst[j])):  # loops over ea product
        print productsPerPo_lst[j][k]['po_detail'].values()
        for ids in ids_lst:
            exist = ids in productsPerPo_lst[j][k]['po_detail'].values()
            clave =
            print ("for j: ", j, " k: ", k, "id is:", ids, "exist is: ")
            print exist
            if exist == False:
                totals_dic["producto_" + str(ids)] = 0
            else:
                totals_dic["producto_" + str(ids)] = 1
