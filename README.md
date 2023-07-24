# Telegram 提醒机器人

这是一个简单的Telegram机器人，可以帮助用户设置提醒。

## 功能

- 用户可以设置提醒的内容和时间。
- 用户可以查看所有未过期的提醒。
- 用户可以取消某个提醒或所有提醒。

## 如何使用

- 发送 `/start` 命令获取并保存你的chatID。
- 发送 `/text` 命令并按照提示输入提醒内容和时间。
- 发送 `/list` 命令查看所有未过期的提醒。
- 发送 `/cancel` 命令取消当前的提醒。也可以发送 `/cancel [提醒编号]` 取消指定编号的提醒，或发送 `/cancel all` 取消所有提醒。
- 发送 `/help` 命令获取操作说明。

## 安装和运行

1. 克隆这个仓库。
2. 安装依赖：`pip install python-telegram-bot apscheduler`
3. 将代码中的`[your bot token]`修改为你的Telegram bot token
4. 运行 `python "Telegram Reminder Bot.py"`

## 注意

这个项目是作为示例和学习用途创建的，可能不适合在生产环境中使用。



# Telegram Reminder Bot

This is a simple Telegram bot that can help users set reminders.

## Features

- Users can set the content and time of reminders.
- Users can view all unexpired reminders.
- Users can cancel a reminder or all reminders.

## How to use

- Send the `/start` command to get and save your chatID.
- Send the `/text` command and follow the prompts to enter the reminder content and time.
- Send the `/list` command to view all unexpired reminders.
- Send the `/cancel` command to cancel the current reminder. You can also send `/cancel [reminder number]` to cancel the specified reminder, or send `/cancel all` to cancel all reminders.
- Send the `/help` command for operating instructions.

## Installation and running

1. Clone this repository.
2. Install dependencies: `pip install python-telegram-bot apscheduler`
3. Replace `[your bot token]` in the code with your Telegram bot token
4. 4. Run `python "Telegram Reminder Bot.py"`

## Note

This project was created for demonstration and learning purposes and may not be suitable for use in a production environment.
