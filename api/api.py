import base64
import os
from io import BytesIO
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from skimage import color
import skimage
import torch
import torchvision.transforms as T
from model_components.model_arch import eccv16, postprocess_tens, preprocess_img, load_img
from model_components.util_classes import CIELAB, AnnealedMeanDecodeQ, GetClassWeights, RebalanceLoss, SoftEncoder

app = Flask(__name__)
CORS(app)


DEFAULT_CIELAB = CIELAB()
decode_q = AnnealedMeanDecodeQ(DEFAULT_CIELAB, T=0.4)
soft_encoder = SoftEncoder()
get_class_weights = GetClassWeights()
rebalance_loss = RebalanceLoss.apply

preprocess = T.Compose([
    T.Resize(256),
    T.CenterCrop(256),
    T.ToTensor()
])

checkpoint = torch.load(
    os.getcwd() + "\model_components\model_weights.pth")

colorizer_eccv16 = eccv16(pretrained=False)
colorizer_eccv16.load_state_dict(checkpoint['model_state_dict'])


def separate_data(image):
    # RGB to Lab color space
    img_lab_orig = color.rgb2lab(image.numpy().transpose((1, 2, 0)))
    # Get L channel
    L_orig = img_lab_orig[:, :, 0]
    # Get ab channels
    ab_orig = img_lab_orig[:, :, 1:]  # (256, 256, 2)
    # Convert back to tensor
    X_train = torch.Tensor(L_orig)[None, None, :, :]  # [1, 1, 256, 256]
    y_train = torch.Tensor(ab_orig.transpose((2, 0, 1)))[
        None, :, :, :]  # [1, 2, 256, 256]
    Z_train = torch.Tensor(soft_encoder(ab_orig).transpose(
        [2, 0, 1]).copy())  # [313, 256, 256]
    return X_train, y_train, Z_train


@app.route('/colourise', methods=['POST'])
def colourise_image():
    input_image = request.files['image']
    img = load_img(input_image)
    # Separate L and ab channels
    # x = preprocess(img)
    # X_input, y_input, _ = separate_data(x)
    X_orig, y_orig, X_input = preprocess_img(img)
    # Predict the result
    y_pred = colorizer_eccv16(X_input)
    color_weights = get_class_weights(y_orig)
    y_pred = rebalance_loss(y_pred, color_weights)
    y_pred_decoded = decode_q(y_pred)
    colourised_image = postprocess_tens(X_orig, y_pred_decoded)
    # data = base64.b64encode(stream_image).decode()
    # convert image to bytes
    with BytesIO() as output_bytes:
        PIL_image = Image.fromarray(skimage.img_as_ubyte(colourised_image))
        # Note JPG is not a vaild type here
        PIL_image.save(output_bytes, 'JPEG')
        bytes_data = output_bytes.getvalue()

    # encode bytes to base64 string
    base64_str = str(base64.b64encode(bytes_data), 'utf-8')
    return jsonify({'msg': 'success', 'img': base64_str})
