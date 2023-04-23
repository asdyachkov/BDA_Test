#BDA_Test
<h4>Репозитория создан Дьячковым С.А.</h4>

<h3>Функционал проекта</h3>
<ul>
    <li>
        Определяет погоду по указанному городу (API)
    </li>
    <li>
        Конвертирует валюты (API)
    </li>
    <li>
        Отправка котиков (API)
    </li>
    <li>
        Создание опросов и отправка в указанный чат (бот должен находиться в этом чате и обладать необходимыми правами)
    </li>
</ul>

<h3>Особенности проекта</h3>
<ul>
    <li>
        Прописаны файлы dockerfile и docker-compose
    </li>
    <li>
        Контейнер выложен на dockerhub: https://hub.docker.com/repository/docker/asdyachkov/bda_test
    </li>
    <li>
        Для запуска бота можно как запустить файл bot.py (установив requirements), так и используя docker / docker-compose
    </li>
    <li>
        Проект полностью асинхронный. От aiogram до работы с api через aiohttp
    </li>
    <li>
        Используются только inline кнопки или текстовый ввод от пользователя
    </li>
    <li>
        Бот устойчив к ошибкам ввода от пользователей
    </li>
    <li>
        В коде имеются комментарии по работе каждой функции
    </li>
</ul>

<h3>Ссылка на бота: @BDATest_bot</h3>
