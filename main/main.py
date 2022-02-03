import threading
import random
import aminofix
import time
from util import *

# aminofix кал

methods = []; userMessages = []
client = aminofix.Client()
client.login(email="schawerm1234@bk.ru", password="Apkhgvek@1542")
sub_client = aminofix.SubClient(comId="141660670", profile=client.profile)
print(f"Я щас на акке {sub_client.profile.nickname}")

def reload_socket():
    client.close()
    client.run_amino_socket()

def on_message(data: aminofix.objects.Event):

    chatId = data.message.chatId
    nickname = data.message.author.nickname
    content = data.message.content
    id = data.message.messageId
    userId = data.message.author.userId
    time = data.json["chatMessage"]["createdTime"]

    userMessages.append(time); userMessages.append(userId)

    print(nickname, content, data.message.type, userId, userMessages)

    if userMessages[0] == time and userMessages.count(userId) >= 3:
        sub_client.ban(userId, "рейд")
        sub_client.kick(userId, chatId, False)
        userMessages.clear()
        print("обрати на меня внимание!!!!!!!!", userMessages)

    elif userMessages[0] != time and userMessages.count(userId) <= 3 and len(userMessages) == 4:
        userMessages.clear()

    if data.message.type != 0 and content != None:
        sub_client.kick(userId, chatId, False)

    if "t.me/" in content or "@" in content:
        sub_client.send_message(message="реклама тг канала! ты будешь забанен. ты не понял? ЗАБАНЕН", chatId=chatId)
        sub_client.ban(userId, "Реклама тг канала")
        sub_client.kick(userId, chatId, False)

    if "http://aminoapps.com/" in content:
        sub_client.send_message(message="реклама чего-то! ты будешь забанен. ты не понял? ЗАБАНЕН", chatId=chatId)
        sub_client.ban(userId, "Реклама чего-то из амино")
        sub_client.kick(userId, chatId, False)



    if content.lower().startswith("!флуд"):
        count = int(content.split()[1])
        print(count)
        sub_client.send_message(message='щас зафлудим чат', messageType=107, chatId=chatId)
        for i in range(count):
            # threading.Thread(target=sub_client.send_message, args=(chatId, f"флудю для проверки ацтаньте {i}")).start()
            sub_client.send_message(chatId, f"флудю для проверки ацтаньте {i}")


    if content.lower().startswith("!почисти"):
        count = int(content.split()[1])
        print(count)
        sub_client.send_message(message='сек', chatId=chatId)

        for messageId in sub_client.get_chat_messages(chatId=chatId, size=count).messageId:
            threading.Thread(target=sub_client.delete_message, args=(chatId, messageId, True, "Повелитель приказал почистить, а я за снюс готов на всё")).start()

    if content.lower() == "!угадай число":
        isWin = False; number = random.randint(0, 10)
        sub_client.send_message(message=randomNumberText, chatId=chatId)
        print(number)

        while isWin == False:
            user_variant = sub_client.get_chat_messages(chatId=chatId, size=1).content[0]
            print(user_variant)
            if int(user_variant) == number:
                sub_client.send_message(message=f"вы угадали число!! это было число {number}", messageType=107, chatId=chatId)
                isWin = True

    if content.lower() == "!info":
        message = infoText(
            nickname=nickname,
            uid=userId,
            reputation=sub_client.get_user_info(userId=userId).reputation
        )
        sub_client.send_message(message=message, messageType=0, chatId=chatId, replyTo=id)

    if content.lower() == "чек":
        sub_client.send_message(message="privet", chatId=chatId, replyTo=id)


for x in client.chat_methods:
    methods.append(client.event(client.chat_methods[x].__name__)(on_message))

while True:
    threading.Thread(target=reload_socket).start()
    time.sleep(300)
