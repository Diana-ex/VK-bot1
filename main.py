
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

# === Настройки ===
GROUP_TOKEN = 'vk1.a.oRBjcOGyGgr93acUfckI4elhb8v5cVsRrm_AY0mGXen9W4gA88jUWzqAyXX6jD9Ialq8yvsSZekc3GJpAiK3SaAmTeIw2DOIG-LOyj8Dzhi6ThFlYv1W4LGudWcQNwEwQH_HVS5aTRyhcAKDf7q5Q9EVfClJxmvxL3rSicq9AXLawnP48cxnzVwqElgHNVyz454ltCwFOgxSpf4CTwu--A'  # ← замени на свой токен из ВК

# === Авторизация ===
vk_session = vk_api.VkApi(token=GROUP_TOKEN)
vk = vk_session.get_api()

# Получение ID группы
group_id = vk.groups.getById(
    group_ids='226105127')[0]['id']  # Замени на ID своей группы

print(f"Идентификатор группы: {group_id}")

# Создание Long Poll
longpoll = VkBotLongPoll(vk_session, group_id)

print("Бот запущен!")

# === База знаний по переработке ===
faq = {
    "привет":
    "Привет! Я бот по переработке вторсырья. Выбери интересующую тему:",
    "что такое переработка?":
    "Переработка — это процесс повторной обработки уже использованных материалов,"
    " чтобы сделать из них новые изделия. Так мы экономим природные ресурсы и уменьшаем количество отходов.",
    "виды вторсырья":
    "Основные виды вторсырья:\n"
    "- Бумага и картон\n"
    "- Пластик\n"
    "- Стекло\n"
    "- Металл\n"
    "- Электроника\n"
    "- Текстиль\n"
    "- Органические отходы",
    "как сортировать мусор?":
    "Сортируй мусор так:\n"
    "🟦 Синий — бумага\n"
    "🟩 Зелёный — стекло\n"
    "🟨 Жёлтый — пластик\n"
    "🟥 Красный — опасные отходы\n"
    "⚪ Серый — смешанные отходы (не подлежит переработке)",
    "польза переработки":
    "Польза переработки:\n"
    "- Уменьшение количества мусора на свалках\n"
    "- Снижение загрязнения воздуха и воды\n"
    "- Экономия энергии и природных ресурсов\n"
    "- Защита животных и среды обитания",
    "куда сдавать мусор?":
    "Можно сдать вторсырьё:\n"
    "- В специальные контейнеры для раздельного сбора\n"
    "- В пункты приёма вторсырья\n"
    "- В экопункты или центры переработки\n"
    "- Через программы по сбору старой техники или одежды"
}


# === Функция создания клавиатуры ===
def create_keyboard():
    keyboard = VkKeyboard(
        one_time=False)  # one_time=False — клавиатура остаётся после нажатия

    keyboard.add_button('Что такое переработка?',
                        color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()  # Переход на новую строку

    keyboard.add_button('Виды вторсырья', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('Как сортировать мусор?',
                        color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()

    keyboard.add_button('Польза переработки', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('Куда сдавать мусор?', color=VkKeyboardColor.SECONDARY)

    return keyboard.get_keyboard()


# === Обработка событий ===
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        user_id = event.obj.message['peer_id']
        message_text = event.obj.message['text'].lower().strip()

        print(f"Получено сообщение от {user_id}: {message_text}")

        answer = faq.get(message_text, None)

        if message_text == 'привет':
            vk.messages.send(peer_id=user_id,
                             message=faq['привет'],
                             keyboard=create_keyboard(),
                             random_id=0)
        elif answer:
            vk.messages.send(peer_id=user_id,
                             message=answer,
                             keyboard=create_keyboard(),
                             random_id=0)
        else:
            vk.messages.send(peer_id=user_id,
                             message="Не понял. Нажми на одну из кнопок.",
                             keyboard=create_keyboard(),
                             random_id=0)
