# Базіка - Telegram Агент

Workspace для агента Базіка — дружелюбного помічника у Telegram-чаті.

## Структура

```
~/.openclaw/
├── agents/
│   └── bazika/            # Базіка
└── workspace-bazika/      # Workspace для Базіки (ЦЕЙ КАТАЛОГ)
    ├── SOUL.md            # Характер і стиль Базіки
    ├── IDENTITY.md        # Хто такий Базіка
    ├── USER.md            # Опис користувачів
    └── README.md          # Цей файл
```

## Характер

Базіка — теплий і уважний помічник:
- Дружелюбний і ввічливий
- Трохи пестливий, але по суті
- Лаконічний — максимум 2-3 речення
- Шукає свіжі новини та інформацію в інтернеті
- М'яко виправляє неточності

## Редагування поведінки

Щоб змінити поведінку або роль Базіки, редагуй:
- `SOUL.md` — основний характер, тон і стиль відповідей
- `IDENTITY.md` — хто такий Базіка і яка його роль
- `USER.md` — для кого він працює і чим допомагає

`README.md` — довідковий файл для людини; він не задає поведінку напряму.

Коротко:
- `SOUL.md` = як Базіка говорить
- `IDENTITY.md` = ким Базіка є
- `USER.md` = для кого і як саме допомагає

Зміни в цих файлах у цьому workspace підхоплюються автоматично.

## Перевірка

```bash
openclaw agents list
openclaw agents bindings
openclaw channels status --probe
```

## Логи

```bash
openclaw logs --follow
openclaw logs --follow | grep bazika
```

## Self-Improvement

У репо додано workflow `.github/workflows/self-improve.yml`, який кожні 2 години може робити маленькі покращення `README.md`, `SOUL.md`, `IDENTITY.md` або `USER.md` через LLM і створювати PR.

Для цього в GitHub Secrets має бути `OPENAI_API_KEY`.

---

**Базіка завжди готовий допомогти.**
