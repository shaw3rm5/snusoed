import threading
import random
import aminofix
import time
from variables import *

# aminofix кал

methods = []
client = aminofix.Client()
client.login(email="email", password="password")
sub_client = aminofix.SubClient(comId="141660670", profile=client.profile)
print(f"Я щас на акке {sub_client.profile.nickname}")

def reload_socket():
    client.close()
    client.start()


def check_raid():
    pass


def on_message(data: aminofix.objects.Event):

    chatId = data.message.chatId
    nickname = data.message.author.nickname
    content = data.message.content
    id = data.message.messageId
    userId: str = data.message.author.userId


    if content.lower().startswith("!флуд"):
        count = int(content[6:9]); i = 0
        print(count)
        sub_client.send_message(message='щас зафлудим чат', messageType=107, chatId=chatId)
        for i in range(count):
            # threading.Thread(target=sub_client.send_message, args=(chatId, f"флудю для проверки ацтаньте {i}")).start()
            sub_client.send_message(chatId, f"флудю для проверки ацтаньте {i}")


    if content.lower().startswith("!почисти"):
        count = int(content[9:12])
        print(count)
        sub_client.send_message(message='сек', chatId=chatId)

        for message_id in sub_client.get_chat_messages(chatId=data.message.chatId, size=count).messageId:
            threading.Thread(target=sub_client.delete_message, args=(chatId, message_id, True, "Повелитель приказал почистить, а я за снюс готов на всё")).start()

    if content.lower().startswith("!угадай число"):
        isWin = False; number = random.randint(0, 10)
        sub_client.send_message(message=random_number_text, chatId=chatId)
        print(number)

        while isWin == False:
            user_variant = sub_client.get_chat_messages(chatId=chatId, size=1).content[0]
            print(user_variant)
            if int(user_variant) == number:
                sub_client.send_message(message=f"вы угадали число!! это было число {number}", messageType=107, chatId=chatId)
                isWin = True

    if content.lower().startswith("!info"):
        message = info_text(
            nickname=nickname,
            uid=userId,
            reputation=sub_client.get_user_info(userId=userId).reputation
        )
        sub_client.send_message(message=message, messageType=0, chatId=chatId, replyTo=id)

    if content.lower().startswith("!пососи"):
        sub_client.send_message(message="соси", messageType=0, chatId=chatId, replyTo=id)


for x in client.chat_methods:
    methods.append(client.event(client.chat_methods[x].__name__)(on_message))
