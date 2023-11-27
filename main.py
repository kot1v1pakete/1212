import random
import asyncio
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import FloodWaitError, ChatSendMediaForbiddenError

api_accounts = [
    {'api_id' : 26254782, 'api_hash' : '8a7e23f39450fba659bb190cf762d4f3', 'unread_count' : 1, 'delay' : 20},
    {'api_id': 26254782, 'api_hash': '8a7e23f39450fba659bb190cf762d4f3', 'unread_count': 1, 'delay': 10}
]

async def send_sequential_messages(client, dialog, messages, api_id, delay):
    try:
        for message in messages:
            await client.send_message(dialog.id, message=message, parse_mode='html')
            await asyncio.sleep(delay)
    except Exception as e:
        print(f'Error for account {api_id}: {e}')

async def respond_to_incoming_messages(client, messages_to_send, delay,api_id):
    while True:
        async for message in client.iter_messages('me'):  # Здесь 'me' означает, что мы получаем сообщения для собственного аккаунта бота.
            if message.is_private:  # Если сообщение из личного чата
                await send_sequential_messages(client, message, messages_to_send, api_id, delay)
            elif message.is_group:  # Если сообщение из группового чата
                await send_sequential_messages(client, message, messages_to_send, api_id, delay)
        await asyncio.sleep(60)

async def send_messages(account, messages_to_send):
    api_id = account['api_id']
    api_hash = account['api_hash']
    unread_count = account['unread_count']
    delay = account['delay']
    async with TelegramClient(f'session_{api_id}', api_id, api_hash) as client:
        while True:
            try:
                async for dialog in client.iter_dialogs():
                    if dialog.is_group and dialog.unread_count > unread_count:
                        await send_sequential_messages(client, dialog, messages_to_send, api_id, delay)
            except FloodWaitError as e:
                print(f'Flood wait error for account {api_id}: waiting {e.seconds} seconds')
                await asyncio.sleep(e.seconds)
            except Exception as e:
                print(f'Error for account {api_id}: {e}')
            await respond_to_incoming_messages(client, messages_to_send, 20)

async def run_clients():
    tasks = []
    for account in api_accounts:
        messages_to_send_random = ['🔥🔥🔥ВЗАИМНАЯ ПОДПИСКА🔥🔥🔥\n@lesenka_piar',
            '☠️☠️☠️ ЗАХОДИ ЕСЛИ НУЖЕН АКТИВ ☠️☠️☠️ \n@lesenka_piar"',
            '🔔АКТИВНЫЙ ПИАР ЧАТ \nБЕЗ ЗАПРЕТОВ, ТАЙМЕРОВ И ОГРАНИЧЕНИЙ 🔔 \n✅(1.400 человек)  \n@lesenka_piar']  # Твои сообщения здесь
        tasks.append(send_messages(account, messages_to_send_random))
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_clients())