import numpy as np
import torch
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter
from Model import Model1, Model2


def predict_image(img, model):
    batch = img.unsqueeze(0)
    _, preds = torch.max(model(batch), dim=1)
    return preds[0].item()


def imshow(img, mean=0.1307, std=0.3081):
    img = img / std + mean
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)), cmap="gray")
    plt.show()


# Converting image to MNIST dataset
def prepare_image(path: str, mod_num):
    im = Image.open(path).convert('L')
    width = float(im.size[0])
    height = float(im.size[1])
    new_image = Image.new('L', (28, 28), (255))  # creates white canvas of 28x28 pixels

    if width > height:  # check which dimension is bigger
        # Width is bigger. Width becomes 20 pixels.
        nheight = int(round((20.0 / width * height), 0))  # resize height according to ratio width
        if (nheight == 0):  # rare case but minimum is 1 pixel
            nheight = 1
            # resize and sharpen
        img = im.resize((20, nheight), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wtop = int(round(((28 - nheight) / 2), 0))  # calculate horizontal position
        new_image.paste(img, (4, wtop))  # paste resized image on white canvas
    else:
        # Height is bigger. Height becomes 20 pixels.
        nwidth = int(round((20.0 / height * width), 0))  # resize width according to ratio height
        if (nwidth == 0):  # rare case but minimum is 1 pixel
            nwidth = 1
            # resize and sharpen
        img = im.resize((nwidth, 20), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wleft = int(round(((28 - nwidth) / 2), 0))  # calculate vertical position
        new_image.paste(img, (wleft, 4))  # paste resized image on white canvas

    new_image.save("test/mnist_format.png")

    pixels = list(new_image.getdata())  # get pixel values
    pixels_normalized = [(255 - x) * 1.0 / 255.0 for x in pixels]

    # Need adequate shape to 4D tensor for Model 2, no need for Model 1
    adequate_shape = np.reshape(pixels_normalized, (1, 28, 28))
    output = torch.FloatTensor(adequate_shape) if mod_num == 1 else \
        torch.FloatTensor(adequate_shape).unsqueeze(0)
    return output


def test_image(mod_num):
    if mod_num == 1:
        model = Model1()
        model.load_state_dict(torch.load('test/model1.pth'))
        model.eval()
        input_img = prepare_image('test/im_test.png', 1)
    else:
        model = Model2()
        model.load_state_dict(torch.load('test/model2.pth'))
        model.eval()
        input_img = prepare_image('test/im_test.png', 2)

    prediction = torch.argmax(model(input_img)).item()
    #prediction = torch.max(model(input_img), 1)[1].item()
    return str(prediction)
