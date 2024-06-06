import aiogram.utils.markdown as fmt

COMMANDS ={
    "START": "start",
    "HELP": "help",
    "GET": "get",
    "CREATE_ACCOUNT": "create_account",
    "DELETE_ACCOUNT": "delete_account",
    "SET_QUERY": "set_query",
    "DELETE_QUERY": "delete_query",
    "RESET_QUERIES": "reset_query",
    "RESET": "reset", 
}

COMMANDS_DESCRIPTIONS = {
    "START": "Начало работы",
    "HELP": "Помощь",
    "GET": "Получить текущие аккаунт",
    "CREATE_ACCOUNT": "Создать аккаунт",
    "DELETE_ACCOUNT": "Удалить аккааунт",
    "SET_QUERY": "Установить запрос",
    "DELETE_QUERY": "Удалить запрос",
    "RESET_QUERIES": "Сбросить все запросы",
    "RESET": "Сбросить КЭШ", 
}

if set(COMMANDS.keys()) != set(COMMANDS_DESCRIPTIONS.keys()):
    raise RuntimeError("The list of COMMANDS_DESCRIPTIONS must match the COMMANDS set")


MESSAGE = {}

MESSAGE["HELP"] = "\n".join(
    f"{i+1}. { COMMANDS_DESCRIPTIONS[key] }: /{command}"
    for i, (key, command) in enumerate(COMMANDS.items())
)

MESSAGE["INPUT_SECRET_TOKEN"] = f"""
{ fmt.hbold("Процесс регистрации") }
Введите токен доступа (securityToken)
Пример: {fmt.hcode("5119925560a2344eabc2d51662dc99ec2af173276c1ec635c50f015c8d9672a6d6e50298ade7f19fe5d0f2b2c0d42adbd2d48c19d8787852589e297afe006a27")}
"""

MESSAGE["NOT_REGISTERED"] = f"""
{ fmt.hbold("Вы не зарегестрированы") }
{ MESSAGE["HELP"] }
"""

MESSAGE["INPUT_ORG_UID"] = f"""
{ fmt.hbold("Процесс регистрации") }
Введите uid вашей организации
Пример: { fmt.hcode("1754404588698103809") }
"""

MESSAGE["INPUT_USER_UID"] = f"""
{ fmt.hbold("Процесс регистрации") }
Введите ваш uid
Пример: { fmt.hcode("1754404588698103808") }
"""

MESSAGE["USER_SUCCESS_REGISTERED"] = f"""
<b>Процесс регистрации успешно завершен 😎</b>
Установите запрос для рассылки: /{COMMANDS["SET_QUERY"]}
"""

MESSAGE["RESET_QUERY"] = f"""
Запрос успешно сброшен
"""

MESSAGE["SET_QUERY"] = f"""
<b>Напишите запрос</b>
Пример: <code>(Python OR Django) AND (C++ AND WebRTC)</code>
"""


MESSAGE["ACCOUNT_ALREADY_CREATED"] = f"""
Аккаунт уже зарегестрирован
"""


MESSAGE["ACCOUNT_DELETE"] = f"""
Аккаунт успешно удаленно
"""


MESSAGE["CANCEL"] = f"""
КЭШ очишен
"""


MESSAGE["NUMBER_QUESTION"] = """
<b>Осталось запросов 🤔: {}</b>""" + f"""
    /{COMMANDS["RESET_QUERIES"]} - удалить все
    /{COMMANDS["DELETE_QUERY"]} - удалить конкретный
"""

MESSAGE["INPUT_DELETE_QUERY"] = """
Выберете запрос, который бы вы хотели удалить
"""

MESSAGE["GET_ACCOUNT"] = """
<b>Telegram ID</b>: <code>{}</code>
<b>UID организации</b>: <code>{}</code>
<b>UID пользователя</b>: <code>{}</code>
<b>Секретный токен</b>: <code>{}</code>
<b>Запросы</b>: \n{}
"""


MESSAGE["INPUT_ERROR"] = """
<b>Простите, я вас не понял  😵‍💫</b>
"""

MESSAGE["SUCCESS_DELETE"] = """
Запрос <code>{}</code> успешно удален
"""


MESSAGE["QUERIES"] = """
<b>Актуальные запросы:</b> 
{}
<b>Создать новый запрос</b>""" + f""" (/{COMMANDS["SET_QUERY"]})"""
