import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# Словарь ассоциаций с вероятностями
associations = {
    "Власть": [("Народ", 0.3), ("Государство", 0.3), ("Сила", 0.2), ("Политика", 0.2)],
    "Совесть": [("Поступки", 0.3), ("Чистота", 0.2), ("Честь", 0.3), ("Мораль", 0.2)],
    "Отец": [("Родня", 0.3), ("Семья", 0.3), ("Мужчина", 0.2), ("Родитель", 0.2)],
    "Иностранец": [("Англичанин", 0.2), ("Чужак", 0.3), ("Гость", 0.2), ("Турист", 0.3)],
    "Богатый": [("Состояние", 0.3), ("Деньги", 0.3), ("Бизнес", 0.2), ("Роскошь", 0.2)],
    "Нищий": [("Бедность", 0.4), ("Горе", 0.2), ("Деньги", 0.2), ("Нужда", 0.2)],
    "Правда": [("Истина", 0.4), ("Сила", 0.2), ("Ложь", 0.2), ("Честность", 0.2)],
    "Ложь": [("Вранье", 0.3), ("Фейк", 0.2), ("Обман", 0.3), ("Хитрость", 0.2)],
    "Смысл": [("Жизнь", 0.4), ("Цель", 0.3), ("Средства", 0.1), ("Идея", 0.2)],
    "Злой": [("Эмоция", 0.2), ("Человек", 0.3), ("Опасность", 0.2), ("Агрессия", 0.3)],
    "Добрый": [("Человек", 0.3), ("Хороший", 0.3), ("Вежливый", 0.2), ("Заботливый", 0.2)],
    "Думать": [("Мыслить", 0.3), ("Существовать", 0.2), ("Голова", 0.2), ("Анализировать", 0.3)],
    "Мы": [("Люди", 0.3), ("Народ", 0.3), ("Местоимение", 0.2), ("Единство", 0.2)],
    "Они": [("Люди", 0.3), ("Местоимение", 0.2), ("Другие", 0.3), ("Общество", 0.2)],
    "Я": [("Человек", 0.3), ("Личность", 0.3), ("Думать", 0.2), ("Субъект", 0.2)],
    "Враг": [("Друг", 0.2), ("Человек", 0.3), ("Соперник", 0.2), ("Противник", 0.3)],
    "Друг": [("Человек", 0.3), ("Приятель", 0.2), ("Свой", 0.2), ("Товарищ", 0.3)],
    "Человек": [("Личность", 0.3), ("Персона", 0.2), ("Вид", 0.2), ("Индивид", 0.3)],
    "Уважение": [("Заслуга", 0.2), ("Достоинство", 0.3), ("Поступки", 0.3), ("Признание", 0.2)],
    "Страх": [("Опасность", 0.3), ("Темнота", 0.3), ("Фобия", 0.2), ("Тревога", 0.2)],
    "Русские": [("Народ", 0.4), ("Мы", 0.2), ("Язык", 0.2), ("Культура", 0.2)],
    "Надеяться": [("Верить", 0.3), ("Исход", 0.2), ("Ожидание", 0.3), ("Мечта", 0.2)],
    "Сильный": [("Человек", 0.3), ("Мощь", 0.2), ("Мускулы", 0.2), ("Уверенный", 0.3)],
    "Слабый": [("Хрупкий", 0.2), ("Человек", 0.3), ("Черта", 0.2), ("Уязвимый", 0.3)],
    "Люди": [("Народ", 0.3), ("Общество", 0.3), ("Вид", 0.2), ("Человечество", 0.2)],
    "Общество": [("Социум", 0.2), ("Народ", 0.3), ("Люди", 0.3), ("Мнение", 0.2)],
    "Помогать": [("Благо", 0.2), ("Добро", 0.3), ("Действие", 0.2), ("Поддержка", 0.3)],
    "Долг": [("Деньги", 0.2), ("Кредит", 0.2), ("Честь", 0.3), ("Ответственность", 0.3)],
    "Будущее": [("Время", 0.3), ("Надежды", 0.3), ("Мечты", 0.2), ("Прошлое", 0.2)],
    "Прошлое": [("Будущее", 0.2), ("Время", 0.3), ("Детство", 0.3), ("Воспоминания", 0.2)],
    "Жизнь": [("Смысл", 0.3), ("Человек", 0.2), ("Существование", 0.2), ("Смерть", 0.3)],
    "Смерть": [("Утрата", 0.3), ("Потеря", 0.3), ("Похороны", 0.2), ("Горе", 0.2)],
    "Свой": [("Человек", 0.2), ("Родной", 0.3), ("Приятель", 0.2), ("Друг", 0.3)],
    "Чужой": [("Человек", 0.2), ("Незнакомец", 0.3), ("Посторонний", 0.2), ("Чужак", 0.3)],
    "Правильно": [("Верно", 0.3), ("Совесть", 0.2), ("Честь", 0.2), ("Ответ", 0.3)],
    "Сестра": [("Родня", 0.3), ("Девушка", 0.2), ("Человек", 0.2), ("Брат", 0.3)],
    "Брат": [("Родня", 0.3), ("Мужчина", 0.2), ("Человек", 0.2), ("Сестра", 0.3)],
    "Мама": [("Забота", 0.3), ("Женщина", 0.2), ("Любовь", 0.3), ("Родня", 0.2)],
    "Мать": [("Забота", 0.3), ("Женщина", 0.2), ("Любовь", 0.3), ("Родня", 0.2)],
    "Бабушка": [("Родня", 0.3), ("Дедушка", 0.2), ("Старость", 0.2), ("Женщина", 0.3)],
    "Дедушка": [("Родня", 0.3), ("Бабушка", 0.2), ("Старость", 0.2), ("Мужчина", 0.3)],
    "Сосед": [("Квартира", 0.2), ("Дом", 0.3), ("Мужчина", 0.3), ("Знакомый", 0.2)],
    "Соседка": [("Девушка", 0.2), ("Дом", 0.3), ("Человек", 0.2), ("Знакомый", 0.3)],
    "Наш": [("Ваш", 0.2), ("Человек", 0.2), ("Предмет", 0.3), ("Общий", 0.3)],
    "Зло": [("Добро", 0.3), ("Враг", 0.2), ("Ненависть", 0.3), ("Поступки", 0.2)],
    "Добро": [("Зло", 0.2), ("Справедливость", 0.3), ("Честность", 0.2), ("Положительный", 0.3)],
    "Иметь": [("Обладать", 0.3), ("Предмет", 0.3), ("Мнение", 0.2), ("Действие", 0.2)],
    "Радость": [("Эмоция", 0.3), ("Веселье", 0.3), ("Горе", 0.2), ("Счастье", 0.2)],
    "Счастье": [("Чувство", 0.3), ("Эмоция", 0.3), ("Радость", 0.2), ("Любовь", 0.2)],
    "Горе": [("Эмоция", 0.3), ("Утрата", 0.2), ("Печаль", 0.3), ("Беда", 0.2)],
    "Вера": [("Религия", 0.3), ("Надежда", 0.3), ("Бог", 0.2), ("Будущее", 0.2)],
    "Доверие": [("Друг", 0.3), ("Приятель", 0.2), ("Тайна", 0.2), ("Честность", 0.3)],
    "Надо": [("Обязанность", 0.3), ("Необходимость", 0.3), ("Требование", 0.2), ("Цель", 0.2)],
    "Глаза": [("Орган", 0.3), ("Взгляд", 0.3), ("Смотреть", 0.2), ("Уши", 0.2)],
    "Говорить": [("Слушать", 0.2), ("Общаться", 0.3), ("Обсуждение", 0.2), ("Рот", 0.3)],
    "Ты": [("Я", 0.3), ("Человек", 0.2), ("Обращение", 0.2), ("Местоимение", 0.3)],
    "Россия": [("Народ", 0.3), ("Страна", 0.3), ("Общество", 0.2), ("Дом", 0.2)],
    "Буряты": [("Народ", 0.4), ("Сибирь", 0.3), ("Холод", 0.2), ("Культура", 0.1)],
    "Работа": [("Волк", 0.2), ("Труд", 0.3), ("Утро", 0.2), ("Усталость", 0.3)],
    "Мужчина": [("Пол", 0.2), ("Человек", 0.3), ("Парень", 0.2), ("Сильный", 0.3)],
    "Женщина": [("Пол", 0.2), ("Человек", 0.3), ("Девушка", 0.2), ("Мать", 0.3)],
    "Герой": [("Человек", 0.3), ("Поступок", 0.3), ("Справедливость", 0.2), ("Сказки", 0.2)],
    "Сила": [("Мускулы", 0.2), ("Правда", 0.3), ("Грубость", 0.2), ("Слова", 0.3)],
    "Помощь": [("Поддержка", 0.3), ("Добро", 0.3), ("Поступок", 0.2), ("Друг", 0.2)],
    "Справедливость": [("Честность", 0.3), ("Суд", 0.2), ("Совесть", 0.2), ("Вера", 0.3)],
    "Близкий": [("Друг", 0.3), ("Человек", 0.3), ("Путь", 0.2), ("Далекий", 0.2)],
    "Ум": [("Мозг", 0.3), ("Острый", 0.2), ("Голова", 0.2), ("Мыслить", 0.3)],
    "Душа": [("Человек", 0.3), ("Тело", 0.2), ("Сознание", 0.2), ("Сердце", 0.3)],
    "Тело": [("Человек", 0.3), ("Душа", 0.2), ("Здоровье", 0.2), ("Мышцы", 0.3)],
    "Далекий": [("Путь", 0.3), ("Взгляд", 0.2), ("План", 0.2), ("Близкий", 0.3)],
    "Вещь": [("Предмет", 0.3), ("Объект", 0.2), ("Имущество", 0.2), ("Одежда", 0.3)],
    "Еда": [("Радость", 0.2), ("Деньги", 0.2), ("Обед", 0.3), ("Ужин", 0.3)],
    "Ненавидеть": [("Глагол", 0.2), ("Враждовать", 0.3), ("Злиться", 0.3), ("Презирать", 0.2)],
    "Любить": [("Глагол", 0.2), ("Страсть", 0.2), ("Забота", 0.3), ("Привязанность", 0.3)],
    "Темный": [("Светлый", 0.2), ("Помещение", 0.3), ("Темнота", 0.3), ("Освещение", 0.2)],
    "Бедный": [("Горе", 0.3), ("Деньги", 0.2), ("Нищета", 0.3), ("Сожаление", 0.2)],
    "Жить": [("Думать", 0.2), ("Существовать", 0.3), ("Надеяться", 0.2), ("Верить", 0.3)],
    "Беда": [("Горе", 0.3), ("Печаль", 0.3), ("Несчастье", 0.2), ("Трудности", 0.2)],
    "Закон": [("Справедливость", 0.3), ("Суд", 0.3), ("Народ", 0.2), ("Порядок", 0.2)],
    "Язык": [("Слова", 0.3), ("Русский", 0.3), ("Орган", 0.2), ("Вкус", 0.2)],
    "Бог": [("Вера", 0.3), ("Религия", 0.3), ("Иисус", 0.2), ("Христианство", 0.2)],
    "Умный": [("Человек", 0.3), ("Черта", 0.2), ("Глупый", 0.2), ("Знания", 0.3)],
    "Глупый": [("Человек", 0.3), ("Черта", 0.2), ("Умный", 0.2), ("Недостаток", 0.3)],
    "Дорога": [("Путь", 0.3), ("Асфальт", 0.2), ("Машина", 0.2), ("Путешествие", 0.3)],
    "Чистый": [("Пол", 0.3), ("Комната", 0.3), ("Воздух", 0.2), ("Вода", 0.2)],
    "Грязный": [("Пол", 0.3), ("Запах", 0.2), ("Пыль", 0.3), ("Грязь", 0.2)],
    "Любовь": [("Чувство", 0.3), ("Мать", 0.2), ("Забота", 0.3), ("Семья", 0.2)],
    "Хороший": [("Человек", 0.3), ("Добрый", 0.3), ("Справедливый", 0.2), ("Качество", 0.2)],
    "Плохой": [("Человек", 0.3), ("Злой", 0.2), ("Поступок", 0.3), ("Негатив", 0.2)],
    "Можно": [("Добро", 0.2), ("Разрешение", 0.3), ("Вопрос", 0.2), ("Действие", 0.3)],
    "Наши": [("Общее", 0.3), ("Люди", 0.3), ("Вещи", 0.2), ("Свой", 0.2)],
    "Родной": [("Дом", 0.3), ("Человек", 0.2), ("Семья", 0.3), ("Близкий", 0.2)],
    "Личность": [("Персона", 0.3), ("Человек", 0.3), ("Мнение", 0.2), ("Индивид", 0.2)],
    "Сердце": [("Мышца", 0.2), ("Человек", 0.3), ("Кровь", 0.2), ("Душа", 0.3)],
    "Деньги": [("Бумага", 0.2), ("Валюта", 0.3), ("Зеленый", 0.2), ("Богатство", 0.3)],
    "Гость": [("Человек", 0.3), ("Дом", 0.3), ("Приглашение", 0.2), ("Визит", 0.2)],
    "Плохо": [("Поступок", 0.3), ("Чувствовать", 0.2), ("Здоровье", 0.3), ("Негатив", 0.2)],
    "Хорошо": [("Добро", 0.3), ("Разрешение", 0.2), ("Оценка", 0.3), ("Позитив", 0.2)],
    "Обман": [("Ложь", 0.3), ("Вранье", 0.3), ("Кража", 0.2), ("Хитрость", 0.2)],
    "Нельзя": [("Можно", 0.2), ("Запрет", 0.3), ("Ограничение", 0.3), ("Правило", 0.2)],
    "Мир": [("Круг", 0.2), ("Земля", 0.3), ("Война", 0.2), ("Спокойствие", 0.3)],
    "Семья": [("Родня", 0.3), ("Люди", 0.2), ("Дом", 0.3), ("Любовь", 0.2)],
    "Народ": [("Общество", 0.3), ("Люди", 0.3), ("Воля", 0.2), ("Культура", 0.2)],
    "Стыд": [("Позор", 0.3), ("Эмоция", 0.3), ("Неудача", 0.2), ("Совесть", 0.2)],
    "Мои": [("Вещи", 0.3), ("Предметы", 0.3), ("Мысли", 0.2), ("Свой", 0.2)],
    "Жадный": [("Человек", 0.3), ("Скупой", 0.3), ("Деньги", 0.2), ("Эгоизм", 0.2)],
    "Свобода": [("Выбор", 0.3), ("Народ", 0.2), ("Радость", 0.2), ("Право", 0.3)],
    "Дом": [("Квартира", 0.2), ("Семья", 0.3), ("Родина", 0.3), ("Уют", 0.2)],
    "Земля": [("Грязь", 0.3), ("Круг", 0.2), ("Планета", 0.3), ("Почва", 0.2)],
    "Идти": [("Ноги", 0.3), ("Пешком", 0.3), ("Путь", 0.2), ("Движение", 0.2)],
    "Время": [("Деньги", 0.2), ("Часы", 0.3), ("Труд", 0.2), ("Жизнь", 0.3)],
    "Цель": [("Задача", 0.3), ("Требование", 0.2), ("Работа", 0.2), ("Мечта", 0.3)],
    "Большой": [("Человек", 0.2), ("Предмет", 0.3), ("Размер", 0.3), ("Великий", 0.2)],
    "Маленький": [("Человек", 0.2), ("Поэзия", 0.2), ("Размер", 0.3), ("Малый", 0.3)],
    "Грязь": [("Осень", 0.2), ("Земля", 0.3), ("Лужи", 0.3), ("Пыль", 0.2)],
    "Он": [("Местоимение", 0.3), ("Парень", 0.2), ("Мужчина", 0.3), ("Человек", 0.2)],
    "Делать": [("Действие", 0.3), ("Дело", 0.3), ("Работа", 0.2), ("Процесс", 0.2)],
    "Мой": [("Твой", 0.2), ("Предмет", 0.3), ("Дом", 0.3), ("Свой", 0.2)],
    "Ребенок": [("Младенец", 0.3), ("Маленький", 0.3), ("Плач", 0.2), ("Сын", 0.2)],
    "Чистота": [("Порядок", 0.3), ("Дом", 0.3), ("Уборка", 0.2), ("Свежесть", 0.2)],
    "Забота": [("Любовь", 0.3), ("Мать", 0.3), ("Добро", 0.2), ("Тепло", 0.2)],
    "Выбор": [("Свобода", 0.3), ("Пути", 0.2), ("Решение", 0.3), ("Возможность", 0.2)],
    "Родина": [("Страна", 0.3), ("Народ", 0.3), ("Дом", 0.3), ("Общество", 0.2)],
}

# Функция для форматирования слова по правилам
def format_word(word):
    word = word.replace("ё", "е")  # Заменяем "ё" на "е"
    return word.capitalize()  # Первая буква заглавная

# Настройка Selenium
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://dictionary-exp-frontend.vercel.app/")

# Логи
print("Начало работы программы...")
print("Авторизация...")

try:
    # Ожидание загрузки страницы авторизации
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    print("Страница авторизации загрузилась")

    # Авторизация
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//label[text()='Имя пользователя']/following-sibling::div/input"))
    )
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//label[text()='Пароль']/following-sibling::div/input"))
    )
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )

    username_field.send_keys("******")
    password_field.send_keys("******")
    login_button.click()

    print("Авторизация прошла успешно!")

    # Ожидание загрузки страницы опроса (таблицы со словами)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table/tbody/tr/td[1]"))
    )
    print("Страница опроса загрузилась")

    # Цикл для заполнения 116 слов
    for i in range(116):
        print(f"Итерация {i + 1} из 116")

        # Извлекаем текущее слово
        try:
            word_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//table/tbody/tr/td[1]"))
            )
            current_word = word_element.text.strip()
            print(f"Текущее слово: {current_word}")
        except Exception as e:
            print(f"Ошибка: не удалось найти слово на странице! ({e})")
            driver.quit()
            sys.exit(1)

        # Проверяем наличие слова в словаре
        if current_word not in associations:
            print(f"Ошибка: слово '{current_word}' отсутствует в словаре ассоциаций!")
            driver.quit()
            sys.exit(1)

        # Находим поле ввода
        try:
            input_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "input"))
            )
        except Exception as e:
            print(f"Ошибка: не удалось найти поле ввода! ({e})")
            driver.quit()
            sys.exit(1)

        # Выбираем ассоциацию с вероятностью
        options, weights = zip(*associations[current_word])
        association = random.choices(options, weights=weights, k=1)[0]
        formatted_association = format_word(association)
        print(f"Выбрана ассоциация: {formatted_association}")

        # Вводим ассоциацию
        input_field.clear()
        input_field.send_keys(formatted_association)

        # Находим и нажимаем кнопку "Далее"
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))
            )
            if not next_button.is_enabled():
                print("Ошибка: кнопка 'Далее' неактивна!")
                driver.quit()
                sys.exit(1)
            next_button.click()
            print("Кнопка 'Далее' нажата")
        except Exception as e:
            print("Программа завершена. Браузер остаётся открытым для просмотра результата.")
            # Браузер не закрывается, программа просто ждёт
            while True:
                time.sleep(1)  # Бесконечный цикл

        # Случайная задержка от 4 до 8 секунд для каждого слова
        delay = random.uniform(4, 8)
        print(f"Ожидание {delay:.2f} секунд...")
        time.sleep(delay)

    print("Все 116 слов обработаны успешно!")
    print("Браузер остаётся открытым. Проверьте результат и нажмите финальную кнопку отправки, если требуется.")
    while True:
        time.sleep(1)  # Бесконечный цикл, чтобы браузер оставался открытым

except Exception as e:
    print(f"Критическая ошибка: {e}")
    print("Браузер остаётся открытым для анализа ошибки.")
    while True:
        time.sleep(1)  # Бесконечный цикл, чтобы браузер не закрылся

# Закрываем браузер
# driver.quit()
# print("Программа завершена.")