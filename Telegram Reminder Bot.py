from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

# Global dictionary to keep track of reminders per user
reminders = {}

# Scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# States
TEXT, TIME = range(2)

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    context.user_data['chat_id'] = user.id
    update.message.reply_text(f'你的chatID是： {user.id}\n请输入 /text 配置提示内容')

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text('操作说明：\n'
                              '/start - 获取并保存你的chatID\n'
                              '/text - 配置提醒内容\n'
                              '/cancel - 取消当前提醒或配置\n'
                              '/cancel [提醒编号] - 取消指定编号的提醒\n'
                              '/cancel all - 取消所有提醒\n'
                              '/list - 查看所有未过期的提醒\n'
                              '/help - 获取操作说明')


def text(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('请输入提醒内容')
    return TEXT

def text_message(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    context.user_data['text'] = text
    update.message.reply_text(f'已保存提醒内容： {text}\n请输入提醒时间，格式为 HH:MM，例如： {datetime.now().strftime("%H:%M")}\n你可以输入 /cancel 来取消这次配置')
    return TIME

def time_message(update: Update, context: CallbackContext) -> int:
    time = update.message.text
    context.user_data['time'] = time
    reminder_id = str(len(reminders.get(context.user_data['chat_id'], {})) + 1)
    context.user_data['id'] = reminder_id
    if context.user_data['chat_id'] not in reminders:
        reminders[context.user_data['chat_id']] = {}
    reminders[context.user_data['chat_id']][reminder_id] = context.user_data.copy()

    # Calculate the time difference till the reminder
    now = datetime.now()
    remind_time = datetime.strptime(time, '%H:%M')
    remind_time = datetime.combine(now.date(), remind_time.time())
    if remind_time < now:
        remind_time += timedelta(days=1)

    # Schedule the reminder
    scheduler.add_job(reminder, 'date', run_date=remind_time, args=(context, reminders[context.user_data['chat_id']][reminder_id],))

    update.message.reply_text(f'已保存提醒时间： {time}\n提醒编号： {reminder_id}\n你可以输入 /list 来查看所有未过期的提醒，或输入 /cancel {reminder_id} 或 /cancel all 来取消提醒')
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> None:
    args = context.args
    if args:
        if args[0] == 'all':
            reminders[context.user_data['chat_id']].clear()
            for job in scheduler.get_jobs():
                if job.args[1]['chat_id'] == context.user_data['chat_id']:
                    job.remove()
            update.message.reply_text('已取消所有提醒')
        elif args[0] in reminders[context.user_data['chat_id']]:
            del reminders[context.user_data['chat_id']][args[0]]
            for job in scheduler.get_jobs():
                if job.args[1]['id'] == args[0] and job.args[1]['chat_id'] == context.user_data['chat_id']:
                    job.remove()
            update.message.reply_text(f'已取消提醒 {args[0]}')
        else:
            update.message.reply_text('未知的提醒编号')
    else:
        if 'id' in context.user_data:
            del reminders[context.user_data['chat_id']][context.user_data['id']]
            for job in scheduler.get_jobs():
                if job.args[1]['id'] == context.user_data['id'] and job.args[1]['chat_id'] == context.user_data['chat_id']:
                    job.remove()
        update.message.reply_text('已取消当前提醒')
    return ConversationHandler.END

def cancel_conversation(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('已取消当前提醒配置')
    return ConversationHandler.END

def list_reminders(update: Update, context: CallbackContext) -> None:
    user_reminders = reminders.get(context.user_data['chat_id'], {})
    if user_reminders:
        message = ''
        for id, reminder in user_reminders.items():
            message += f'提醒编号： {id}\n提醒内容： {reminder["text"]}\n提醒时间： {reminder["time"]}\n\n'
        update.message.reply_text(message)
    else:
        update.message.reply_text('没有未过期的提醒')

def reminder(context: CallbackContext, user_data):
    context.bot.send_message(chat_id=user_data['chat_id'], text=user_data['text'])
    del reminders[user_data['chat_id']][user_data['id']]

def main() -> None:
    updater = Updater(token="[your bot token]", use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('text', text)],
        states={
            TEXT: [MessageHandler(Filters.text & ~Filters.command, text_message)],
            TIME: [MessageHandler(Filters.text & ~Filters.command, time_message)],
        },
        fallbacks=[CommandHandler('cancel', cancel_conversation)],
    )

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CommandHandler("cancel", cancel))
    dispatcher.add_handler(CommandHandler("list", list_reminders))
    dispatcher.add_handler(CommandHandler("help", help_command))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
