'''
Project Name: Image compression

Student: Vincent ROBIN, ENSTA Bretagne, promotion 2023
Contact: vincent.robin@ensta-bretagne.org

File name: chroma_subsampling.py 
Create Date: 22/02/2023, 15:09:41 AM

Description: converts an image from RGB to YCrCb and sub-samples the chrominance in order to to get the 4:2:0 format

Packages: 
  - matplotlib (pip install matplotlib)
  - numpy (pip install matplotlib)

Revision: Revision 0.01 - File Created
Additional Comments:

'''

import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np


def rgb_to_ycrcb(im):
    
    xform = np.array([[.299, .587, .114], [.5, -.4187, -.0813], [-.1687, -.3313, .5]])
    ycbcr = im.dot(xform.T)
    ycbcr[:,:,[1,2]] += 128

    return np.uint8(ycbcr)



if __name__ == '__main__':

    PATH ="img/sunflower.jpg"
    img_rgb = img.imread(PATH)
    height, width, channels = img_rgb.shape
    print("Frame shape: ({0} x {1})".format(height, width))

    ### Conversion RGB --> YCrCb
    img_ycrcb = rgb_to_ycrcb(img_rgb)

    ### Extraction des canaux Y,Cr,Cb
    y =  img_ycrcb[:,:,0] 
    cr = img_ycrcb[:,:,1]  # Chrominance Red
    cb = img_ycrcb[:,:,2]  # Chrominance Blue

    ### Chroma subsampling (4:4:4 --> 4:2:2)
    crSub422 = cr[::2, ::2]
    cbSub422 = cb[::2, ::2]

    ### Chroma subsampling (4:2:2 --> 4:2:0)
    crSub420 = crSub422[::2, ::2]
    cbSub420 = cbSub422[::2, ::2]

    fig1=plt.figure(figsize=(9,5))
    fig1.add_subplot(2, 2, 1)
    plt.title("Composante Cr")
    plt.imshow(cr)
    fig1.add_subplot(2, 2, 3)
    plt.title("Composante Cr 4:2:0")
    plt.imshow(crSub420)
    fig1.add_subplot(2, 2, 2)
    plt.title("Composante Cb")
    plt.imshow(cb)
    fig1.add_subplot(2, 2, 4)
    plt.title("Composante Cb 4:2:0")
    plt.imshow(cbSub420)

    # Ajustement de l'espacement entre les figures
    plt.subplots_adjust(hspace=0.4)

    # Sauvegarde de la figure 
    fig1.savefig('chroma_subsampling.png')
    
    plt.show()
