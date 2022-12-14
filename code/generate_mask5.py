from email.mime import image
import os
import cv2
import numpy as np
import tqdm
threshold = 5
folder = 'mask' + str(threshold)
def cal_mask(img, gt):
    kernel = np.ones((2, 2), np.uint8)
    # mask = cv2.erode(np.uint8(mask),  kernel, iterations=2)
    # threshold = 25
    mask = np.abs(img.astype(np.float32) - gt.astype(np.float32))
    # mask = np.mean(mask, axis=-1)   
    mask = np.greater(mask, threshold).astype(np.uint8)
    mask = (1 - mask) * 255
    # mask = cv2.erode(np.uint8(mask),  kernel, iterations=1)
    return np.expand_dims(np.uint8(mask),axis=2).repeat(3,axis=2)

data_root = "/home/shb/experiment/OCR/dataset/classone"
for img_dir in os.listdir(data_root):
    data_path = os.path.join(data_root, img_dir)
    image_list = [os.path.join(data_path+"/images", img_path) for img_path in os.listdir(data_path+"/images")]
    new_dir =  os.path.join(data_root, img_dir,folder)

    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    print(img_dir)
    for img_path in tqdm.tqdm(image_list):
        if os.path.exists(img_path.replace("images",folder)[:-4] + '.jpg'):
            continue
        input_img = cv2.imread(img_path)
        gt = cv2.imread(img_path.replace("images","gts")[:-4] + '.jpg')
        mask = cal_mask(np.array(input_img), np.array(gt))
        cv2.imwrite(img_path.replace("images",folder)[:-4] + '.jpg', mask)

data_path = "/home/shb/experiment/OCR/dataset/dehw_train_dataset"
image_list = [os.path.join(data_path+"/images", img_path) for img_path in os.listdir(data_path+"/images")]
new_dir =  os.path.join(data_path,folder)
if not os.path.exists(new_dir):
    os.mkdir(new_dir)
for img_path in tqdm.tqdm(image_list):
    if os.path.exists(img_path.replace("images",folder)[:-4] + '.jpg'):
            continue
    input_img = cv2.imread(img_path)
    # gt = cv2.imread(img_path.replace("images","gts")[:-4] + '.jpg')
    gt = cv2.imread(img_path.replace("images","gts")[:-4] + '.png')
    mask = cal_mask(np.array(input_img), np.array(gt))
    cv2.imwrite(img_path.replace("images",folder)[:-4] + '.jpg', mask)
