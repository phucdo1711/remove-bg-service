import io
import os
import sys

import torch
from torch.autograd import Variable

from . import utils
from .transformer_net import TransformerNet


models_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../models")
models_path = {
    'candy': os.path.join(models_dir, 'candy.pth'),
    'mosaic': os.path.join(models_dir, 'mosaic.pth'),
    'starry-night': os.path.join(models_dir, 'starry-night.pth'),
    'udnie': os.path.join(models_dir, 'udnie.pth'),
}

def check_paths(args):
    try:
        if not os.path.exists(args.vgg_model_dir):
            os.makedirs(args.vgg_model_dir)
        if not os.path.exists(args.save_model_dir):
            os.makedirs(args.save_model_dir)
    except OSError as e:
        print(e)
        sys.exit(1)


def stylize(image_data, model, content_scale = None):
    image = io.BytesIO(image_data)

    content_image = utils.tensor_load_rgbimage(image, scale=content_scale)
    content_image = content_image.unsqueeze(0)
    print('has content_image =====')

    is_cuda = False # torch.cuda.is_available()
    print('is_cuda', is_cuda)
    if is_cuda:
        content_image = content_image.cuda()
    print('loaded cuda =====')
   
    content_image = Variable(utils.preprocess_batch(content_image), volatile=True)
    style_model = TransformerNet()
    
    if is_cuda:
        style_model.load_state_dict(torch.load(models_path[model]))
        style_model.to(torch.device("cuda"))
    else: 
        style_model.load_state_dict(torch.load(models_path[model], map_location="cpu"))
    print('load model done =====')

    try: 
        output = style_model(content_image)
    except: 
        print("Unexpected error:", sys.exc_info()[0])
        raise
    print('output done =====')
        
    img = utils.tensor_save_bgrimage(output.data[0], is_cuda)
    
    bio = io.BytesIO()
    img.save(bio, "PNG")
    # print(bio.getbuffer())
    return bio.getbuffer()

