# Freelance crm

![](https://img.shields.io/static/v1?label=status&message=in%20development&color=informational)
![GitHub Workflow Status (with branch)](https://img.shields.io/github/actions/workflow/status/andrew281213/freelance-crm/pylint.yml?branch=main)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/andrew281213/freelance-crm/pytest.yml?label=tests)

Система для работы с заказами и клиентами на фрилансе.

## Основной функционал
***
### Клиенты

![Скрин страницы списка клиентов][clients-screen]
![Скрин страницы клиента][clients-screen-detailed]

Основная задача - хранение контактов для связи, истории заказов + предоставление
краткой сводки (кол-во выполненных заказов, заказов в работе, общая сумма заказов и т.д.)

**Основные данные о клиенте:**
- ФИО
- Ники(с разных бирж, чатов, мессенджеров)
- Ссылки на страницы (страницу биржи, профиля на сайте, профиля в мессенджере)
- Комментарий


**Возможности:**
- [ ] Создание, редактирование, удаление
- [ ] Добавление комментария (описать какой он плохой и требовательный
и что с ним лучше не работать)
- [ ] Поиск по части ника
- [ ] Поиск по части ссылки
- [ ] Поиск по части информации из заказа(ссылка на сайт, название заказа, 
часть описания и т.д.)
- [ ] Фильтр по дате создания клиента
- [ ] Фильтр по дате создания заказа
- [ ] Сортировка по дате создания клиента
- [ ] Сортировка по дате создания заказа
- [ ] Сортировка по сумме заказов

***
### Заказы

![Скрин страницы списка заказов][orders-screen]
![Скрин страницы заказа][orders-screen-detailed]

Основная задача - хранение входных данных, результатов работы над заказом,
вывод краткой сводки (стоимость, затраченное время и т.д.)

**Основные данные о заказе:**
- Основная информация о клиенте
- ТЗ
- Исходные файлы
- Архив с результатом работы
- Статус
- Дата создания
- Дата окончания
- Дата редактирования информации
- Дата завершения работы
- Комментарий (от меня)
- Стоимость работы
- Затраченное время (вводится вручную)
- История изменений

**Возможности:**
- [ ] Создание, изменение, удаление
- [ ] Прикрепление ТЗ и доп. файлов
- [ ] Прикрепление архива с результатом работы
- [ ] Изменение статуса
- [ ] Добавление комментария
- [ ] Возможность вернуть заказ в работу (доработка, улучшение)
- [ ] Сохранение предыдущих версий результатов работы
- [ ] Уведомление об истечении срока выполнения (тг, почта)
- [ ] Поиск по части названия
- [ ] Поиск по части описания
- [ ] Поиск по нику клиента
- [ ] Поиск по части ссылки на клиента
- [ ] Фильтр по дате создания заказа
- [ ] Сортировка по дате создания заказа
- [ ] Сортировка по сумме заказа
- [ ] Сортировка по статусу заказа
- [ ] По времени до дедлайна


***
### Парсеры

![Скрин страницы списка предложений с бирж][market-projects-screen]
![Скрин страницы парсеров][parsers-screen]

Основная задача - хранение входных данных, результатов работы над заказом,
вывод краткой сводки (стоимость, затраченное время и т.д.)

**Основные данные о заказах с бирж:**
- Название заказа
- Описание заказа
- Прикрепленные файлы
- Стоимость работы

**Возможности:**
- [ ] Запуск, остановка парсера
- [ ] Изменение списка игнорируемых слов
- [ ] Изменение расписания работы каждого парсера

## Разработка

***
### Структура БД

**Пользователи:**

![Таблица пользователей][sql-db-users]

**Клиенты:**

![Таблицы клиентов][sql-db-clients]

**Заказы:**

![Таблицы заказов][sql-db-orders]


**Парсеры:**

![Таблицы настроек и данных парсеров][sql-db-market-projects]


## TODO list
- [ ] Продумать структуру бд
- [ ] Добавить скрины структуры в readme
- [ ] Добавить страницу входа
- [ ] Добавить страницу вывода списка клиентов
- [ ] Добавить страницу создания клиента
- [ ] Добавить страницу редактирования клиента
- [ ] Добавить метод удаления клиента
- [ ] Добавить страницу вывода списка заказов
- [ ] Добавить страницу создания заказа
- [ ] Добавить страницу изменения заказа
- [ ] Добавить метод удаления заказа
- [ ] Добавить возможность прикрепления файлов к заказу
- [ ] Добавить возможность прикрепления архива результата работы
- [ ] Добавить возможность возвращения заказа в работу
- [ ] Добавить возможность сохранения предыдущих результатов работы
- [ ] Добавить возможность изменения статуса
- [ ] Добавить сортировки по заказам
- [ ] Добавить фильтрации по заказам
- [ ] Добавить сортировки по клиентам
- [ ] Добавить фильтрации по клиентам
- [ ] Добавить поиск по клиентам
- [ ] Добавить поиск по заказам
- [ ] Добавить страницу настроек для уведомлений
- [ ] Добавить возможность уведомлений об истечении заказа
- [ ] **Добавить модуль статистики по заказам и клиентам**
- [ ] **Добавить модуль TODO**


[comment]: <> (links)
[clients-screen]: <> "Скрин страницы списка клиентов"
[clients-screen-detailed]: <> "Скрин страницы клиента"
[orders-screen]: <> "Скрин страницы списка заказов"
[orders-screen-detailed]: <> "Скрин страницы заказа"
[market-projects-screen]: <> "Скрин страницы списка предложений с биржи"
[parsers-screen]: <> "Скрин страницы парсеров"
[sql-db-users]: readme/users-table.png "Таблица пользователей"
[sql-db-clients]: readme/clients-table.png "Таблицы пользователей"
[sql-db-orders]: <> "Таблицы заказов"
[sql-db-market-projects]: <> "Таблицы настроек и данных парсеров"
