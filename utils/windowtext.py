AUTHOR = 'Московский Авиационный Институт\n' \
         'Институт №8\n' \
         'Кафедра 813 «Компьютерная математика»\n' \
         'Группа М8О-311Б-19\n' \
         '\n' \
         'Тришин Дмитрий\n' \
         'Мамченков Дмитрий\n' \
         'Нодия Гиорги\n' \
         'Терешков Алексей\n' \
         'Солдатов Вячеслав\n' \
         'Ложкина Ольга\n' \
         'Сорокин Никита\n' \
         'Евкарпиев Михаил\n' \
         'Буреева Полина'

INSTRUCTION = 'Graph Visualizer - программа для визуализации и работы с графами, ' \
              'разработанная на языке Python.\n\n' \
              '1. Возможности программы:\n' \
              '    1. Загрузка матрицы из файла .csv' \
              '(матрица смежности, матрица инцидентности, файл конфигурации);\n' \
              '    2. Сохранение графа в файл .csv' \
              '(в виде матрицы смежности, матрицы инцидентности, файла конфигурации или изображения);\n' \
              '    3. Создание и редактирование графа с помощью мыши и кнопок Undo/Redo;\n' \
              '    4. Построение матрицы смежности графа в реальном времени;\n' \
              '    5. Применение алгоритмов к графу (п. Задачи теории графов);\n' \
              '    6. Выбор темы (п. Настройки -> Сменить тему);\n' \
              '\n' \
              '2. Загрузка графа\n' \
              '    Граф можно загрузить из файла формата .csv. Это может быть матрица смежности, ' \
              'матрица инцидентности и файл конфигурации.\n' \
              '    Файл конфигурации может иметь комментарии, начинающиеся со знака %.\n' \
              '\n' \
              '    Матрица смежности и инцидентности в файле формата .csv - это прямоугольная ' \
              'числовая таблица размера NxM, \n' \
              '    где N - число строк, а M - число столбцов. Элементы матрицы смежности и инцидентности ' \
              'разделены запятой.\n' \
              '\n' \
              '    Файл конфигурации содержит в себе информацию о вершинах и ребрах, которые соединяют ' \
              'эти вершины. Информация о вершинах \n' \
              '    задается с помощью конструкции Vertex{v(x, y)}, где v — имя или номер вершины,' \
              'x и y — координаты в пикселях.' \
              ' Список ребер задается \n' \
              '    с помощью конструкции Edges{i(a, k, l), . . .}, где i — номер ребра, a — вес ребра,' \
              'k и l — номера или имена вершин.\n' \
              '    Пример входных данных находится в папке examples.\n' \
              '\n' \
              '3. Сохранения графа\n'\
              '    Граф можно сохранить в файл формата .csv в виде матрицы смежности, матрицы инцидентности ' \
              'или файла конфигурации, а также \n' \
              '    в виде изображения любого формата (например, .png, .jpg). Файл конфигурации может иметь ' \
              'комментарии, начинающиеся со знака %.\n' \
              '\n' \
              '4. Рисование графа\n' \
              '    Рисование графа происходит с помощью выбора действия в контекстном меню и мыши. ' \
              'Для создания и удаления вершины нажмите \n' \
              '    правой кнопкой мыши на вершину и выберите необходимое действие в контекстном меню. ' \
              'Для включения отображения направления, \n' \
              '    установки веса и удаления ребра нажмите правой кнопкой мыши в любой точке экрана, после ' \
              'чего выберите необходимое действие.\n' \
              '    Для создания петли у вершины воспользуйтесь контекстным меню. Для создания ребра между двумя ' \
              'вершинами зажмите колесо \n' \
              '    мыши на первой вершине, затем, не отпуская колесо мыши, переместите мышь на вторую вершину, ' \
              'после чего отпустите кнопку.\n'
