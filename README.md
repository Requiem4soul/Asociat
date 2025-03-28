**README**

# 1. В начале:
- **Изменить логин и пароль** в коде программы. Найдите следующие строки и замените `*****` на свои данные:
  ```python
  username_field.send_keys("*****")
  password_field.send_keys("******")
  ```
![изображение](https://github.com/user-attachments/assets/b5857d86-6da5-428d-bc66-95e473daf563)

- **Изменить словарь ассоциаций**. В коде есть словарь `associations`. Обязательно подставьте свои ассоциации!
![изображение](https://github.com/user-attachments/assets/0230fe30-dbfd-4f5c-bb9c-fc72042a5528)

---

# 2. Установка:
- **Шаг 1:** Установить `uv`. В PowerShell выполните команду:
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
![изображение](https://github.com/user-attachments/assets/d98b54ee-995c-4872-a01b-b1c703f813c8)
![изображение](https://github.com/user-attachments/assets/ddd2366a-58a6-4874-baed-d9d0485c7da2)

- **Шаг 2:** Перейти в папку проекта.
![изображение](https://github.com/user-attachments/assets/4215d9a8-1596-4894-8eb8-281b96125f93)

- **Шаг 3:** Открыть PowerShell в папке проекта.
![изображение](https://github.com/user-attachments/assets/711c9ea8-1a25-4ee4-9476-ebd1db6a1224)

- **Шаг 4:** В PowerShell выполнить:
  ```powershell
  uv sync
  ```
![изображение](https://github.com/user-attachments/assets/1f95c9b4-0676-43a7-9c6a-6a091c3264d9)

- Готово!

---

# 3. Запуск программы:
- **Шаг 1:** Перейти в корень проекта и открыть PowerShell.
![изображение](https://github.com/user-attachments/assets/80a4829f-5f59-4805-b9ee-101851e5a850)

- **Шаг 2:** Запустить программу командой:
  ```powershell
  uv run main.py
  ```
![изображение](https://github.com/user-attachments/assets/fc715035-9e0d-4bcc-aed4-dffd4517557a)

---

# 4. Дополнительные рекомендации:
- Лучше **запускать программу на втором рабочем столе** и сразу переключаться на первый (Win + Tab).
- **Окна браузера не трогать** во время работы программы.


