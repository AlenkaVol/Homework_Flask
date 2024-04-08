import requests

# добавляем нового пользователя
response = requests.post('http://127.0.0.1:5000/user',
                         json={"name": "Kevin", "password": "123456789"})
print(response.text)
print(response.status_code)

# # получаем пользователя по его id
# response = requests.get('http://127.0.0.1:5000/user/1')
# print(response.text)
# print(response.status_code)
#
# # меняем данные о пользователе
# response = requests.patch('http://127.0.0.1:5000/user/1',
#                           json={"password": "secret12345"})
# print(response.text)
# print(response.status_code)
#
# # удаляем пользователя
# response = requests.delete('http://127.0.0.1:5000/user/1')
# print(response.text)
# print(response.status_code)
#
#
# # добавляем новое объявление
# response = requests.post("http://localhost:5000/advertisement",
#                          json={"title": "Продам машину", "description": "Не бита, не крашена!", "owner": "1"})
# print(response.text)
# print(response.status_code)
#
# # получаем информацию об объявлении
# response = requests.get('http://localhost:5000/advertisement/1')
# print(response.text)
# print(response.status_code)
#
# # меняем данные в объявлении
# response = requests.patch('http://127.0.0.1:5000/advertisement/1',
#                           json={"description": "Срочно!"})
# print(response.text)
# print(response.status_code)
#
# # удаляем объявление
# response = requests.delete('http://127.0.0.1:5000/advertisement/1')
# print(response.text)
# print(response.status_code)


