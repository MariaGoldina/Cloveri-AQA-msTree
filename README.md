Это репозиторий с автотестами для сервиса построения структур типа дерева Tree Microservice на стажировке Cloveri. Тесты запускать командой:

pytest test_ms_tree_smoke.py

Тесты предусмотрены для сервиса на продакшн сервере. При необходимости можно задавать переменные окружения, для тестового сервера, для этого нужно раскоммитить строки 1-6 в файле settings.py.