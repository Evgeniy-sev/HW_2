# HW_2

Scrapy with SQLAlchemy ORM <p>
Pycharm 2021.3.3  Python 3.8<p>
Корневой каталог: notebooks первого уровня.<p>
Модель описана в файле models.py<p>
Запуск проекта:
  - scrapy crawl scrapNotik
  - scrapy crawl scrapKNS
Приложена тестовая база sqlite test_notebooks.db, таблица с данными, полученными при проверке работоспособности.<p>
test_notebooks.db можно удалять, при запуске приложения создается пустая БД. Если не удалять, то записи добавятся к существующим.<p>
Данные о ноутбуках собираются с двух сайтов: https://www.notik.ru и https://www.kns.ru<p>
