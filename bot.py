#!/usr/bin/env python3
"""
Бот-анкета @ira.psycho — версия 3.0
Установка: pip install pyTelegramBotAPI
Запуск: python bot_v3.py
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


# ─────────────────────────────────────────────────────────────────
# ПРОГРЕСС-БАР
# ─────────────────────────────────────────────────────────────────

def progress_bar(current, total, size=10):
    filled = round(current / total * size)
    return "🟣" * filled + "⚪️" * (size - filled) + f"  {current} из {total}"


# ─────────────────────────────────────────────────────────────────
# ВОПРОСЫ АНКЕТЫ
# ─────────────────────────────────────────────────────────────────

QUESTIONS = [
    {"id": "name",       "text": "Ваше имя",                                                            "type": "text"},
    {"id": "dog_name",   "text": "Кличка собаки",                                                       "type": "text"},
    {"id": "dog_age",    "text": "Возраст собаки",                                                      "type": "text"},
    {"id": "dog_breed",  "text": "Порода собаки (если метис — примерная порода или вес)",               "type": "text"},
    {"id": "how_got",    "text": "Как к вам попал питомец? В каком возрасте?",                          "type": "text"},
    {"id": "problems",   "text": "С какими проблемами поведения своей собаки вы столкнулись?",          "type": "text"},
    {"id": "since_when", "text": "Как давно это началось и сколько продолжается?",                      "type": "text"},
    {"id": "priority",   "text": "Какие из них вы хотите решить в первую очередь?",                     "type": "text"},
    {"id": "tried",      "text": "Что вы уже предпринимали для решения этих проблем?",                  "type": "text"},
    {"id": "goal",       "text": "Какой результат вы ждёте от наших занятий?",                          "type": "text"},
    {"id": "good",       "text": "Что хорошего есть в жизни с вашим питомцем? Как вы обычно проводите время вместе?", "type": "text"},

    {"id": "castrated",  "text": "Кастрирована ли ваша собака?",
     "type": "choice", "options": ["Да", "Нет"]},

    {"id": "vaccinated", "text": "Привита ли ваша собака?",
     "type": "choice", "options": ["Да", "Нет"]},

    {"id": "vacc_date",  "text": "Дата последней вакцинации (для собак с агрессией к людям)",
     "type": "text", "skip": True},

    {"id": "vet_check",  "text": "Как давно вы проходили полное ветеринарное обследование?",
     "type": "choice", "options": ["Менее полугода назад", "Полгода–год назад", "Более года"]},

    {"id": "chronic_yn", "text": "Есть ли у вашего питомца хронические заболевания?",
     "type": "choice", "options": ["Да", "Нет"],
     "branch": {"Да": [{"id": "chronic_what", "text": "Какие хронические заболевания?", "type": "text"}]}},

    {"id": "acute_yn",   "text": "Есть ли у вашего питомца заболевания в острой фазе?",
     "type": "choice", "options": ["Да", "Нет"],
     "branch": {"Да": [{"id": "acute_what", "text": "Какие заболевания в острой фазе?", "type": "text"}]}},

    {"id": "beh_vet_yn", "text": "Был ли опыт посещения врачей поведенческой медицины или невролога?",
     "type": "choice", "options": ["Да", "Нет"],
     "branch": {"Да": [
         {"id": "beh_vet_who",  "text": "Укажите имя врача",                                            "type": "text"},
         {"id": "beh_vet_diag", "text": "Поставленный диагноз",                                         "type": "text"},
         {"id": "beh_vet_meds", "text": "Назначенные препараты (если нет — напишите «Нет»)",            "type": "text"},
     ]}},

    {"id": "walks_count","text": "Сколько раз в день вы гуляете?",
     "type": "choice", "options": ["1–2 раза в день", "2–3 раза в день", "3–4 раза в день", "Другое"]},

    {"id": "walks_desc", "text": "Продолжительность и интенсивность ваших прогулок? (общение с другими собаками, активные игры и т.д.)", "type": "text"},
    {"id": "equipment",  "text": "Какую амуницию вы используете в быту?",                              "type": "text"},

    {"id": "trainer_yn", "text": "Был ли в прошлом опыт занятий с кинологом?",
     "type": "choice", "options": ["Да", "Нет"],
     "branch": {"Да": [{"id": "trainer_desc", "text": "Расскажите об этом. Как работали, что понравилось, что нет?", "type": "text"}]}},

    {"id": "family_yn",  "text": "Есть ли члены семьи, живущие в одном доме с собакой?",
     "type": "choice", "options": ["Да", "Нет"],
     "branch": {"Да": [
         {"id": "family_who", "text": "Кто живёт с собакой? (перечислите)",                             "type": "text"},
         {"id": "family_rel", "text": "Какие у них отношения с собакой?",                               "type": "text"},
     ]}},

    {"id": "animals_yn", "text": "Есть ли другие животные, живущие в одном доме с собакой?",
     "type": "choice", "options": ["Да", "Нет"],
     "branch": {"Да": [
         {"id": "animals_who", "text": "Какие животные живут с собакой?",                               "type": "text"},
         {"id": "animals_rel", "text": "Какие у них отношения с собакой?",                              "type": "text"},
     ]}},

    {"id": "extra",      "text": "Любая дополнительная информация о вашей собаке, которую вы считаете важной",
     "type": "text", "skip": True},

    {"id": "format",     "text": "Подходящий вам формат занятий",
     "type": "choice", "options": ["Очное занятие", "Онлайн консультация", "Сопровождение"],
     "skip": True,
     "branch": {
         "Очное занятие":  [{"id": "location", "text": "Ближайшая к вам станция метро или адрес", "type": "text"}],
         "Сопровождение":  [{"id": "location", "text": "Ближайшая к вам станция метро или адрес", "type": "text"}],
     }},

    {"id": "source",     "text": "Откуда вы узнали про меня?",                                         "type": "text"},
    {"id": "promo",      "text": "Промокод (если есть)\n\nЕсли нет — нажмите «Пропустить»",
     "type": "text", "skip": True},
]


# ─────────────────────────────────────────────────────────────────
# INLINE КНОПКИ — всегда видны, не прячутся за клавиатурой
# ─────────────────────────────────────────────────────────────────

def inline_keyboard(options=None, skip=False, back=True, is_first=False):
    """
    Строит InlineKeyboardMarkup.
    - options: список вариантов для choice-вопросов
    - skip: добавить кнопку Пропустить
    - back: добавить кнопку Назад
    - is_first: первый вопрос — кнопку Назад не показываем
    """
    markup = types.InlineKeyboardMarkup(row_width=2)

    if options:
        # Варианты ответа — каждый своей кнопкой
        for opt in options:
            markup.add(types.InlineKeyboardButton(text=opt, callback_data=f"ans:{opt}"))

    # Навигация
    nav = []
    if back and not is_first:
        nav.append(types.InlineKeyboardButton("⬅️ Назад", callback_data="nav:back"))
    if skip:
        nav.append(types.InlineKeyboardButton("Пропустить", callback_data="nav:skip"))
    # Кнопка "Написать Ирине" — всегда
    markup.add(types.InlineKeyboardButton("✍️ Написать Ирине", callback_data="nav:ask"))
    if nav:
        markup.row(*nav)

    return markup


def start_keyboard():
    """Три кнопки на старте."""
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📋 Заполнить анкету", callback_data="start:anketa"),
        types.InlineKeyboardButton("📅 Записаться на консультацию", callback_data="start:zapis"),
        types.InlineKeyboardButton("❓ Задать вопрос", callback_data="start:ask"),
    )
    return markup


# ─────────────────────────────────────────────────────────────────
# ОТПРАВКА ВОПРОСА
# ─────────────────────────────────────────────────────────────────

def send_question(chat_id, state, message_id=None):
    """Отправляет (или редактирует) вопрос с inline-кнопками."""
    queue    = state["queue"]
    idx      = state["step"]
    total    = state["total_main"]
    main_idx = state["main_step"]
    q        = queue[idx]
    is_first = (idx == 0)

    bar  = progress_bar(main_idx + 1, total)
    text = bar + "\n\n📋 " + q["text"]

    markup = inline_keyboard(
        options  = q.get("options") if q["type"] == "choice" else None,
        skip     = q.get("skip", False),
        back     = True,
        is_first = is_first,
    )

    if message_id:
        try:
            bot.edit_message_text(text, chat_id, message_id, reply_markup=markup)
            return message_id
        except Exception:
            pass

    msg = bot.send_message(chat_id, text, reply_markup=markup)
    return msg.message_id


# ─────────────────────────────────────────────────────────────────
# ФОРМАТИРОВАНИЕ АНКЕТЫ ДЛЯ АДМИНА
# ─────────────────────────────────────────────────────────────────

def format_summary(answers, user):
    name     = user.first_name or ""
    username = f"@{user.username}" if user.username else f"ID: {user.id}"
    lines    = ["🐕 *НОВАЯ АНКЕТА ВЛАДЕЛЬЦА*", f"От: {name} ({username})", "―" * 33]
    for q_id, answer in answers.items():
        label = q_id
        for q in _all_questions():
            if q["id"] == q_id:
                label = q["text"].split("\n")[0]
                break
        lines.append(f"\n{label}\n*{answer}*")
    lines += ["\n" + "―" * 33, "✅ Анкета заполнена полностью"]
    return "\n".join(lines)


def _all_questions():
    result = []
    for q in QUESTIONS:
        result.append(q)
        if "branch" in q:
            for bqs in q["branch"].values():
                result.extend(bqs)
    return result


# ─────────────────────────────────────────────────────────────────
# СОСТОЯНИЯ ПОЛЬЗОВАТЕЛЕЙ
# ─────────────────────────────────────────────────────────────────

user_state = {}
# Режимы: "anketa" | "ask" | "zapis" | None


def init_anketa_state():
    return {
        "mode":       "anketa",
        "queue":      list(QUESTIONS),
        "step":       0,
        "main_step":  0,
        "total_main": len(QUESTIONS),
        "answers":    {},
        "history":    [],
        "last_msg_id": None,
    }


# ─────────────────────────────────────────────────────────────────
# HANDLERS
# ─────────────────────────────────────────────────────────────────

@bot.message_handler(commands=["start", "restart"])
def handle_start(message):
    uid = message.from_user.id
    user_state.pop(uid, None)
    bot.send_message(
        message.chat.id,
        "Привет! 👋\n\n"
        "Я помогу вам связаться с Ирой — специалистом по поведению собак и психологом.\n\n"
        "Выберите, что вы хотите сделать:",
        reply_markup=start_keyboard()
    )


@bot.message_handler(commands=["ask"])
def handle_ask_command(message):
    _enter_ask_mode(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda m: True)
def handle_text(message):
    uid  = message.from_user.id
    text = message.text.strip()

    if uid not in user_state:
        bot.send_message(message.chat.id,
            "Нажмите /start чтобы начать.",
            reply_markup=start_keyboard())
        return

    state = user_state[uid]
    mode  = state.get("mode")

    # ── РЕЖИМ: ожидаем вопрос ─────────────────────────────────
    if mode == "ask":
        # Пересылаем вопрос администратору
        name     = message.from_user.first_name or ""
        username = f"@{message.from_user.username}" if message.from_user.username else f"ID: {uid}"
        try:
            bot.send_message(
                ADMIN_ID,
                f"❓ *ВОПРОС ОТ ПОЛЬЗОВАТЕЛЯ*\nОт: {name} ({username})\n\n{text}",
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Ошибка пересылки вопроса: {e}")

        bot.send_message(
            message.chat.id,
            "Ваш вопрос отправлен! 🙏\n\n"
            "Ира ответит вам лично в ближайшее время.",
            reply_markup=start_keyboard()
        )
        user_state.pop(uid, None)
        return

    # ── РЕЖИМ: анкета, ждём текстовый ответ ──────────────────
    if mode == "anketa":
        q = state["queue"][state["step"]]

        if q["type"] == "choice":
            bot.send_message(
                message.chat.id,
                "Пожалуйста, выберите вариант кнопкой выше 👆"
            )
            return

        if len(text) > MAX_TEXT_LENGTH:
            bot.send_message(
                message.chat.id,
                f"Слишком длинный ответ. Уложитесь в {MAX_TEXT_LENGTH} символов "
                f"(сейчас {len(text)}) ✂️"
            )
            return

        _save_and_advance(message.chat.id, uid, state, q, text)
        return

    # ── Режим: запись ─────────────────────────────────────────
    if mode == "zapis":
        name     = message.from_user.first_name or ""
        username = f"@{message.from_user.username}" if message.from_user.username else f"ID: {uid}"
        try:
            bot.send_message(
                ADMIN_ID,
                f"📅 *ЗАПРОС НА ЗАПИСЬ*\nОт: {name} ({username})\n\n{text}",
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Ошибка пересылки: {e}")
        bot.send_message(
            message.chat.id,
            "Запрос отправлен! 🙏 Ира свяжется с вами для согласования времени.",
            reply_markup=start_keyboard()
        )
        user_state.pop(uid, None)


# ─────────────────────────────────────────────────────────────────
# CALLBACK HANDLER — все нажатия на inline-кнопки
# ─────────────────────────────────────────────────────────────────

@bot.callback_query_handler(func=lambda c: True)
def handle_callback(call):
    uid     = call.from_user.id
    chat_id = call.message.chat.id
    data    = call.data

    bot.answer_callback_query(call.id)

    # ── СТАРТ ─────────────────────────────────────────────────
    if data == "start:anketa":
        state = init_anketa_state()
        user_state[uid] = state
        bot.send_message(
            chat_id,
            "Отлично! Заполняем анкету 🐾\n\n"
            "Это займёт около 5–10 минут. Отвечайте своими словами — "
            "чем подробнее, тем лучше я смогу подготовиться к работе с вами."
        )
        time.sleep(0.3)
        msg_id = send_question(chat_id, state)
        state["last_msg_id"] = msg_id
        return

    if data == "start:zapis":
        user_state[uid] = {"mode": "zapis"}
        bot.send_message(
            chat_id,
            "Напишите удобное время для консультации или любой комментарий — "
            "Ира свяжется с вами для согласования 📅"
        )
        return

    if data == "start:ask":
        _enter_ask_mode(uid, chat_id)
        return

    # ── КНОПКА «НАПИСАТЬ ИРИНЕ» из любого места ───────────────
    if data == "nav:ask":
        _enter_ask_mode(uid, chat_id)
        return

    # ── НАВИГАЦИЯ В АНКЕТЕ ────────────────────────────────────
    if uid not in user_state or user_state[uid].get("mode") != "anketa":
        return

    state = user_state[uid]

    if data == "nav:back":
        if not state["history"]:
            bot.send_message(chat_id, "Это первый вопрос, назад некуда 🙂")
            return
        prev = state["history"].pop()
        state["step"]      = prev["step"]
        state["main_step"] = prev["main_step"]
        state["queue"]     = prev["queue"]
        prev_q = state["queue"][state["step"]]
        state["answers"].pop(prev_q["id"], None)
        msg_id = send_question(chat_id, state, state.get("last_msg_id"))
        state["last_msg_id"] = msg_id
        return

    if data == "nav:skip":
        q = state["queue"][state["step"]]
        if not q.get("skip"):
            bot.send_message(chat_id, "На этот вопрос нужно ответить 🙏")
            return
        _save_and_advance(chat_id, uid, state, q, "—")
        return

    # ── ОТВЕТ НА CHOICE-ВОПРОС ────────────────────────────────
    if data.startswith("ans:"):
        answer = data[4:]
        q      = state["queue"][state["step"]]
        if q["type"] != "choice" or answer not in q.get("options", []):
            return
        _save_and_advance(chat_id, uid, state, q, answer)
        return


# ─────────────────────────────────────────────────────────────────
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ─────────────────────────────────────────────────────────────────

def _enter_ask_mode(uid, chat_id):
    """Переводит пользователя в режим вопроса."""
    # Сохраняем текущее состояние анкеты если было
    prev = user_state.get(uid)
    user_state[uid] = {"mode": "ask", "prev_state": prev}
    bot.send_message(
        chat_id,
        "Напишите ваш вопрос — я передам его Ире ✍️\n\n"
        "Она ответит вам лично в ближайшее время."
    )


def _save_and_advance(chat_id, uid, state, q, answer):
    """Сохраняет ответ, вставляет ветку, переходит к следующему вопросу."""
    state["history"].append({
        "step":      state["step"],
        "main_step": state["main_step"],
        "queue":     list(state["queue"]),
    })

    state["answers"][q["id"]] = answer
    state["step"] += 1

    # Ветвление
    if "branch" in q and answer in q["branch"]:
        branch_qs = q["branch"][answer]
        ins = state["step"]
        state["queue"] = state["queue"][:ins] + branch_qs + state["queue"][ins:]

    # Обновляем прогресс
    answered_main = sum(1 for mq in QUESTIONS if mq["id"] in state["answers"])
    state["main_step"] = min(answered_main, len(QUESTIONS) - 1)

    if state["step"] >= len(state["queue"]):
        _finish(chat_id, uid, state)
    else:
        msg_id = send_question(chat_id, state, state.get("last_msg_id"))
        state["last_msg_id"] = msg_id


def _finish(chat_id, uid, state):
    """Завершение анкеты."""
    # Убираем inline-кнопки с последнего вопроса
    if state.get("last_msg_id"):
        try:
            bot.edit_message_reply_markup(chat_id, state["last_msg_id"],
                                          reply_markup=types.InlineKeyboardMarkup())
        except Exception:
            pass

    bot.send_message(
        chat_id,
        "Спасибо большое! 🐾\n\n"
        "Анкета заполнена. Я изучу ваши ответы и вернусь с обратной связью в течение суток.\n\n"
        "До скорой встречи! 🤍"
    )

    # Картинка
    try:
        img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "anketa_finish.png")
        if os.path.exists(img_path):
            with open(img_path, "rb") as photo:
                bot.send_photo(chat_id, photo)
    except Exception as e:
        print(f"Ошибка картинки: {e}")

    # Анкета администратору
    summary = format_summary(state["answers"], bot.get_chat(chat_id))
    try:
        if len(summary) <= 4096:
            bot.send_message(ADMIN_ID, summary, parse_mode="Markdown")
        else:
            for chunk in [summary[i:i+4000] for i in range(0, len(summary), 4000)]:
                bot.send_message(ADMIN_ID, chunk, parse_mode="Markdown")
    except Exception as e:
        print(f"Ошибка отправки анкеты: {e}")

    user_state.pop(uid, None)


if __name__ == "__main__":
    print("Бот запущен. Нажмите Ctrl+C для остановки.")
    bot.infinity_polling()
