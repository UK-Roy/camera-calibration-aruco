import cv2
import requests
import numpy as np
import os

def take_images(url, path):
    isExist = os.path.exists(path)
    if not isExist:
    # Create a new directory because it does not exist
        os.makedirs(path)
        print("The new directory is created!")

    address = f"{url}/shot.jpg"
    print(f"Your camera ip is: {address}")
    
    count = 0
    while True:
        RawData = requests.get(address, verify=False)
        One_D_Arry = np.array(bytearray(RawData.content),dtype = np.uint8)
        img = cv2.imdecode(One_D_Arry, -1)
        file_name = f"{path}/{str(count)}.jpg"

        cv2.imshow("window", img)

        if cv2.waitKey(5) & 0xFF == ord('c'):
            cv2.imwrite(file_name, img)
            cv2.imshow("window", img)
            count += 1
            
            if cv2.waitKey(0) & 0xFF == ord('q'):
                break