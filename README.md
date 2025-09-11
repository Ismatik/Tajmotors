# Tajmotors Telegram Bot
<figuer>
    <img src = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTYTBTg29dYfcyPKgQkJHW0ay87RRgs_fCUag&s' alt = 'TajMotors, Tajikistan'>
    <figcaption>Официальный дилерский центр Тойота в Душанбе..</figcaption>
</figure>

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Why Tajmotors?](#why-tajmotors)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Testing](#testing)
- [Project Structure](#project-structure)
- [License](#license)
- [Links](#links)

---

## Overview

**Tajmotors** is a versatile developer toolkit for building scalable, feature-rich Telegram bots focused on automotive customer engagement. It streamlines the development of complex workflows such as user registration, profile management, service scheduling, and mass notifications, all within a modular architecture.

---

## Features

- **Modular Handlers:** Easily extend and customize user interaction flows like registration, profile editing, and test drive scheduling.
- **Mass Messaging API:** Send scalable notifications and updates to users stored in Excel databases without blocking operations.
- **Centralized Configuration:** Manage localization, environment settings, and prompts efficiently across the system.
- **Excel Data Integration:** Seamlessly retrieve and update user info, service history, and test drive data.
- **Multilingual Support:** Built-in constants and prompts facilitate a multilingual user experience.
- **State Management:** Structured classes ensure smooth multi-step workflows and user session handling.

---

## Why Tajmotors?

This project empowers developers to create reliable, multilingual Telegram bots with ease. Tajmotors is designed for automotive businesses seeking to automate customer interactions, manage service requests, and provide instant support—all through Telegram.

---

## Getting Started

### Prerequisites

- Python 3.8+
- Telegram Bot Token (from [BotFather](https://core.telegram.org/bots#botfather))
- Excel files for user and service data management

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Ismatik/tajmotors
   cd tajmotors

2. **Install dependencies:**
    pip install -r requirements.txt

3. **Configure environment variables:**
    Create a .env file and add your bot token and other settings as needed.

### Usage

1. **Run the bot:**
   python tajmotors.py

2. **Interact with the bot on Telegram:**
    ● Start the bot with /start
    ● Register, edit your profile, schedule services, and more using the intuitive menu.

**Testing**
○ Manual testing: Interact with the bot in Telegram and verify workflows.
○ Automated tests: Add unit tests for handlers and functions as needed.

## Project Structure
tajmotors/
├── handlers/                # Bot handlers for registration, service, test drive, etc.
├── edit_profile/            # Modular profile editing handlers
├── Registration_functions/  # Excel integration and user data management
├── [config_reader.py](http://_vscodecontentref_/0)         # Centralized configuration and localization
├── [tajmotors.py](http://_vscodecontentref_/1)             # Main bot entry point
├── [requirements.txt](http://_vscodecontentref_/2)         # Python dependencies
├── [README.md](http://_vscodecontentref_/3)                # Project documentation


### License
    This project is for demonstration purposes. For commercial use, please contact the author.

### Links
    Telegram Bot API Documentation

    
**ТЗ от Tajmotors**


1. Функциональные требования к Telegram-боту (интерфейс для клиента)
    • При первом запуске (/start) бот приветствует пользователя, кратко описывает свои возможности и отображает главное меню.
    • Навигация по боту осуществляется с помощью кнопок (inline-клавиатура).
    • После каждой успешной отправки заявки бот информирует пользователя о том, что его запрос принят в работу ("Спасибо! Ваша заявка принята. Менеджер свяжется с вами в ближайшее время.").
Состоит из следующих кнопок:
    • Каталог автомобилей
    • Запись на сервис
    • Тест-драйв
    • Задать вопрос оператору
    • Контакты и адреса
    • О компании
    1. При нажатии на кнопку пользователю предлагается выбрать категорию: «Новые авто» / «Авто с пробегом».
    2. После выбора категории появляются кнопки для фильтрации: «Марка», «Модель», «Ценовой диапазон», «Тип кузова».
    3. После применения фильтров бот выводит список подходящих автомобилей в виде карусели карточек. Каждая карточка содержит: фото, марку и модель, цену.
    4. Под каждой карточкой есть кнопка «Хочу узнать больше». При нажатии на нее в административной панели создается «Заявка на консультацию» с привязкой к конкретному автомобилю и пользователю.
    1. Запускается пошаговый опросник для сбора данных:
        ◦ ФИО.
        ◦ Контактный телефон.
        ◦ Госномер или VIN-код автомобиля.
        ◦ Модель автомобиля.
        ◦ Тип необходимой услуги (выбор из списка, который редактируется в админ-панели).
        ◦ Желаемая дата и время.
    2. Интеграция с 1С (требует уточнения):
        ◦ Вариант А (Полная интеграция): Бот обращается к API 1С, получает список свободных слотов на выбранную дату и предлагает их пользователю. Выбор пользователя фиксируется.
        ◦ Вариант Б (Упрощенная интеграция): Пользователь указывает желаемые дату и время. Эти данные передаются в заявку. Менеджер вручную проверяет доступность в 1С и подтверждает запись при звонке клиенту.
    3. После заполнения всех полей в административной панели создается «Заявка на сервис».
    1. Пользователю предлагается выбрать модель из списка доступных для тест-драйва автомобилей (список управляется из админ-панели).
    2. Запускается анкета: ФИО, контактный телефон, желаемая дата.
    3. В административной панели создается «Заявка на тест-драйв».
    1. Пользователь вводит свой вопрос в свободной форме.
    2. Сообщение пользователя инициирует создание нового «Диалога» в административной панели.
    3. Бот отвечает: «Ваш вопрос отправлен оператору. Мы ответим вам прямо здесь, в чате, в ближайшее время».
    4. Все ответы менеджера из админ-панели приходят пользователю в этот же чат от имени бота.
    • Отображают информацию, которая полностью редактируется в административной панели.
    • Раздел «Контакты» должен содержать адреса, телефоны (кликабельные), ссылки на соцсети и кнопку для построения маршрута на карте.
2. Функциональные требования к административной панели (интерфейс для сотрудников)
    • Доступ к панели осуществляется через веб-браузер по логину и паролю.
    • Реализована система ролей (например, «Администратор», «Менеджер»).
    • Интерфейс должен быть интуитивно понятным и адаптивным для работы на ПК.
    • Единый реестр всех заявок (сервис, тест-драйв, консультация).
    • Возможность фильтрации и поиска заявок по типу, статусу («Новая», «В работе», «Завершено», «Отклонено»), дате, клиенту.
    • При клике на заявку открывается её детальная карточка со всей информацией, собранной ботом.
    • Менеджер может менять статус заявки и оставлять внутренние комментарии.
    • Интерфейс для обработки вопросов от пользователей, стилизованный под чат.
    • Список активных и завершенных диалогов.
    • Менеджер выбирает диалог и может писать ответ, который будет мгновенно отправлен пользователю в Telegram.
    • Возможность прикреплять файлы и изображения к ответам.
    • Интерфейс для добавления, редактирования и удаления автомобилей в каталоге.
    • Поля для заполнения: марка, модель, цена, категория (новый/с пробегом), описание, фото, тип кузова, статус «в наличии».
    • Возможность указать, доступен ли автомобиль для тест-драйва.
    • Редактор для всех текстовых сообщений бота: приветствие, тексты в разделах «О компании», «Контакты», автоответы, названия кнопок.
    • Управление списком услуг для записи на сервис.
    • Функционал для создания и отправки массовых сообщений всем пользователям бота.
    • Возможность прикрепить изображение и кнопки со ссылками.
    • Планирование отложенной отправки рассылки.
    • Список всех пользователей, которые взаимодействовали с ботом.
    • Просмотр истории заявок и диалогов конкретного пользователя.


