import threading
import random
import aminofix
import time
from gtts import gTTS
from util import *

# aminofix кал

methods = []; userMessages = []; admins = [100, 101]
client = aminofix.Client()
client.login(email="зеви", password="кринж")
sub_client = aminofix.SubClient(comId="141660670", profile=client.profile)
print(f"Я щас на акке {sub_client.profile.nickname}")

def reload_socket():
    client.close()
    client.run_amino_socket()

def on_message(data: aminofix.objects.Event):

    ndcId = data.comId
    chatId = data.message.chatId
    nickname = data.message.author.nickname
    content = data.message.content
    id = data.message.messageId
    userId = data.message.author.userId
    time = data.json["chatMessage"]["createdTime"]

    #Castle of the DeКринж спасибо за критику но твою мамашу это не воскресит

    userMessages.append(time); userMessages.append(userId)

    # print(nickname, content, data.message.type, userId, ndcId)

    if userMessages[0] == time and userMessages.count(userId) >= 3:
        sub_client.ban(userId, "рейд")
        sub_client.kick(userId, chatId, False)
        userMessages.clear()
        for messageId in sub_client.get_chat_messages(chatId=chatId, size=count).messageId:
            threading.Thread(target=sub_client.delete_message, args=(chatId, messageId, True, "какой-то ебанок рейдер")).start()

    elif userMessages[0] != time and userMessages.count(userId) <= 3 and len(userMessages) == 4:
        userMessages.clear()

    if data.message.type != 0 and content != None:
        sub_client.kick(userId, chatId, False)

    if "t.me/" in content:
        sub_client.send_message(message="реклама тг канала! ты будешь забанен. ты не понял? ЗАБАНЕН", chatId=chatId)
        sub_client.ban(userId, "Реклама тг канала")
        sub_client.kick(userId, chatId, False)

    if content.lower().startswith("бан"):
        if sub_client.get_user_info(userId).role in admins:
            content = content.split(); bannedUserId = sub_client.get_from_code(content[1]).objectId
            reason = ' '.join(content[2:]); bannedNickname = sub_client.get_user_info(bannedUserId).nickname
            sub_client.ban(userId=bannedUserId, reason=reason)
            sub_client.send_message(message=f"готово! пользователь {bannedNickname} забанен!", chatId=chatId, replyTo=id)

        else:
            sub_client.send_message(message="ты не можешь использовать эту команду, потому что ты не админ!", chatId=chatId, replyTo=id)

    if content.lower().startswith("разбан"):
        if sub_client.get_user_info(userId).role in admins:
            content = content.split(); unBannedUserId = sub_client.get_from_code(content[1]).objectId
            reason = ' '.join(content[2:]); unBannedNickname = sub_client.get_user_info(unBannedUserId).nickname
            sub_client.unban(userId=unBannedUserId, reason=reason)
            sub_client.send_message(message=f"готово! пользователь {unBannedNickname} разбанен!", chatId=chatId, replyTo=id)

        else:
            sub_client.send_message(message="ты не можешь использовать эту команду, потому что ты не админ!", chatId=chatId, replyTo=id)

    if "http://aminoapps.com/" in content:

        content = content.split(); link = None;
        for i in content:
            if "http://aminoapps.com/" in i:
                link = i; break

        if "/p/" in link:
            if client.get_from_code(link).comIdPost != ndcId:
                sub_client.send_message(message="реклама поста из другого соо! ты будешь забанен. ты не понял? ЗАБАНЕН", chatId=chatId)
                sub_client.ban(userId, "Реклама чего-то из амино")
                sub_client.kick(userId, chatId, False)
        elif "/c/" in link:
            if client.get_from_code(link).comId != ndcId:
                sub_client.send_message(message="реклама другого соо! ты будешь забанен. ты не понял? ЗАБАНЕН", chatId=chatId)
                sub_client.ban(userId, "Реклама чего-то из амино")
                sub_client.kick(userId, chatId, False)


    # if content.lower() == ".проверь ботов в соо":


    if content.lower().startswith(".гс"):
        content = content.split(); text = ' '.join(content[1:])
        voice = gTTS(text=text, lang="ru"); voice.save("гс.mp3")
        with open("гс.mp3", "rb") as vm:
            sub_client.send_message(chatId=chatId, file=vm, fileType="audio")


    if content.lower().startswith(".любовь"):
        content = content.split(); chance = random.randint(0, 100)
        sub_client.send_message(message=f"любовь между {nickname} и {content[1]} равна {chance}%", chatId=chatId, replyTo=id)


    if content.lower().startswith(".команды"):
        print(sub_client.get_user_info(userId).role)
        if sub_client.get_user_info(userId).role == 0:
            sub_client.send_message(message=commandsText, chatId=chatId, replyTo=id)
        elif sub_client.get_user_info(userId).role in admins:
            sub_client.send_message(message=adminCommandsText, chatId=chatId, replyTo=id)

    if content.lower().startswith(".флуд"):
        count = int(content.split()[1])
        print(count)
        sub_client.send_message(message='щас зафлудим чат', messageType=107, chatId=chatId)
        for i in range(count):
            threading.Thread(target=sub_client.send_message, args=(chatId, f"флудю для проверки ацтаньте {i}")).start()
            sub_client.send_message(chatId, f"флудю для проверки ацтаньте {i}")


    if content.lower().startswith(".почисти"):
        count = int(content.split()[1])
        print(count)
        sub_client.send_message(message='сек', chatId=chatId)

        for messageId in sub_client.get_chat_messages(chatId=chatId, size=count).messageId:
            threading.Thread(target=sub_client.delete_message, args=(chatId, messageId, True, "Повелитель приказал почистить, а я за снюс готов на всё")).start()

    if content.lower() == ".угадай число":
        isWin = False; number = random.randint(0, 10)
        sub_client.send_message(message=randomNumberText, chatId=chatId)
        print(number)

        # ЭТА ХУЙНЯ НЕ РАБОТАЕТ

        while isWin == False:
            user_variant = sub_client.get_chat_messages(chatId=chatId, size=1).content[0]
            print(user_variant)
            if int(user_variant) == number:
                sub_client.send_message(message=f"вы угадали число!! это было число {number}", messageType=107, chatId=chatId)
                isWin = True

    if content.lower() == ".info":
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
