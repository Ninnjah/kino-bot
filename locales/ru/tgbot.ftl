admin-start-text = Добро пожаловать в панель администратора!
user-start-text = Добро пожаловать!
admin-button-back = ⬅️ Назад ⬅️
admin-button-yes = Да
admin-button-no = Нет
admin-button-cancel = Отмена
admin-button-close = Закрыть

# User list
admin-users-list = Список пользователей:
admin-button-list-users = Пользователи
admin-error-users-notfound = Ни одного пользователя не было найдено
admin-users-export = Экспортировать 📦

# Admin list
admin-admins-list = Список администраторов:
admin-error-admins-notfound = Ни одного администратора еще не было добавлено
admin-button-list-admins = Администраторы
admin-button-add-admin = Добавить 🆕
admin-button-del-admin = Удалить 🗑
admin-show-admin = 
    Айди администратора: <a href='tg://user?id={ $admin_id }'><b>{ $admin_id }</b></a>

    Назначен: <code>{ $created_on }</code>
    Последнее обновление: <code>{ $updated_on }</code>
admin-show-sudo = Права суперпользователя: { $sudo ->
        [0] ❌
        [1] ✅
        *[other] ❓
    }
admin-delete-text = 
    Вы уверены что хотите удалить пользователя <a href='tg://user?id={ $admin_id }'><b>{ $admin_id }</b></a> из списка администраторов?

    Права суперпользователя: { $sudo ->
        [0] ❌
        [1] ✅
        *[other] ❓
    }
    Назначен: <code>{ $created_on }</code>
    Последнее обновление: <code>{ $updated_on }</code>
admin-add-admin-request = Отправьте айди или выберите из списка пользователя, которого хотите назначить администратором
admin-error-user-id-is-invalid =
    Айди пользователя неверен!
    Отправьте айди или выберите из списка пользователя, которого хотите назначить администратором. 
    Айди можно узнать, например у бота @my_id_bot
admin-error-is-not-user-id =
    Пересланное сообщение было отправлено не пользователем!
    Отправьте айди или выберите из списка пользователя, которого хотите назначить администратором. 
    Айди можно узнать, например у бота @my_id_bot
admin-error-already-admin = Пользователь уже администратор
admin-add-admin-sudo-request = Назначить пользователя <a href='tg://user?id={ $admin_id }'><b>{ $admin_id }</b></a> суперпользователем?
admin-add-admin-confirm = Вы уверены что хотите добавить пользователя <a href='tg://user?id={ $admin_id }'><b>{ $admin_id }</b></a> в администраторы?

# Sources
admin-button-list-players = Источники
admin-players-list = Вот список доступных источников

close-button-text = Закрыть
user-start-text = Чтобы найти фильм просто отправьте мне его название!
yesno-button-text-yes = Да
yesno-button-text-no = Нет
cancel-button-text = Отмена
search-wait-text = Подожди пожалуйста, я ищу фильм
search-button-text = {$title} ({$year}) ⭐️{$rating}
search-message-text = Вот список доступных фильмов по запросу "{$request}"
search-not-found-text = Похоже, что по вашему запросу ничего не найдено
film-message-text =
    🎬 {$title} ({$year}) ⭐️{$rating}
    🎭 <b>Жанры:</b> <i>{$genres}</i>

    📰 <b>Описание:</b> <i>{$description}</i>

    <a href="https://t.me/share/url?url={$share_url}&text={$title}">📣 Поделись фильмом!</a>
serial-season-url-button-text = Сезон {$number}
film-url-button-text = Смотреть онлайн [{$title}]
film-not-found-text = Похоже, что этого фильма больше нет
error-handler-text = Упс! Что-то пошло не так