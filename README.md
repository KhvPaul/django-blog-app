# django-blog-app

Дополнительная ДЗ с тем же заданием для дополнительных баллов.

Для тех кто присутствовал на занятии:
ожидаю ссылку на репозиторий (если в команде - то общий) и ссылку на задеплоенный проект (если успели)

Тех задание:
Блог (опять).
Функционал:


Пользователь может зарегистрироваться + логин/логаут
Пользователь может создавать посты
Пользователь может публиковать посты или убирать их в заготовки
Анонимные пользователи могут публиковать комментарии
Комментарии модерируется перед публикацией (поле is_published + admin page)
Администратор получает уведомление на почту о новом посте или комментарии (в консоль)
Пользователь получает уведомление о новом комментарии под постом с сылкой на пост (консоль)
Есть страница с списком всех постов
Есть страница с списком постов пользователя
Есть страница поста
Есть страница профиля публичная
Есть профиль в котором можно изменять свои данные
Пагинация постов и комментариев
У поста есть заголовок, краткое описание, картинка(опционально ссылка или реальное изображение) и полное описание
У комментария есть юзернейм и текст
Фикстуры loremipsum
Админка с функционалом
Форма обратной связи с админом (в консоль)
Темплейты с стилизацией
Разные настройки для разработки и продакшена
Оптимизация запросов в базу
Кеширование *
Селера и парсинг постов из рсс ленты или сайта *
Pythonanywhere (без кеширования и бэкграунд задач) **

Для тех кто не присутствовал на занятии:
выполнить все пункты
пункты с * или с ** опциональны, но желательны - реализацию селери и кеширования можно выполнить в отдельно ветке
ожидаю ссылку на репозиторий и ссылку на задеплоенный проект
больше инструкций найдете тут - https://djangogirls.org/resources/
учтите что на Pythonanywhere - redis и celery не заработают.
