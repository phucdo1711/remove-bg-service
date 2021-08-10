import io
import os
import re
import sys

import torch

from . import utils
from .transformer_net import TransformerNet
from torchvision import transforms


models_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../models")
models_path = {
    'candy': os.path.join(models_dir, 'candy.pth'),
    'mosaic': os.path.join(models_dir, 'mosaic.pth'),
    # 'starry-night': os.path.join(models_dir, 'starry-night.pth'),
    'udnie': os.path.join(models_dir, 'udnie.pth'),
    'rain-princess': os.path.join(models_dir, 'rain_princess.pth'),
    'dog': os.path.join(models_dir, 'dog.pth'),
}

def stylize(image_data, model, content_scale = None):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    with torch.no_grad():
        image = io.BytesIO(image_data)

        content_image = utils.load_image(image, scale=content_scale)
        content_transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Lambda(lambda x: x.mul(255))
        ])
        content_image = content_transform(content_image)
        content_image = content_image.unsqueeze(0).to(device)
        print('has content_image =====')

        is_cuda = torch.cuda.is_available()
        print('is_cuda', is_cuda)
        
        with torch.no_grad():
            style_model = TransformerNet()
            state_dict = torch.load(models_path[model])
            print('loaded model ====')
            # remove saved deprecated running_* keys in InstanceNorm from the checkpoint
            for k in list(state_dict.keys()):
                if re.search(r'in\d+\.running_(mean|var)$', k):
                    del state_dict[k]
            style_model.load_state_dict(state_dict)
            style_model.to(device)
            output = style_model(content_image).cpu()
        
        try: 
            bio = io.BytesIO()
            utils.save_image(bio, output[0])
        except: 
            print("Unexpected error:", sys.exc_info())
            raise
        
        
        del style_model, output
        # torch.cuda.empty_cache()
        # print(bio.getbuffer())
        return bio.getbuffer()

