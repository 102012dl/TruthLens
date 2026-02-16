# TruthLens - Інструкція зі створення репозиторію

## Крок 1: Створення GitHub репозиторію

### Опція A: Через веб-інтерфейс

1. Перейдіть на https://github.com/new
2. **Repository name:** `truthlens`
3. **Description:** AI-Powered Information Credibility Analysis Platform
4. **Public** або **Private**
5. Натисніть "Create repository"

### Опція B: Через GitHub CLI

```bash
# Встановлення GitHub CLI
# macOS: brew install gh
# Linux: sudo apt install gh
# Windows: winget install GitHub.cli

# Авторизація
gh auth login

# Створення репозиторію
gh repo create truthlens --public --description "AI-Powered Information Credibility Analysis Platform"
```

---

## Крок 2: Push коду на GitHub

```bash
# Перейдіть до папки проекту
cd /home/ubuntu/truthlens_github_package

# Ініціалізація Git
git init

# Додавання всіх файлів
git add .

# Перший commit
git commit -m "Initial commit: TruthLens MVP - Capstone Project"

# Додавання remote
git remote add origin https://github.com/102012dl/truthlens.git

# Push
git branch -M main
git push -u origin main
```

---

## Крок 3: Створення GitLab репозиторію (опціонально)

```bash
# Додавання GitLab як додатковий remote
git remote add gitlab https://gitlab.com/102012dl/truthlens.git

# Push на GitLab
git push gitlab main
```

---

## Крок 4: Використання Jupyter Notebook

### Google Colab

1. Відкрийте https://colab.research.google.com/
2. File > Upload notebook
3. Виберіть `notebooks/TruthLens_Capstone_Project.ipynb`
4. Виконайте всі комірки

### Jupyter Lab (локально)

```bash
pip install jupyterlab
jupyter lab notebooks/TruthLens_Capstone_Project.ipynb
```

---

## Оцінка платформ для створення MVP

| Платформа | Оцінка | Переваги | Недоліки |
|----------|--------|----------|----------|
| **Abacus.AI** | 5/5 | Повний цикл розробки, вбудований ML | Платний |
| **Cursor AI** | 4/5 | Швидкий кодинг, автокомпліт | Потребує IDE |
| **Claude** | 4/5 | Якісний код, пояснення | Немає IDE |
| **ChatGPT** | 3/5 | Доступність, популярність | Менше контексту |
| **Replit** | 4/5 | Миттєвий запуск, хостинг | Обмеження ресурсів |
| **Bolt.new** | 3/5 | Швидкий старт | Обмежений функціонал |
| **Lovable** | 3/5 | UI/UX фокус | Не для ML |
| **Google AI Studio** | 3/5 | Gemini API | Тільки API |

### Рекомендація

**Для TruthLens найкраще:** **Abacus.AI DeepAgent** (де ви зараз)
- Повний цикл розробки
- Вбудовані LLM APIs
- Автоматичний деплой
- CI/CD інтеграція

---

## Надсилання Ментору

### Email шаблон:

```
Тема: Capstone Project - TruthLens | 102012dl

Шановний Менторе,

Надсилаю матеріали Capstone Project "TruthLens".

Посилання:
- GitHub: https://github.com/102012dl/truthlens
- GitLab: https://gitlab.com/102012dl/truthlens
- Jupyter Notebook: (додано до листа)

Ключові файли:
1. README.md - документація
2. notebooks/TruthLens_Capstone_Project.ipynb - основний notebook
3. src/ - вихідний код
4. tests/ - тести

З повагою,
102012dl
102012dl@gmail.com
```

---

## Checklist перед надсиланням

- [ ] README.md повний та зрозумілий
- [ ] Всі тести проходять
- [ ] Jupyter Notebook виконується без помилок
- [ ] Docker білдиться
- [ ] CI/CD pipeline працює
- [ ] Security сканування пройдено

---

**© 2024 TruthLens | 102012dl@gmail.com**
