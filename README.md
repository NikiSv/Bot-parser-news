#### Телеграм-бот для отслеживания новостей.

##### Использование
1. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```

2. Зарегистрируйте бота в Telegram и получите его API-ключ.

3. Задайте следующие переменные окружения:
   - `URL`: Адрес страницы, которую вы хотите парсить.
   - `API_KEY`: API-ключ вашего Telegram-бота.
   - `WEBSITE`: Начало URL-адреса для формирования ссылки на полные новости.

4. Запустите бота:
   ```
   python main.py
   ```

5. В Telegram найдите своего бота и начните с ним диалог. Он будет автоматически отправлять вам новости, найденные на заданной странице.

