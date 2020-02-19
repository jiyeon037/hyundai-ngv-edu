import requests
import datetime
import os
import time

url_data = 'http://ec2-18-217-158-122.us-east-2.compute.amazonaws.com:5000/data'
url_image = 'http://ec2-18-217-158-122.us-east-2.compute.amazonaws.com:5000/image'
#url_data = 'http://127.0.0.1:5000/data'
#url_image = 'http://127.0.0.1:5000/image'


thisDirectory = os.path.dirname(os.path.realpath(__file__))

def createFolder(directory): 
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory.', + directory)

last_img_num = 0
createFolder(thisDirectory)
while True:
    file_list = os.listdir(thisDirectory + '\wetroad')
    file_list.sort()
    if len(file_list) != last_img_num :
        last_img_num = len(file_list)
        file_name = thisDirectory + '\wetroad\\' + file_list[-1]
        
        print(file_list)
        print("CHANGE")

        files = {'file': open(file_name, 'rb')}
        res = requests.post(url_image, files=files)
        print("post : ", res)
