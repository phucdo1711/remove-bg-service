

import os
import cv2
import torch
import numpy as np
from models import ResnetGenerator
import argparse
from utils import Preprocess


parser = argparse.ArgumentParser()
parser.add_argument('--photo_path', type=str, help='input photo path')
parser.add_argument('--save_path', type=str, help='cartoon save path')
args = parser.parse_args()

os.makedirs(os.path.dirname(args.save_path), exist_ok=True)

class Photo2Cartoon:
    def __init__(self):
        self.pre = Preprocess()
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
       

    def inference(self, img):
        # face alignment and segmentation
        face_rgba = self.pre.process(img)
        if face_rgba is None:
            print('[Step2: face detect] can not detect face!!!')
            return None
        width = 256 #face_rgba.shape[1]
        self.net = ResnetGenerator(ngf=32, img_size=width, light=True).to(self.device)
        model_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'./models/photo2cartoon_weights.pt')
        
        assert os.path.exists(model_path), "[Step1: load weights] Can not find 'photo2cartoon_weights.pt' in folder 'models!!!'"
        params = torch.load(model_path, map_location=self.device)
        self.net.load_state_dict(params['genA2B'])
        print('[Step1: load weights] success!')
        
        # print('[Step2: face detect] success!', width, height )
        face_rgba = cv2.resize(face_rgba, (width, width), interpolation=cv2.INTER_AREA)
        face = face_rgba[:, :, :3].copy()
        mask = face_rgba[:, :, 3][:, :, np.newaxis].copy() / 255.
        face = (face*mask + (1-mask)*255) / 127.5 - 1

        face = np.transpose(face[np.newaxis, :, :, :], (0, 3, 1, 2)).astype(np.float32)
        face = torch.from_numpy(face).to(self.device)

        # inference
        with torch.no_grad():
            cartoon = self.net(face)[0][0]

        # post-process
        cartoon = np.transpose(cartoon.cpu().numpy(), (1, 2, 0))
        cartoon = (cartoon + 1) * 127.5
        cartoon = (cartoon * mask + 255 * (1 - mask)).astype(np.uint8)
        cartoon = cv2.cvtColor(cartoon, cv2.COLOR_RGB2BGR)
        print('[Step3: photo to cartoon] success!')
        return cartoon


if __name__ == '__main__':
    print(os.path.exists(args.photo_path))
    img = cv2.imread(args.photo_path, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    c2p = Photo2Cartoon()
    cartoon = c2p.inference(img)
    if cartoon is not None:
        cv2.imwrite(args.save_path, cartoon)
        print('Cartoon portrait has been saved successfully!')
