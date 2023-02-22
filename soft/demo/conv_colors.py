'''
Project Name: Image compression

Student: Vincent ROBIN, ENSTA Bretagne, promotion 2023
Contact: vincent.robin@ensta-bretagne.org

File name: conv_color.py 
Create Date: 22/02/2023, 11:30:41 AM

Description: converts an image from RGB to YCrCb and displays the different colour channels

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

    PATH ="img/baboon.jpg"
    img_rgb = img.imread(PATH)
    height, width, channels = img_rgb.shape
    print("Frame shape: ({0} x {1})".format(height, width))

    ### Conversion RGB --> YCrCb
    img_ycrcb = rgb_to_ycrcb(img_rgb)
    
    fig1=plt.figure(figsize=(9,4))
    fig1.add_subplot(1, 2, 1)
    plt.title("Image originale (RGB)")
    plt.imshow(img_rgb)
    fig1.add_subplot(1, 2, 2)
    plt.title("Image YCrCb")
    plt.imshow(img_ycrcb)

    ### Visualisation des canaux R,G,B
    r = img_rgb[:,:,0]  
    b = img_rgb[:,:,1] 
    g = img_rgb[:,:,2] 

    ### Visualisation des canaux Y,Cr,Cb
    y =  img_ycrcb[:,:,0] 
    cr = img_ycrcb[:,:,1]  # Chrominance Red
    cb = img_ycrcb[:,:,2]  # Chrominance Blue

    fig2=plt.figure(figsize=(10,6))
    fig2.add_subplot(2, 3, 1)
    plt.title("Canal rouge")
    plt.imshow(r)
    fig2.add_subplot(2, 3, 2)
    plt.title("Canal vert")
    plt.imshow(g)
    fig2.add_subplot(2, 3, 3)
    plt.title("Canal bleu")
    plt.imshow(b)
    fig2.add_subplot(2, 3, 4)
    plt.title("Canal luminance Y")
    plt.imshow(y)
    fig2.add_subplot(2, 3, 5)
    plt.title("Canal chrominance rouge Cr")
    plt.imshow(cr)
    fig2.add_subplot(2, 3, 6)
    plt.title("Canal chrominance bleu Cb")
    plt.imshow(cb)

    # Ajustement de l'espacement entre les figures
    plt.subplots_adjust(wspace=0.5)
    
    # Sauvegarde des figures 
    fig1.savefig('conv_rgb_to_ycrcb.png')
    fig2.savefig('view_channels.png')

    plt.show()