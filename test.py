import requests

BASE = 'http://127.0.0.1:5000/'

# data = [
#     {'likes': 100, 'name' : 'Lecture 1: Algorithmic Thinking', 'views' : 100},
#     {'likes': 100, 'name' : 'Unlocking your CPU cores in Python', 'views' : 100},
#     {'likes': 100, 'name' : 'What To Learn After Python', 'views' : 100}
# ]

# for i in range(len(data)):
#     response = requests.put(BASE + 'video/' + str(3+i), data[i])
#     print(response.json())

# input()
# response = requests.delete(BASE + 'video/0')
# print(response)
# input()

# response = requests.patch(BASE + 'video/2', {'views' : 102, 'likes' : 101})
# print(response.json())

response = requests.delete(BASE + 'video/1')
print(response.json())
