admin-start-text = Добро пожаловать в панель администратора!
user-start-text = Привет! Отправь мне название фильма и я постараюсь найти его для тебя!
admin-button-back = ⬅️ Назад ⬅️
admin-button-yes = Да
admin-button-no = Нет
admin-button-next = Дальше
admin-button-cancel = Отмена
admin-button-close = Закрыть
admin-button-skip = Пропустить

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

# Messages
admin-button-send-message = Рассылка
admin-button-send-again = Отправить заного
admin-button-send-preview = Посмотреть сообщение
admin-button-send = Отправить пост
admin-message-media-request-text = Отправьте фото/видео, которые будут прикреплены к сообщению
admin-message-media-preview-text = Эти медиа будут прикреплены к сообщению (все сразу, без кнопок)
admin-message-request-text = Отправьте сообщение, которое хотите отправить пользователям
admin-message-preview-text = {$text}
admin-message-edit-media = Изменить медиа
admin-message-edit-text = Изменить текст
admin-button-cancel-edit = Отменить редактирование
admin-messages-sent = Пост был успешно отправлен!

close-button-text = Закрыть
user-start-text = Чтобы найти фильм просто отправьте мне его название!
yesno-button-text-yes = Да
yesno-button-text-no = Нет
cancel-button-text = Отмена
search-wait-text = Подожди пожалуйста, я ищу фильм
search-not-found-text = Я не нашел этот фильм
search-button-text = {$title} ({$year}) ⭐️{$rating}
search-message-text = Вот список доступных фильмов по запросу "{$request}"
search-not-found-text = Похоже, что по вашему запросу ничего не найдено
film-message-text =
    <a href="{$share_url}">🎬 {$title}</a> ({$year}) ⭐️{$rating}
    🎭 <b>Жанры:</b> <i>{$genres}</i>

    📰 <b>Описание:</b> <i>{$description}</i>
film-share-text = 📣 Поделись фильмом!
film-share-url = https://t.me/share/url?url={$share_url}&text={$title}
serial-season-url-button-text = Сезон {$number}
film-url-button-text = Смотреть онлайн [{$title}]
film-not-found-text = Похоже, что этого фильма больше нет
error-handler-text = Упс! Что-то пошло не так

user-yes-message = ДА 🥰🥰🥰☺️☺️☺️👍👍👍🦔
user-no-message = НЕТ 😡😡😡🤢🤢🤢👎👎👎🦧
user-percent-message = 🦭🦔🦒 {$percent}% 🦫🦖🪵

user-reaction-positive = Спс😭😭😭😭😭 стараюсь 🙏🙏🙏
