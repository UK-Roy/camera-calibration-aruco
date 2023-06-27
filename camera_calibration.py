"""
This code assumes that images used for calibration are of the same arUco marker board provided with code

"""
import cv2
from cv2 import aruco
import yaml
import numpy as np
import glob
from pathlib import Path
from tqdm import tqdm

def calib(path, yml_dir):
    # For validating results, show aruco board to camera.
    aruco_dict = aruco.getPredefinedDictionary( aruco.DICT_6X6_1000 )

    #Provide length of the marker's side
    markerLength = 3.75  # Here, measurement unit is centimetre.

    # Provide separation between markers
    markerSeparation = 0.5   # Here, measurement unit is centimetre.

    # create arUco board
    board = aruco.GridBoard((4, 5), markerLength, markerSeparation, aruco_dict)

    '''uncomment following block to draw and show the board'''
    #img = board.draw((864,1080))
    #cv2.imshow("aruco", img)

    arucoParams = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(aruco_dict, arucoParams)


    img_list = []
    calib_fnms = glob.glob(f'{path}/*.jpg')
    fns = list(calib_fnms)
    print('Using ...', end='')
    for idx, fn in enumerate(fns):
        print(idx, '', end='')
        img = cv2.imread(fn)
        img_list.append(img)
        h, w, c = img.shape
    print('Calibration images')

    counter, corners_list, id_list = [], [], []
    first = True

    for idx, im in enumerate(tqdm(img_list)):
        print(f"Calibrating on {idx} {fns[idx]}")
        img_gray = cv2.cvtColor(im,cv2.COLOR_RGB2GRAY)
        corners, ids, rejectedImgPoints = detector.detectMarkers(img_gray) #aruco.detectMarkers(, aruco_dict, parameters=arucoParams)
        if first:
            corners_list = corners
            id_list = ids
            first = False
        else:
            corners_list = np.vstack((corners_list, corners))
            id_list = np.vstack((id_list,ids))
        counter.append(len(ids))
    print('Found {} unique markers'.format(np.unique(ids)))

    counter = np.array(counter)
    print ("Calibrating camera .... Please wait...")
    #mat = np.zeros((3,3), float)
    ret, mtx, dist, rvecs, tvecs = aruco.calibrateCameraAruco(corners_list, id_list, counter, board, img_gray.shape, None, None )

    print("Camera matrix is \n", mtx, "\n And is stored in calibration.yaml file along with distortion coefficients : \n", dist)
    data = {'camera_matrix': np.asarray(mtx).tolist(), 'dist_coeff': np.asarray(dist).tolist()}
    
    with open(f"{yml_dir}/calibration.yaml", "w") as f:
        yaml.dump(data, f)

    cv2.destroyAllWindows()
