import pytest
from nodes import *


# Базовые тесты на создание корневых узлов
# OS-API-Cr-1, OS-API-Cr-2
@pytest.mark.order(1)
def test_create_root_positive():
    status, response, res_headers = org.create_root(attributes=None, wrong_data={'project_id': project_id,
                                                                                 'item_type': item_type, 'item': item,
                                                                                 'attributes': '{"name": "Компания Ромашка", "description": "ПО"}'})
    # print(f"\nCode: {status}")
    # print(f"Response: {response}")
    # print(f'Response headers: {res_headers}')
    id_node = response[0]['id']
    assert status == 201
    assert response[0]['project_id'] == project_id
    assert response[0]['item_type'] == item_type
    assert response[0]['item'] == item
    assert response[0]['id'] != 0
    assert response[0]['path'] == '0' * (10 - len(str(id_node))) + str(id_node)
    assert 'inner_order' in str(response[0])
    assert response[0]['attributes'] == '{"name": "Компания Ромашка", "description": "ПО"}'
    assert response[0]['level_node'] == 1
    assert "'Content-Type': 'application/json'" in str(res_headers)


# Базовые тесты на создание дочек разных уровней
# OS-API-Cc-1, OS-API-Cc-2, OS-API-Cc-3, OS-API-Cc-4, OS-API-Cc-5, OS-API-Cc-6, OS-API-Cc-37
@pytest.mark.order(2)
def test_create_child_positive():
    status, response, res_headers = org.create_child(attributes=None, node_id=id_root2,
                                                     wrong_data={'project_id': project_id,
                                                                 'item_type': item_type, 'item': item,
                                                                 'attributes': '{"name": "other child 2lvl"}'})
    # print(f"\nCode: {status}")
    # print(f"Response: {response}")
    # print(f'Response headers: {res_headers}')
    id_node = response[0]['id']
    assert status == 201
    assert response[0]['project_id'] == project_id
    assert response[0]['item_type'] == item_type
    assert response[0]['item'] == item
    assert response[0]['id'] != 0
    assert response[0]['path'] == path_root2 + ('0' * (10 - len(str(id_node))) + str(id_node))
    assert response[0]['attributes'] == '{"name": "other child 2lvl"}'
    assert response[0]['level_node'] == 2
    assert "'Content-Type': 'application/json'" in str(res_headers)
    assert 'inner_order' in str(response[0])


# Тесты на отправку запросов с несовпадением обязательных полей с родителем
# OS-API-Cc-25, OS-API-Cc-26, OS-API-Cc-27
@pytest.mark.order(3)
def test_create_child_value_in_fields_not_equal_parent():
    status, response, res_headers = org.create_child(node_id=id_root2, attributes=None,
                                                     wrong_data={'project_id': other_project_id, 'item_type': item_type,
                                                                 'item': item, 'attributes': {}})
    # print(f"\nCode: {status}")
    # print(f"Response: {response}")
    # print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 404
    assert "'id': " not in str(response[0])
    assert 'error' in str(response[0])
    assert "Objects for verification not received" in str(response[0])


# Базовый тест на получение пустого списка по несозданному дереву
# OS-API-Gt-1
@pytest.mark.order(4)
def tests_get_empty_tree():
    status, response, res_headers = org.get_tree(wrong_params={'project_id': project_id,
                                                               'item_type': item_type,
                                                               'item': other_item})
    # print(f"\nCode: {status}")
    # print(f"Response: {response}")
    # print(f'Response headers: {res_headers}')
    assert status == 200
    assert len(response[0]) == 0
    assert "'Content-Type': 'application/json'" in str(res_headers)


# Базовый тест на получение созданного дерева
# OS-API-Gt-2
@pytest.mark.order(5)
def test_get_tree_positive():
    status, response, res_headers = org.get_tree()
    # print(f"\nCode: {status}")
    # print(f"Response: {response}")
    # print(f'Response headers: {res_headers}')
    assert status == 200
    assert len(response[0]) != 0
    nodes = []
    for node in response[0]:
        nodes.append(node)
    for s in nodes:
        assert 'project_id' in s
        assert 'item_type' in s
        assert 'item' in s
        assert 'id' in s
        assert 'path' in s
        assert 'inner_order' in s
        assert 'attributes' in s
        assert 'level_node' in s
    assert "'Content-Type': 'application/json'" in str(res_headers)


# Проверка сортировки узлов при получении созданного дерева
# OS-API-Gt-2
@pytest.mark.order(6)
def test_get_tree_check_default_sorted_tree():
    status, response, res_headers = org.get_tree()
    # print(f"\nCode: {status}")
    # print(f"Response: {response}")
    # print(f'Response headers: {res_headers}')
    assert status == 200
    assert len(response[0]) != 0
    new_nodes = []
    id_new_nodes_sorted = [id_root1, id_child2lvl, id_child3lvl, id_sec_child2lvl, id_root2]
    for i in response[0]:
        if i['id'] in id_new_nodes_sorted:
            new_nodes.append(i['id'])
    # print(new_nodes)
    assert new_nodes == id_new_nodes_sorted


# Тест на получение дерева с сортировкой узлов по id
# OS-API-Gt-38
@pytest.mark.order(7)
def test_get_tree_sorted_by_id():
    status, response, res_headers = org.get_tree(wrong_params={'project_id': project_id, 'item_type': item_type,
                                                               'item': item, 'sort_by_id': True})
    # print(f"\nCode: {status}")
    # print(f"Response: {response}")
    # print(f'Response headers: {res_headers}')
    assert status == 200
    assert len(response[0]) != 0
    new_nodes = []
    id_new_nodes_sorted = [id_root1, id_child2lvl, id_root2, id_sec_child2lvl, id_child3lvl]
    for i in response[0]:
        if i['id'] in id_new_nodes_sorted:
            new_nodes.append(i['id'])
    assert new_nodes == id_new_nodes_sorted


# Базовый тест на получение пустого списка при отсутствии дочек у узла
# OS-API-Gc-1
@pytest.mark.order(8)
def test_get_descendants_empty():
    status, response, res_headers = org.get_descendants(node_id=id_sec_child2lvl)
    # print(f"\nCode: {status}")
    # print(f"Response: {response}")
    # print(f'Response headers: {res_headers}')
    assert status == 200
    assert len(response[0]) == 0
    assert "'Content-Type': 'application/json'" in str(res_headers)


# Базовый тест на получение всех дочек узлов разных уровней
# OS-API-Gc-2, OS-API-Gc-3, OS-API-Gc-4
@pytest.mark.order(9)
def test_get_descendants_positive():
    _, get_parent, _ = org.get_node(id_root1)
    # print(get_parent)
    status, response, res_headers = org.get_descendants(node_id=id_root1)
    # print(f"\nCode: {status}")
    # print(f"Response: {response}")
    # print(f'Response headers: {res_headers}')
    assert status == 200
    assert len(response[0]) != 0
    nodes = []
    for node in response[0]:
        nodes.append(node)
    for s in nodes:
        assert 'project_id' in s
        assert 'item_type' in s
        assert 'item' in s
        assert 'id' in s
        assert 'path' in s
        assert 'inner_order' in s
        assert 'attributes' in s
        assert 'level_node' in s
        if s['level_node'] >= 1:
            assert s['path'][:1 * 10] == path_root1
        assert s['id'] != id_root1
    child_nodes = []
    for node in response[0]:
        child_nodes.append(node['id'])
    # print(child_nodes)
    assert child_nodes == [id_child2lvl, id_child3lvl, id_sec_child2lvl]
    assert "'Content-Type': 'application/json'" in str(res_headers)


# Тест на отправку запроса get_descendants с параметром depth
# OS-API-Gc-51, # OS-API-Gc-52, # OS-API-Gc-53, # OS-API-Gc-54
@pytest.mark.order(10)
def test_get_descendants_with_depth():
    status, response, res_headers = org.get_descendants(node_id=id_root1, wrong_params={'project_id': project_id,
                                                                                     'item_type': item_type,
                                                                                     'item': item, 'depth': 1})
    # print(f"\nCode: {status}")
    # print(f"Response: {response}")
    # print(f'Response headers: {res_headers}')
    assert status == 200
    assert len(response[0]) != 0
    child_nodes = []
    for node in response[0]:
        child_nodes.append(node['id'])
    # print(child_nodes)
    assert child_nodes == [id_child2lvl, id_sec_child2lvl]


# Базовый тест на получение узла любого уровня
# OS-API-Gn-4, OS-API-Gn-5, OS-API-Gn-6, OS-API-Gn-7
@pytest.mark.order(11)
def test_get_node_positive():
    status, response, res_headers = org.get_node(node_id=id_root1)
    # print(f"\nCode: {status}")
    # print(f"Response: {response}")
    # print(f'Response headers: {res_headers}')
    assert status == 200
    assert response[0]['project_id'] == project_id
    assert response[0]['item_type'] == item_type
    assert response[0]['item'] == item
    assert response[0]['id'] == id_root1
    assert response[0]['path'] == path_root1
    assert response[0]['inner_order'] == order_root1
    assert response[0]['level_node'] == 1
    assert response[0]['attributes'] == '{}'
    assert "'Content-Type': 'application/json'" in str(res_headers)


# Тесты на отправку запросов с несуществующим id в url
# OS-API-Gn-31
@pytest.mark.order(12)
def test_get_node_with_nonexistent_id_node():
    status, response, res_headers = org.get_node(node_id=100000, wrong_url=None, wrong_headers=None, wrong_data=None,
                                                 wrong_params=None)
    # print(f"\nCode: {status}")
    # print(f"Response: {response}")
    # print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 404
    assert "'id': " not in str(response[0])
    assert 'error' in str(response[0])
    assert "does not exist object(s)" in str(response[0])


# Базовые тесты на изменение атрибутов узлов всех уровней
# OS-API-Ua-1, OS-API-Ua-2, OS-API-Ua-3, OS-API-Ua-4
@pytest.mark.order(13)
def test_change_attributes_positive():
    status, response, res_headers = org.change_attributes(attributes={"name": "new name",
                                                                      "description": "new description"},
                                                          node_id=id_root2)
    # print(f"\nCode: {status}")
    # print(f"Response: {response}")
    # print(f'Response headers: {res_headers}')
    assert status == 201

    org.change_attributes(attributes={}, node_id=id_root2)

    assert response[0]['project_id'] == project_id
    assert response[0]['item_type'] == item_type
    assert response[0]['item'] == item
    assert response[0]['id'] == id_root2
    assert response[0]['path'] == path_root2
    assert response[0]['inner_order'] == order_root2
    assert response[0]['level_node'] == 1
    assert response[0]['attributes'] == '{"name": "new name", "description": "new description"}'
    assert "'Content-Type': 'application/json'" in str(res_headers)


# Базовый тест на изменение порядка узлов всех уровней
# OS-API-Uo-1, OS-API-Uo-2, OS-API-Uo-3, OS-API-Uo-4
@pytest.mark.order(14)
def test_change_order_positive():
    # _, changing_node_out, _ = org.get_node(node_id=id_child2lvl)
    # print(changing_node_out)
    # _, changing_node_in, _ = org.get_node(node_id=id_sec_child2lvl)
    # print(changing_node_in)
    status, change_response, res_headers = org.change_order(node_id_out=id_child2lvl, node_id_in=id_sec_child2lvl)
    # print(f"\nCode: {status}")
    # print(f"Response: {change_response}")
    # print(f'Response headers: {res_headers}')
    assert status == 201
    _, get_response, _ = org.get_node(node_id=id_child2lvl)
    _, response_get_descendants, _ = org.get_descendants(node_id=id_child2lvl)

    org.change_order(node_id_out=id_sec_child2lvl, node_id_in=id_child2lvl)

    assert change_response[0] == f"Node {id_child2lvl} moved on node's {id_sec_child2lvl} position"
    assert get_response[0]['project_id'] == project_id
    assert get_response[0]['item_type'] == item_type
    assert get_response[0]['item'] == item
    assert get_response[0]['id'] == id_child2lvl
    assert get_response[0]['path'] == path_child2lvl
    assert get_response[0]['inner_order'] == order_sec_child2lvl
    assert get_response[0]['attributes'] == '{}'
    assert get_response[0]['level_node'] == 2
    all_children = []
    for node in response_get_descendants[0]:
        if node['path'][0:-10] == path_child2lvl and node['level_node'] == 3:
            all_children.append(node)
    for s in all_children:
        assert s['inner_order'][:-10] == order_sec_child2lvl
    assert "'Content-Type': 'application/json'" in str(res_headers)
    # _, changed_node_out, _ = org.get_node(node_id=id_child2lvl)
    # print(changed_node_out)
    # _, changed_node_in, _ = org.get_node(node_id=id_sec_child2lvl)
    # print(changed_node_in)


# Базовый тест на изменение родителя узлов 2-4 уровней (в т.ч. узла без дочек, перемещение к родителю без дочек)
# OS-API-Up-1, OS-API-Up-3, OS-API-Up-5
@pytest.mark.order(15)
def test_change_parent_positive():
    # _, changing_node_out, _ = org.get_node(node_id=id_child2lvl)
    # print(changing_node_out)
    # _, changing_node_in, _ = org.get_node(node_id=id_root2)
    # print(changing_node_in)
    status_get_descendants, response_get_descendants, _ = org.get_descendants(node_id=id_root2)
    child_nodes_for_new_parent = []
    for node in response_get_descendants[0]:
        if status_get_descendants == 200:
            if node['path'][0:-10] == path_root2 and node['level_node'] == 2:
                child_nodes_for_new_parent.append(node)
    amount_child_nodes = len(child_nodes_for_new_parent)
    status, change_response, res_headers = org.change_parent(node_id_out=id_child2lvl, node_id_in=id_root2)
    # print(f"\nCode: {status}")
    print(f"Response: {change_response}")
    # print(f'Response headers: {res_headers}')
    assert status == 201
    _, get_response, _ = org.get_node(node_id=id_child2lvl)
    _, response_get_descendants_for_node, _ = org.get_descendants(node_id=id_child2lvl)

    org.change_parent(node_id_out=id_child2lvl, node_id_in=id_root1)
    org.change_order(node_id_out=id_sec_child2lvl, node_id_in=id_child2lvl)

    assert change_response[0] == f"Node {id_child2lvl} changed it's parent to node {id_root2}"
    assert get_response[0]['project_id'] == project_id
    assert get_response[0]['item_type'] == item_type
    assert get_response[0]['item'] == item
    assert get_response[0]['id'] == id_child2lvl
    assert get_response[0]['path'] == path_root2 + ('0' * (10 - len(str(id_child2lvl))) + str(id_child2lvl))
    assert get_response[0]['attributes'] == '{}'
    assert get_response[0]['level_node'] == 2
    assert get_response[0]['inner_order'] == \
           order_root2 + '0' * (10 - len(str(amount_child_nodes + 1))) + str(amount_child_nodes + 1)
    for node in response_get_descendants_for_node[0]:
        assert node['path'][:20] == path_root2 + ('0' * (10 - len(str(id_child2lvl))) + str(id_child2lvl))
        assert node['inner_order'][:20] == \
               order_root2 + '0' * (10 - len(str(amount_child_nodes + 1))) + str(amount_child_nodes + 1)
    assert "'Content-Type': 'application/json'" in str(res_headers)
    # _, changed_node_out, _ = org.get_node(node_id=id_child2lvl)
    # print(changed_node_out)
    # _, changed_node_back, _ = org.get_node(node_id=id_root1)
    # print(changed_node_back)
    # _, changed_node_in, _ = org.get_node(node_id=id_root2)
    # print(changed_node_in)


# Базовый тест на удаление/скрытие узлов всех уровней
@pytest.mark.order(16)
def test_delete_and_restore_node_positive():
    status, response, res_headers = org.change_hidden_attr(node_id=id_sec_child2lvl, hidden=True)
    # print(f"\nCode: {status}")
    # print(f"Response: {response}")
    # print(f'Response headers: {res_headers}')
    assert status == 200
    assert response[0] == "Node(s) deleted"
    assert "'Content-Type': 'application/json'" in str(res_headers)
    get_status, get_response, _ = org.get_node(node_id=id_sec_child2lvl)
    assert get_status == 404
    assert "{'error': 'does not exist object(s)'}" in str(get_response[0])
    status, response, res_headers = org.change_hidden_attr(node_id=id_sec_child2lvl, hidden=None)
    # print(f"\nCode: {status}")
    # print(f"Response: {response}")
    # print(f'Response headers: {res_headers}')
    assert status == 200
    assert response[0] == "Node(s) restored"
    get_status, get_response, _ = org.get_node(node_id=id_sec_child2lvl)
    assert get_status == 200
    assert get_response[0]['id'] == id_sec_child2lvl


# Тест на удаление узла с дочками (с полем affect_descendants)
@pytest.mark.order(17)
def test_delete_and_restore__node_with_affect_descendants_is_true():
    status, response, res_headers = org.change_hidden_attr(node_id=id_root1, hidden=True,
                                                           wrong_data={'project_id': project_id, 'item_type': item_type,
                                                                       'item': item, 'hidden': True,
                                                                       'affect_descendants': True})
    # print(f"\nCode: {status}")
    # print(f"Response: {response}")
    # print(f'Response headers: {res_headers}')
    assert status == 200
    assert response[0] == "Node(s) deleted"
    assert "'Content-Type': 'application/json'" in str(res_headers)
    get_status, get_response, _ = org.get_node(node_id=id_root1)
    # print(f"\nGet code: {get_status}")
    # print(f"Get response: {get_response}")
    assert get_status == 404
    assert "{'error': 'does not exist object(s)'}" in str(get_response[0])
    status_get_descendants, response_get_descendants, _ = org.get_descendants(node_id=id_root1)
    # print(f"\nGet code: {status_get_descendants}")
    # print(f"Get response: {response_get_descendants}")
    assert status_get_descendants == 404
    get_child_status, get_child_response, _ = org.get_node(node_id=id_child2lvl)
    # print(f"\nGet code: {get_child_status}")
    # print(f"Get response: {get_child_response}")
    assert get_child_status == 404
    assert "{'error': 'does not exist object(s)'}" in str(get_child_response[0])
    status, response, res_headers = org.change_hidden_attr(node_id=id_root1, hidden=None,
                                                           wrong_data={'project_id': project_id, 'item_type': item_type,
                                                                       'item': item, 'hidden': None,
                                                                       'affect_descendants': True})
    # print(f"\nCode: {status}")
    # print(f"Response: {response}")
    # print(f'Response headers: {res_headers}')
    assert status == 200
    assert response[0] == "Node(s) restored"
    get_status, get_response, _ = org.get_node(node_id=id_root1)
    # print(f"\nGet code: {get_status}")
    # print(f"Get response: {get_response}")
    assert get_status == 200
    assert get_response[0]["id"] == id_root1
    status_get_descendants, response_get_descendants, _ = org.get_descendants(node_id=id_root1)
    # print(f"\nGet code: {status_get_descendants}")
    # print(f"Get response: {response_get_descendants}")
    assert status_get_descendants == 200
    assert len(response_get_descendants[0]) != 0
    get_child_status, get_child_response, _ = org.get_node(node_id=id_child2lvl)
    # print(f"\nGet code: {get_child_status}")
    # print(f"Get response: {get_child_response}")
    assert get_child_status == 200
    assert get_child_response[0]["id"] == id_child2lvl


# Тест на удаление узла без дочек (с полем affect_descendants)
@pytest.mark.order(18)
def test_delete_node_with_affect_descendants_is_false():
    status, response, res_headers = org.change_hidden_attr(node_id=id_root1, hidden=True,
                                                           wrong_data={'project_id': project_id, 'item_type': item_type,
                                                                       'item': item, 'hidden': True,
                                                                       'affect_descendants': False})
    # print(f"\nCode: {status}")
    # print(f"Response: {response}")
    # print(f'Response headers: {res_headers}')
    assert status == 200
    assert response[0] == "Node(s) deleted"
    assert "'Content-Type': 'application/json'" in str(res_headers)
    get_status, get_response, _ = org.get_node(node_id=id_root1)
    # print(f"\nGet code: {get_status}")
    # print(f"Get response: {get_response}")
    assert get_status == 404
    assert "{'error': 'does not exist object(s)'}" in str(get_response[0])
    status_get_descendants, response_get_descendants, _ = org.get_descendants(node_id=id_root1)
    # print(f"\nGet code: {status_get_descendants}")
    # print(f"Get response: {response_get_descendants}")
    assert status_get_descendants == 404
    get_child_status, get_child_response, _ = org.get_node(node_id=id_child2lvl)
    # print(f"\nGet code: {get_child_status}")
    # print(f"Get response: {get_child_response}")
    assert get_child_status == 200
    assert get_child_response[0]["id"] == id_child2lvl
    org.change_hidden_attr(node_id=id_root1, hidden=None, wrong_data={'project_id': project_id, 'item_type': item_type,
                                                                      'item': item, 'hidden': None,
                                                                      'affect_descendants': False})


# Тест на восстановление узла без дочек (с полем affect_descendants)
@pytest.mark.order(18)
def test_restore_node_with_affect_descendants_is_false():
    org.change_hidden_attr(node_id=id_root1, hidden=True, wrong_data={'project_id': project_id, 'item_type': item_type,
                                                                      'item': item, 'hidden': True,
                                                                      'affect_descendants': False})
    org.change_hidden_attr(node_id=id_child2lvl, hidden=True, wrong_data={'project_id': project_id, 'item_type': item_type,
                                                                          'item': item, 'hidden': True,
                                                                          'affect_descendants': False})
    status, response, res_headers = org.change_hidden_attr(node_id=id_root1, hidden=None,
                                                           wrong_data={'project_id': project_id, 'item_type': item_type,
                                                                       'item': item, 'hidden': None,
                                                                       'affect_descendants': False})
    # print(f"\nCode: {status}")
    # print(f"Response: {response}")
    # print(f'Response headers: {res_headers}')
    assert status == 200
    assert response[0] == "Node(s) restored"
    assert "'Content-Type': 'application/json'" in str(res_headers)
    get_status, get_response, _ = org.get_node(node_id=id_root1)
    # print(f"\nGet code: {get_status}")
    # print(f"Get response: {get_response}")
    assert get_status == 200
    assert get_response[0]["id"] == id_root1
    status_get_descendants, response_get_descendants, _ = org.get_descendants(node_id=id_root1)
    # print(f"\nGet code: {status_get_descendants}")
    # print(f"Get response: {response_get_descendants}")
    assert status_get_descendants == 200
    assert str(f"'id': {id_child2lvl}") not in str(response_get_descendants[0])
    get_child_status, get_child_response, _ = org.get_node(node_id=id_child2lvl)
    # print(f"\nGet code: {get_child_status}")
    # print(f"Get response: {get_child_response}")
    assert get_child_status == 404
    assert "{'error': 'does not exist object(s)'}" in str(get_child_response[0])
    org.change_hidden_attr(node_id=id_child2lvl, hidden=True, wrong_data={'project_id': project_id, 'item_type': item_type,
                                                                          'item': item, 'hidden': None,
                                                                          'affect_descendants': False})


# Функция для удаления тестовых узлов после тестов
@pytest.mark.order(20)
def test_delete_all_nodes():
    get_status, get_response, _ = org.get_tree()
    # print(get_response[0])
    # id_node = get_response[0][-1]["id"]
    # print(id_node)
    for n in get_response[0]:
        # print(n["id"])
        if n["id"] > 1:
            status, response, _ = org.change_hidden_attr(node_id=n["id"], hidden=True, wrong_data={
                'project_id': project_id,
                'item_type': item_type,
                'item': item,
                'hidden': True,
        'affect_descendants': None
                })
    after_get_status, after_get_response, _ = org.get_tree()
    # print(after_get_response)
    assert after_get_response[0] == []
