#!/usr/bin/env python3
"""
Бот-анкета для кинолога/психолога @ira.psycho
Установка: pip install pyTelegramBotAPI
Запуск: python bot.py
"""

import telebot
from telebot import types

# ═══════════════════════════════════════════════
#  ВСТАВЬТЕ СЮДА СВОИ ДАННЫЕ
BOT_TOKEN = "8662279654:AAGArQhxpyQTZGUJr3VL7trZFCvqWEEQvZ4"
ADMIN_ID   = 141894747
# ═══════════════════════════════════════════════

bot = telebot.TeleBot(BOT_TOKEN)

# Все вопросы анкеты по порядку
QUESTIONS = [
    {"text": "Ваше имя", "type": "text"},
    {"text": "Кличка собаки", "type": "text"},
    {"text": "Возраст собаки", "type": "text"},
    {"text": "Порода собаки (если метис — примерная порода или вес)", "type": "text"},
    {"text": "Как к вам попал питомец? В каком возрасте?", "type": "text"},
    {"text": "С какими проблемами поведения своей собаки вы столкнулись?", "type": "text"},
    {"text": "Как давно это началось и сколько продолжается?", "type": "text"},
    {"text": "Каких из них вы хотите решить в первую очередь?", "type": "text"},
    {"text": "Что вы уже предпринимали для решения этих проблем?", "type": "text"},
    {"text": "Какой результат вы ждёте от наших занятий?", "type": "text"},
    {"text": "Что хорошего есть в жизни с вашим питомцем? Как вы обычно проводите время вместе?", "type": "text"},
    {"text": "Кастрирована ли ваша собака?", "type": "choice", "options": ["Да", "Нет"]},
    {"text": "Привита ли ваша собака?", "type": "choice", "options": ["Да", "Нет"]},
    {"text": "Дата последней вакцинации (для собак с агрессией к людям)\n\nЕсли не актуально — напишите «—»", "type": "text"},
    {"text": "Как давно вы проходили полное ветеринарное обследование?",
     "type": "choice", "options": ["Менее полугода назад", "Полгода–год назад", "Более года"]},
    {"text": "Есть ли у вашего питомца хронические заболевания? Если да — какие?\n\nЕсли нет — напишите «Нет»", "type": "text"},
    {"text": "Есть ли у вашего питомца заболевания в острой фазе? Если да — какие?\n\nЕсли нет — напишите «Нет»", "type": "text"},
    {"text": "Был ли опыт посещения врачей поведенческой медицины или невролога? Если да — укажите имя врача.\n\nЕсли прислали выписку на этапе записи — напишите «Выписка отправлена». Если не было — «Нет»", "type": "text"},
    {"text": "Были ли назначены препараты? Если да — какие?\n\nЕсли прислали выписку — напишите «Выписка отправлена». Если нет — «Нет»", "type": "text"},
    {"text": "Сколько раз в день вы гуляете?",
     "type": "choice", "options": ["1–2 раза в день", "2–3 раза в день", "3–4 раза в день", "Другое"]},
    {"text": "Продолжительность и интенсивность ваших прогулок? (общение с другими собаками, активные игры и т.д.)", "type": "text"},
    {"text": "Какую амуницию вы используете в быту?", "type": "text"},
    {"text": "Был ли в прошлом опыт занятий с кинологом? Если был — расскажите об этом.\n\nЕсли не было — напишите «Нет»", "type": "text"},
    {"text": "Есть ли члены семьи, живущие в одном доме с собакой?\nЕсли да — кто? Какие у них отношения с собакой?", "type": "text"},
    {"text": "Есть ли другие животные, живущие в одном доме с собакой?\nЕсли да — какие? Какие у них отношения с собакой?", "type": "text"},
    {"text": "Любая дополнительная информация о вашей собаке, которую вы считаете важной.\n\nЕсли нечего добавить — напишите «—»", "type": "text"},
    {"text": "Подходящий вам формат занятий",
     "type": "choice", "options": ["Очное занятие", "Онлайн консультация", "Сопровождение"]},
    {"text": "Ближайшая к вам станция метро или адрес (для очных консультаций)\n\nЕсли онлайн — напишите «—»", "type": "text"},
    {"text": "Откуда вы узнали про меня?", "type": "text"},
    {"text": "Где вам удобнее получать обратную связь и итоги занятия?",
     "type": "choice", "options": ["WhatsApp", "Телеграм", "Другое"]},
    {"text": "Промокод (если есть)\n\nЕсли нет — напишите «—»", "type": "text"},
    {"text": "Ваш контактный телефон или ссылка на Telegram", "type": "text"},
]

# Хранилище состояний пользователей
user_state = {}  # {user_id: {"step": int, "answers": list}}


def get_keyboard(options):
    """Создаёт клавиатуру с вариантами ответа"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for option in options:
        markup.add(types.KeyboardButton(option))
    return markup


def remove_keyboard():
    return types.ReplyKeyboardRemove()


def send_question(chat_id, step):
    """Отправляет вопрос номер step"""
    q = QUESTIONS[step]
    total = len(QUESTIONS)
    progress = f"[{step + 1}/{total}]\n\n"
    text = progress + "📋 " + q["text"]

    if q["type"] == "choice":
        bot.send_message(chat_id, text, reply_markup=get_keyboard(q["options"]))
    else:
        bot.send_message(chat_id, text, reply_markup=remove_keyboard())


def format_summary(answers, user):
    """Форматирует итоговое сообщение с анкетой"""
    name = user.first_name or ""
    username = f"@{user.username}" if user.username else f"ID: {user.id}"

    lines = [
        "🐕 НОВАЯ АНКЕТА ВЛАДЕЛЬЦА",
        f"От: {name} ({username})",
        "─" * 35,
    ]
    for i, q in enumerate(QUESTIONS):
        answer = answers[i] if i < len(answers) else "—"
        # Берём только первую строку заголовка вопроса (без пояснений)
        q_title = q["text"].split("\n")[0]
        lines.append(f"\n❓ {q_title}\n✏️ {answer}")

    lines.append("\n" + "─" * 35)
    lines.append("✅ Анкета заполнена полностью")
    return "\n".join(lines)


@bot.message_handler(commands=["start"])
def handle_start(message):
    user_id = message.from_user.id
    user_state[user_id] = {"step": 0, "answers": []}

    bot.send_message(
        message.chat.id,
        "Привет! 👋\n\n"
        "Я помогу заполнить анкету перед консультацией.\n"
        "Это займёт около 5–10 минут.\n\n"
        "Отвечайте своими словами — здесь нет правильных или неправильных ответов. "
        "Чем подробнее — тем лучше я смогу подготовиться к нашей работе.\n\n"
        "Начнём! 🐾",
        reply_markup=remove_keyboard()
    )

    import time
    time.sleep(1)
    send_question(message.chat.id, 0)


@bot.message_handler(commands=["restart"])
def handle_restart(message):
    handle_start(message)


@bot.message_handler(func=lambda m: True)
def handle_answer(message):
    user_id = message.from_user.id

    if user_id not in user_state:
        bot.send_message(
            message.chat.id,
            "Напишите /start чтобы начать заполнение анкеты."
        )
        return

    state = user_state[user_id]
    step = state["step"]
    q = QUESTIONS[step]

    # Валидация для вопросов с вариантами
    if q["type"] == "choice":
        if message.text not in q["options"]:
            bot.send_message(
                message.chat.id,
                "Пожалуйста, выберите один из вариантов кнопкой ниже 👇",
                reply_markup=get_keyboard(q["options"])
            )
            return

    # Сохраняем ответ
    state["answers"].append(message.text)
    state["step"] += 1

    # Проверяем — это был последний вопрос?
    if state["step"] >= len(QUESTIONS):
        # Анкета завершена
        bot.send_message(
            message.chat.id,
            "Спасибо! 🙏 Анкета заполнена.\n\n"
            "Я получу ваши ответы и свяжусь с вами для подтверждения записи.",
            reply_markup=remove_keyboard()
        )

        # Отправляем анкету администратору
        summary = format_summary(state["answers"], message.from_user)
        try:
            # Разбиваем на части если длинное (лимит Telegram — 4096 символов)
            if len(summary) <= 4096:
                bot.send_message(ADMIN_ID, summary)
            else:
                parts = [summary[i:i+4000] for i in range(0, len(summary), 4000)]
                for part in parts:
                    bot.send_message(ADMIN_ID, part)
        except Exception as e:
            print(f"Ошибка отправки администратору: {e}")

        # Очищаем состояние
        del user_state[user_id]

    else:
        # Следующий вопрос
        send_question(message.chat.id, state["step"])


if __name__ == "__main__":
    print("Бот запущен. Нажмите Ctrl+C для остановки.")
    bot.infinity_polling()
