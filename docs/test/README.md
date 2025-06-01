

# Тестування працездатності системи

## Передумови

### 1. Встановити залежності проєкту

```bash
pip install -U fastapi
pip show fastapi
pip install uvicorn
```

### 2. Запустити сервер

```bash
uvicorn src.api.main:app --reload
```

## Перевірка працездатності сервісів

### POST: Створити користувача

![alt text](1.jpeg)

### GET: Отримати список всіх користувачів

![alt text](2.jpeg)

### PUT: Оновити користувача

![alt text](3.png)

### DELETE: Видалити користувача

![alt text](4.jpeg)

### POST: Створити роль

![alt text](5.jpeg)

### GET: Отримати усі ролі

![alt text](6.jpeg)

### PUT: Оновити роль

![alt text](7.jpeg)

### DELETE: Видалити роль

![alt text](8.jpeg)

### POST: Створити дозвіл

![alt text](9.jpeg)

### GET: Отримати всі дозволи

![alt text](10.jpeg)

### PUT: Оновити дозвіл     

![alt text](11.jpeg)

### DELETE: Видалити дозвіл

![alt text](12.jpeg)