from methods import *


status_root1, root1, _ = org.create_root(attributes={})
id_root1 = root1[0]['id']
path_root1 = root1[0]['path']
order_root1 = root1[0]['inner_order']

status_child2lvl, child2lvl, _ = org.create_child(attributes={}, node_id=id_root1)
id_child2lvl = child2lvl[0]['id']
path_child2lvl = child2lvl[0]['path']
order_child2lvl = child2lvl[0]['inner_order']

status_root2, root2, _ = org.create_root(attributes={})
id_root2 = root2[0]['id']
path_root2 = root2[0]['path']
order_root2 = root2[0]['inner_order']

status_sec_child2lvl, sec_child2lvl, _ = org.create_child(attributes={}, node_id=id_root1)
id_sec_child2lvl = sec_child2lvl[0]['id']
path_sec_child2lvl = sec_child2lvl[0]['path']
order_sec_child2lvl = sec_child2lvl[0]['inner_order']

status_child3lvl, child3lvl, _ = org.create_child(attributes={}, node_id=id_child2lvl)
id_child3lvl = child3lvl[0]['id']
path_child3lvl = child3lvl[0]['path']
order_child3lvl = child3lvl[0]['inner_order']