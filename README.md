Сервис управления рассылками

* Реализована отправка рассылок как из консоли, так и в автоматическом режиме без участия пользователя
* Созданы страницы для создания/редактирования/удаления/изменения и просмотра рассылок
* Такие же страницы созданы для сообщений и клиентов
* Добавлен функционал регистрации в сервисе по почте и паролю
* Созданы группы менеджера и контент менеджера
* 3 случайных поста из блога отображаются на главной странице - странице отображения списка рассылок
* Только пользователь с правами контент-менеджера может редактировать, создавать и удалять посты
* На главную страницу выведено количество рассылок, активных рассылок, уникальных клиентов
* Произведено кеширование списка постов и страницы с детальным просмотром поста


Правила использования:
* Для ручной рассылки необходимо прописать в консоль 'python3 manage.py start_program'
* Чтобы программа работала корректно без вмешательства пользователя, раскомментируйте код в файле app.py приложения newsletter и запустите сервер

