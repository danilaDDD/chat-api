## Запуск проекта

### **Запуск из Docker**
1.  Добавьте в папку `conf` файл `.env.dev` с переменными окружения для подключения к базе данных.

    **Пример содержимого файла:**
    ```.env.dev
    DB_PREFIX=postgresql+asyncpg
    DB_NAME=chat_db
    DB_USER=pyuser
    # Для запуска из Docker значение DB_HOST=db, для локального запуска - localhost
    DB_HOST=db
    DB_PASSWORD=float136
    DB_PORT=5432
    ```

2.  Из корня проекта выполните команду:
    ```bash
    ./run_app
    ```
    *или*
    ```bash
    docker-compose down && docker-compose up --build app
    ```

**Важно:** Для запуска из Docker в файле `.env.dev` укажите `DB_HOST=db`.

### Локальный запуск проекта
*   Требуется версия Python 3.12+.
*   Создайте виртуальное окружение в корне проекта:
    ```bash
    python -m venv env
    ```
*   Активируйте его:
    *   **Linux/macOS:**
        ```bash
        source env/bin/activate
        ```
    *   **Windows:**
        ```bash
        .\env\Scripts\activate
        ```
*   Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```
*   Запустите приложение:
    *   **Linux/macOS:**
        ```bash
        ./sh/start.sh
        ```
    *   **Windows (или альтернатива):**
        ```bash
        python -m uvicorn app.main:app --reload
        ```

### Запуск тестов
1.  Тесты находятся в директории `test`.
2.  В директории `conf` создайте файл `.env.test`.
    **Пример содержимого файла:**
    ```.env.test
    DB_PREFIX=postgresql+asyncpg
    DB_NAME=chat_db_test
    DB_USER=pyuser
    DB_HOST=localhost
    DB_PASSWORD=float136
    DB_PORT=5432
    ```
3.  Создайте и активируйте виртуальное окружение (см. предыдущий раздел).
4.  Запустите тесты командой:
    ```bash
    pytest -v test
    ```