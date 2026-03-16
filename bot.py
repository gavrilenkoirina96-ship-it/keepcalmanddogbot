#!/usr/bin/env python3
"""
Бот-анкета для кинолога/психолога @ira.psycho — версия 2.0
Установка: pip install pyTelegramBotAPI
Запуск: python bot.py
"""

import telebot
from telebot import types
import time
import os

# ═══════════════════════════════════════════════
#  ВСТАВЬТЕ СЮДА СВОИ ДАННЫЕ
BOT_TOKEN = "8662279654:AAGArQhxpyQTZGUJr3VL7trZFCvqWEEQvZ4"
ADMIN_ID   = 141894747
# ═══════════════════════════════════════════════

bot = telebot.TeleBot(BOT_TOKEN)

MAX_TEXT_LENGTH = 500


def progress_bar(current, total, size=10):
    """🟣🟣🟣⚪️⚪️⚪️  3 из 10"""
    filled = round(current / total * size)
    empty  = size - filled
    return "🟣" * filled + "⚪️" * empty + f"  {current} из {total}"


QUESTIONS = [
    {"id": "name",        "text": "Ваше имя",                                                           "type": "text"},
    {"id": "dog_name",    "text": "Кличка собаки",                                                      "type": "text"},
    {"id": "dog_age",     "text": "Возраст собаки",                                                     "type": "digits"},
    {"id": "dog_breed",   "text": "Порода собаки (если метис — примерная порода или вес)",              "type": "text"},
    {"id": "how_got",     "text": "Как к вам попал питомец? В каком возрасте?",                         "type": "text"},
    {"id": "problems",    "text": "С какими проблемами поведения своей собаки вы столкнулись?",         "type": "text"},
    {"id": "since_when",  "text": "Как давно это началось и сколько продолжается?",                     "type": "text"},
    {"id": "priority",    "text": "Каких из них вы хотите решить в первую очередь?",                    "type": "text"},
    {"id": "tried",       "text": "Что вы уже предпринимали для решения этих проблем?",                 "type": "text"},
    {"id": "goal",        "text": "Какой результат вы ждёте от наших занятий?",                         "type": "text"},
    {"id": "good",        "text": "Что хорошего есть в жизни с вашим питомцем? Как вы обычно проводите время вместе?", "type": "text"},

    {"id": "castrated",   "text": "Кастрирована ли ваша собака?",
     "type": "choice", "options": ["Да", "Нет"]},

    {"id": "vaccinated",  "text": "Привита ли ваша собака?",
     "type": "choice", "options": ["Да", "Нет"]},

    {"id": "vacc_date",   "text": "Дата последней вакцинации (для собак с агрессией к людям)",
     "type": "text", "skip": True},

    {"id": "vet_check",   "text": "Как давно вы проходили полное ветеринарное обследование?",
     "type": "choice", "options": ["Менее полугода назад", "Полгода–год назад", "Более года"]},

    {"id": "chronic_yn",  "text": "Есть ли у вашего питомца хронические заболевания?",
     "type": "choice", "options": ["Да", "Нет"],
     "branch": {
         "Да": [{"id": "chronic_what", "text": "Какие хронические заболевания?", "type": "text"}]
     }},

    {"id": "acute_yn",    "text": "Есть ли у вашего питомца заболевания в острой фазе?",
     "type": "choice", "options": ["Да", "Нет"],
     "branch": {
         "Да": [{"id": "acute_what", "text": "Какие заболевания в острой фазе?", "type": "text"}]
     }},

    {"id": "beh_vet_yn",  "text": "Был ли опыт посещения врачей поведенческой медицины или невролога?",
     "type": "choice", "options": ["Да", "Нет"],
     "branch": {
         "Да": [
             {"id": "beh_vet_who",  "text": "Укажите имя врача",                                        "type": "text"},
             {"id": "beh_vet_diag", "text": "Поставленный диагноз",                                     "type": "text"},
             {"id": "beh_vet_meds", "text": "Назначенные препараты (если нет — напишите «Нет»)",        "type": "text"},
         ]
     }},

    {"id": "walks_count", "text": "Сколько раз в день вы гуляете?",
     "type": "choice", "options": ["1–2 раза в день", "2–3 раза в день", "3–4 раза в день", "Другое"]},

    {"id": "walks_desc",  "text": "Продолжительность и интенсивность ваших прогулок? (общение с другими собаками, активные игры и т.д.)", "type": "text"},
    {"id": "equipment",   "text": "Какую амуницию вы используете в быту?",                              "type": "text"},

    {"id": "trainer_yn",  "text": "Был ли в прошлом опыт занятий с кинологом?",
     "type": "choice", "options": ["Да", "Нет"],
     "branch": {
         "Да": [{"id": "trainer_desc", "text": "Расскажите об этом. Как работали, что понравилось, что нет?", "type": "text"}]
     }},

    {"id": "family_yn",   "text": "Есть ли члены семьи, живущие в одном доме с собакой?",
     "type": "choice", "options": ["Да", "Нет"],
     "branch": {
         "Да": [
             {"id": "family_who", "text": "Кто живёт с собакой? (перечислите)",                         "type": "text"},
             {"id": "family_rel", "text": "Какие у них отношения с собакой?",                           "type": "text"},
         ]
     }},

    {"id": "animals_yn",  "text": "Есть ли другие животные, живущие в одном доме с собакой?",
     "type": "choice", "options": ["Да", "Нет"],
     "branch": {
         "Да": [
             {"id": "animals_who", "text": "Какие животные живут с собакой?",                           "type": "text"},
             {"id": "animals_rel", "text": "Какие у них отношения с собакой?",                          "type": "text"},
         ]
     }},

    {"id": "extra",       "text": "Любая дополнительная информация о вашей собаке, которую вы считаете важной",
     "type": "text", "skip": True},

    {"id": "format",      "text": "Подходящий вам формат занятий",
     "type": "choice", "options": ["Очное занятие", "Онлайн консультация", "Сопровождение"], "skip": True},

    {"id": "location",    "text": "Ближайшая к вам станция метро или адрес (для очных консультаций)\n\nЕсли онлайн — нажмите «Пропустить»",
     "type": "text", "skip": True},

    {"id": "source",      "text": "Откуда вы узнали про меня?",                                         "type": "text"},

    {"id": "messenger",   "text": "Где вам удобнее получать обратную связь и итоги занятия?",
     "type": "choice", "options": ["WhatsApp", "Телеграм", "Другое"], "skip": True},

    {"id": "promo",       "text": "Промокод (если есть)\n\nЕсли нет — нажмите «Пропустить»",
     "type": "text", "skip": True},

    {"id": "contact",     "text": "Ваш контактный телефон или ссылка на Telegram",                      "type": "text"},
]


# ─────────────────────────────────────────────────────────────────

def get_keyboard(options, skip=False, back=True):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for opt in options:
        markup.add(types.KeyboardButton(opt))
    row = []
    if back:
        row.append(types.KeyboardButton("⬅️ Назад"))
    if skip:
        row.append(types.KeyboardButton("Пропустить"))
    if row:
        markup.add(*row)
    return markup


def get_text_keyboard(skip=False, back=True):
    if not skip and not back:
        return types.ReplyKeyboardRemove()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    row = []
    if back:
        row.append(types.KeyboardButton("⬅️ Назад"))
    if skip:
        row.append(types.KeyboardButton("Пропустить"))
    if row:
        markup.add(*row)
    return markup


def send_question(chat_id, state):
    queue    = state["queue"]
    idx      = state["step"]
    total    = state["total_main"]
    main_idx = state["main_step"]

    q        = queue[idx]
    is_first = (idx == 0)
    bar      = progress_bar(main_idx + 1, total)
    text     = bar + "\n\n📋 " + q["text"]

    if q["type"] == "choice":
        markup = get_keyboard(q.get("options", []), skip=q.get("skip", False), back=not is_first)
        bot.send_message(chat_id, text, reply_markup=markup)
    else:
        markup = get_text_keyboard(skip=q.get("skip", False), back=not is_first)
        bot.send_message(chat_id, text, reply_markup=markup)


def format_summary(answers, user):
    name     = user.first_name or ""
    username = f"@{user.username}" if user.username else f"ID: {user.id}"
    lines    = ["🐕 НОВАЯ АНКЕТА ВЛАДЕЛЬЦА", f"От: {name} ({username})", "─" * 35]
    for q_id, answer in answers.items():
        label = q_id
        for q in _all_questions():
            if q["id"] == q_id:
                label = q["text"].split("\n")[0]
                break
        lines.append(f"\n❓ {label}\n✏️ {answer}")
    lines += ["\n" + "─" * 35, "✅ Анкета заполнена полностью"]
    return "\n".join(lines)


def _all_questions():
    result = []
    for q in QUESTIONS:
        result.append(q)
        if "branch" in q:
            for branch_qs in q["branch"].values():
                result.extend(branch_qs)
    return result


# ─────────────────────────────────────────────────────────────────

user_state = {}


def init_state():
    return {
        "queue":      list(QUESTIONS),
        "step":       0,
        "main_step":  0,
        "total_main": len(QUESTIONS),
        "answers":    {},
        "history":    [],
    }


# ─────────────────────────────────────────────────────────────────

@bot.message_handler(commands=["start", "restart"])
def handle_start(message):
    uid = message.from_user.id
    user_state[uid] = init_state()
    bot.send_message(
        message.chat.id,
        "Привет! 👋\n\n"
        "Я помогу заполнить анкету перед консультацией.\n"
        "Это займёт около 5–10 минут.\n\n"
        "Отвечайте своими словами — здесь нет правильных или неправильных ответов. "
        "Чем подробнее — тем лучше я смогу подготовиться к нашей работе.\n\n"
        "Начнём! 🐾",
        reply_markup=types.ReplyKeyboardRemove()
    )
    time.sleep(0.5)
    send_question(message.chat.id, user_state[uid])


@bot.message_handler(func=lambda m: True)
def handle_answer(message):
    uid  = message.from_user.id
    text = message.text.strip()

    if uid not in user_state:
        bot.send_message(message.chat.id, "Напишите /start чтобы начать заполнение анкеты.")
        return

    state = user_state[uid]
    queue = state["queue"]
    idx   = state["step"]
    q     = queue[idx]

    # НАЗАД
    if text == "⬅️ Назад":
        if not state["history"]:
            bot.send_message(message.chat.id, "Это первый вопрос, назад некуда 🙂")
            send_question(message.chat.id, state)
            return
        prev = state["history"].pop()
        state["step"]      = prev["step"]
        state["main_step"] = prev["main_step"]
        state["queue"]     = prev["queue"]
        prev_q = state["queue"][state["step"]]
        state["answers"].pop(prev_q["id"], None)
        send_question(message.chat.id, state)
        return

    # ПРОПУСТИТЬ
    if text == "Пропустить":
        if not q.get("skip"):
            bot.send_message(message.chat.id, "На этот вопрос нужно ответить 🙏")
            send_question(message.chat.id, state)
            return
        _save_and_advance(message, state, q, "—")
        return

    # ВАЛИДАЦИЯ: только цифры
    if q["type"] == "digits":
        if not text.isdigit():
            bot.send_message(
                message.chat.id,
                "Пожалуйста, введите только цифры 🔢",
                reply_markup=get_text_keyboard(back=(idx > 0))
            )
            return

    # ВАЛИДАЦИЯ: длина текста
    if q["type"] in ("text", "digits") and len(text) > MAX_TEXT_LENGTH:
        bot.send_message(
            message.chat.id,
            f"Слишком длинный ответ. Пожалуйста, уложитесь в {MAX_TEXT_LENGTH} символов "
            f"(сейчас {len(text)}) ✂️",
            reply_markup=get_text_keyboard(skip=q.get("skip", False), back=(idx > 0))
        )
        return

    # ВАЛИДАЦИЯ: choice
    if q["type"] == "choice":
        if text not in q.get("options", []):
            bot.send_message(
                message.chat.id,
                "Пожалуйста, выберите один из вариантов кнопкой ниже 👇",
                reply_markup=get_keyboard(q["options"], skip=q.get("skip", False), back=(idx > 0))
            )
            return

    _save_and_advance(message, state, q, text)


def _save_and_advance(message, state, q, answer):
    uid = message.from_user.id

    state["history"].append({
        "step":      state["step"],
        "main_step": state["main_step"],
        "queue":     list(state["queue"]),
    })

    state["answers"][q["id"]] = answer
    state["step"] += 1

    # Вставляем ветку если нужно
    if "branch" in q and answer in q["branch"]:
        branch_qs = q["branch"][answer]
        insert_at = state["step"]
        state["queue"] = (
            state["queue"][:insert_at] +
            branch_qs +
            state["queue"][insert_at:]
        )

    answered_main = sum(1 for mq in QUESTIONS if mq["id"] in state["answers"])
    state["main_step"] = min(answered_main, len(QUESTIONS) - 1)

    if state["step"] >= len(state["queue"]):
        _finish(message, state)
    else:
        send_question(message.chat.id, state)


def _finish(message, state):
    uid = message.from_user.id

    # Сообщение клиенту
    bot.send_message(
        message.chat.id,
        "Спасибо большое! 🐾\n\n"
        "Анкета заполнена. Я изучу ваши ответы и вернусь с обратной связью в течение суток.\n\n"
        "До скорой встречи! 🤍",
        reply_markup=types.ReplyKeyboardRemove()
    )

    # Картинка клиенту
    try:
        img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "anketa_finish.png")
        if os.path.exists(img_path):
            with open(img_path, "rb") as photo:
                bot.send_photo(message.chat.id, photo)
    except Exception as e:
        print(f"Ошибка отправки картинки: {e}")

    # Анкета администратору
    summary = format_summary(state["answers"], message.from_user)
    try:
        if len(summary) <= 4096:
            bot.send_message(ADMIN_ID, summary)
        else:
            for chunk in [summary[i:i+4000] for i in range(0, len(summary), 4000)]:
                bot.send_message(ADMIN_ID, chunk)
    except Exception as e:
        print(f"Ошибка отправки администратору: {e}")

    del user_state[uid]


if __name__ == "__main__":
    print("Бот запущен. Нажмите Ctrl+C для остановки.")
    bot.infinity_polling()
