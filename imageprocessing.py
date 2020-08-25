import base64
import os
import cv2
import numpy as np
from PIL import Image, ExifTags

UPLOAD_FOLDER="./static/images/"


def image_decode(id,im_b64):
    image_name=id+'.jpg'
    image_location = os.path.join(
                UPLOAD_FOLDER,
                image_name
            )
    with open(image_location,"wb") as f:
        f.write(base64.b64decode(im_b64))
    return image_location

def check_rotation(image_location):
    try:
        image=Image.open(image_location)

        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation':
                break

        exif=dict(image._getexif().items())

        if exif[orientation] == 3:
            image=image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image=image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image=image.rotate(90, expand=True)

        image.save(image_location)
        image.close()
    except (AttributeError, KeyError, IndexError):
        # cases: image don't have getexif
        pass

def img_to_encoding(img1,faces,model):
    x, y, w, h = faces[0]['box']
    fc = img1[y:y+h, x:x+w]
    roi = cv2.resize(fc, (96, 96))
    img = roi[...,::-1]
    img = np.around(np.transpose(img, (2,0,1))/255.0, decimals=12)
    x_train = np.array([img])
    embedding = model.predict_on_batch(x_train)
    return embedding

def change_dpi(image_location):
    from PIL import Image
    im = Image.open(image_location)
    nx, ny = im.size
    im2 = im.resize((int(nx), int(ny)), Image.BICUBIC)
    im2.save(image_location,dpi=(300,300))

   