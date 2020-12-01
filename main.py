import time
import requests

def write(users):

    print(">> Начата запись в файл.")

    # Запись в файл
    with open("C:/Users/home/Desktop/py_maga/LR6/info.txt", "w", encoding='utf-8') as file:
        # Для каждого списка в users
        for l1 in users:
            row=""
            # Для каждого значения в списке l1
            for value in range(len(l1)):
                row += str(l1[value])
                if value%2 != 0:
                    row+="| "
            file.writelines(row + "\n")

    print(">> Запись в файл завершена.")

def func():
    id = input("\n________________________\n>> Укажите VK id: ")
    if len(id) <= 0:
        print(">> Неверный ID!")
        func()
    keys = ["id", "first_name", "last_name", "city"]
    users = []
    # access_token
    token = 'тут токен'
    # Указанный пользователь
    id = MainUser(id, keys, users, token)
    print(">> Поиск друзей.")
    UserFriends(id, keys, users, token)
    # Запись в файл
    write(users)
    
def MainUser(id, keys, users, token):
    getUser = f"https://api.vk.com/method/users.get?access_token={token}&v=5.126&user_ids={id}&fields=city"
    # Получаем объект response
    response = requests.get(getUser)
    # Статус запроса
    Code(response)
    # Декодирование в JSON по ключу 'response'
    user = response.json()['response']
    # Вывод имени пользователя на экран
    print(">> Выбран пользователь: "+user[0].get('first_name')+" "+user[0].get('last_name'))
    # Получение id пользователя
    ID = user[0].get('id')
    # Добавление пустого списка в конец списка users
    users.append([])

    # Для каждого значения в списке keys
    for k in range(len(keys)):
        # Ключ + :
        users[0].append(keys[k]+": ")
        # Для города
        if k == len(keys)-1:
            try:          
                # Если город указан, то из словаря города получаем названеи города по ключу 'title'
                users[0].append(user[0][keys[k]]['title'])
            except:
                users[0].append("<None>")
        else:
            try:
                users[0].append(user[0][keys[k]])
            except:
                users[0].append("<None>")

    # Возвращаем ID в числовом виде
    return ID

def UserFriends(id, keys, users, token):
    getFriendsID = f"https://api.vk.com/method/friends.get?access_token={token}&v=5.126&user_id={id}"
    # Получаем объект response
    response = requests.get(getFriendsID)
    # Статус запроса
    Code(response)
    # Число друзей пользователя (Декодирование в JSON по ключу 'response', 'count')
    num = response.json()['response']['count']
    print(">> Число друзей: ", num)
    # Пустой список
    us1=[]
    # Смещение, необходимое для выборки определенного подмножества друзей
    offset=0

    while offset < num:
        getFriends = f"https://api.vk.com/method/friends.get?access_token={token}&v=5.126&user_id={id}&count=5000&offset={offset}&fields=city"
        response = requests.get(getFriends)
        # Декодирование в JSON по ключу 'response', 'items'
        JsonData = response.json()['response']['items']
        offset+=5000
        # Дополняем список элементами из указанного объекта
        us1.extend(JsonData)
        time.sleep(0.5)

    # Для каждого словаря из списка us1
    for user in range(len(us1)):
        # Добавление пустого списка в конец списка users
        users.append([])
        # Для каждого значения в списке keys
        for k in range(len(keys)):
            # Ключ + :
            users[user+1].append(keys[k]+": ")
            if k == len(keys)-1:
                try:
                    # Если город указан, то из словаря города получаем названеи города по ключу 'title'
                    users[user+1].append(us1[user][keys[k]]['title'])
                except:
                    users[user+1].append("<None>")
            else:
                try:
                    users[user+1].append(us1[user][keys[k]])
                except:
                    users[user+1].append("<None>")

def Code(response):
    # 200 OK
    if response.status_code != 200:
        print(">> Запрос не был выполнен ( код "+ response.status_code+ ")! \n----------------")
        func()
    else:
        print(">> Запрос выполнен успешно ( код ", response.status_code, "). \n----------------")
    try:
        # Декодирование в JSON по ключу 'response'
        response.json()['response']
    except:
        print(">> Ошибка: ", response.json()['error']['error_msg'])
        func()
    if len(response.json()['response']) <= 0:
        print(">> Error!")
        func()

if __name__ == "__main__":
    try:
        func()
    except KeyboardInterrupt:
        print("\n>> Программа остановлена!")
    except:
        print(">> Непредвиденная ошибка!")