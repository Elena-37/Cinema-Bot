### **Что сделали, чего добились**

1) Зарегистрировали бота - уже как бы ни хухры мухры

2) Сделали радостные приветствия юзерам - просим потом обратить внимание на смайлики, которые будут вылезать. Так же по команде ${\color{cyan}/start}$ выдается функционал бота. В случае опечаток в команде (ну мало ли) бот честно признаёт, что не умеет этого делать и предлагает начать с ним работу с помощью правильной команды

4) Были добавлены инлайн-кнопочки, которые позволяют выбрать 3 варианта развития событий: "Найти по названию", "Топ-10 по стране", "Топ-10 по жанру"

5) После выбора "Топ-10 по стране" или "Топ-10 по жанру" пока вылезают душевные обещания их доделать

6) После выбора "Найти по названию" вызывается функция, которая достаёт фильмы и сериалы из API кинопоиска (а именно их название, описание, рейтинг и постер), и выдаётся найденное

7) Более того, добавлены команды:
   
   $\longrightarrow$ ${\color{cyan}/link}$ - будет выдавать ссылки
   
   $\longrightarrow$ ${\color{cyan}/another}$ - если нашёлся не тот фильм, предлагается дать ещё попытку боту
   
   $\longrightarrow$ ${\color{cyan}/restart}$ - если пользователь резко передумал и решил использовать другую функцию бота


Что, кто сделал:
 - осознание работы API (Лена, Рената, Катя)
 - оформление приветствия бота + описание функционала(Рената, Лена)
 - функция, по названию фильма возвращающая информацию о нем сообщением: постер, название, описание, рейтинги (все)
 - обеспечение красоты и душевности сообщения бота с инфой по фильму(Рената)
 - создание инлайн кнопочек (Лена)
 - приведение кнопочек в чувства и последующая корректная обработка запросов пользователя (Рената)
 - структура кода, распределение функций по файлам (Рената)
 - душевность гитхаба (Хелена)

### **Что ещё не сделали, но обязательно добьёмся**

Осталось непосредственно доставать ссылки фильмов и сериалов и топы по жанрам и странам. Топы будут без ссылок, будут выдаваться фильмы так же, как в пункте 6. 
Вопрос с запоминаниями серий пока открыт, но мы что-нибудь придумаем

**Пы.сы.** мы помним про логгирование и покрытие тестами. все будет, но когда добъем парсинг.
**Пы.сы. 2** если Вы хотите поддержать наш проект, то вот телефон для донатов 89258281249, а если помочь пережить бессонные ночи, то мы бы были рады ирискам


