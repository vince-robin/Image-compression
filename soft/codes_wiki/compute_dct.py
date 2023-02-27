'''
Project Name: Image compression

Student: Vincent ROBIN, ENSTA Bretagne, promotion 2023
Contact: vincent.robin@ensta-bretagne.org

File name: compute_dct.py 
Create Date: 22/02/2023, 18:48:01 AM

Description: compute the DCT for each block. Visualisation of:
- channels Y,Cr and Cb after DCT 
- the average DCT of all blocks (for Y, Cr and Cb), 
- the DCT on a randomly selected block in the image (also, for Y, Cr and Cb).

Packages: 
  - matplotlib (pip install matplotlib)
  - numpy (pip install matplotlib)

Revision: Revision 0.01 - File Created
Additional Comments:

'''

import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np

from matplotlib import cm
from math import ceil, sqrt, cos, pi


def rgb_to_ycrcb(im):
    
    xform = np.array([[.299, .587, .114], [.5, -.4187, -.0813], [-.1687, -.3313, .5]])
    ycbcr = im.dot(xform.T)
    ycbcr[:,:,[1,2]] += 128

    return np.uint8(ycbcr)


def compute_dct_coeffs():
    T = np.zeros((blockSize, blockSize))
    T[0, :] = sqrt(1.0/blockSize)
    for i in range(1, blockSize):
        for j in range(blockSize):
            T[i][j] = sqrt(2.0/blockSize)*cos(pi*(2.0*j+1.0)*i/(2.0*blockSize))

    return T


if __name__ == '__main__':

    PATH ="img/monster.jpg"
    img_rgb = img.imread(PATH)
    plt.imshow(img_rgb)
    plt.title("Image originale")
    plt.show()

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

    ### 64 DCT coefficients
    blockSize = 8
    T = compute_dct_coeffs()

    ### Visualization of the DCT coefficient matrix   
    fig, ax = plt.subplots()
    ax.matshow(T, cmap='viridis')
    for (i, j), z in np.ndenumerate(T):
        ax.text(j, i, np.round(z,2), ha='center', va='center', color='black')
    plt.title("64 DCT coefficients")
    plt.show()

    # ********************************************************#
    #                 PROCESS FOR LUMINANCE (Y)               #
    # ********************************************************#

    ### Zero Padding
    h = y.shape[0]
    w = y.shape[1]
    nbh = ceil(h / blockSize)  # number of blocks in height and width : nbh et nbw
    nbw = ceil(w / blockSize)
    hPadded = blockSize * nbh  # height and width of padded image : hPadded, wPadded
    wPadded = blockSize * nbw

    if (h % blockSize == 0) and (w % blockSize == 0):
        yPadded = y.copy()
    else:
        yPadded = np.zeros((hPadded, wPadded))
        for i in range(h):
            for j in range(w):
                yPadded[i, j] += y[i, j]

    yDct = np.zeros((hPadded, wPadded))
    yDctAccumulated = np.zeros((blockSize,blockSize))

    for i in range(nbh):
        row_ind_1 = i*blockSize
        row_ind_2 = row_ind_1+blockSize

        for j in range(nbw):
            col_ind_1 = j*blockSize
            col_ind_2 = col_ind_1+blockSize

            yBlock = yPadded[row_ind_1:row_ind_2, col_ind_1:col_ind_2]
            yDct[row_ind_1:row_ind_2, col_ind_1:col_ind_2] = (T.dot(yBlock)).dot(np.transpose(T))
            # Ajouter le bloc DCT accumulé
            yDctAccumulated += yDct[row_ind_1:row_ind_2, col_ind_1:col_ind_2]

    # Calculer la moyenne des blocs DCT
    yDctMean = yDctAccumulated / (nbh * nbw)


    # ********************************************************#
    #             PROCESS FOR CHROMINANCE (Cr,CB)             #
    # ********************************************************#

    # Zero-padding
    h_cbSub = crSub420.shape[0] 
    w_cbSub = crSub420.shape[1] 
    nbh_cbSub = ceil(h_cbSub / blockSize)
    nbw_cbSub = ceil(w_cbSub / blockSize)
    hPadded_cbSub = blockSize * nbh_cbSub
    wPadded_cbSub  = blockSize * nbw_cbSub

    if (h_cbSub % blockSize == 0) and (w_cbSub % blockSize == 0):
        crPadded = crSub420.copy()
        cbPadded = cbSub420.copy()
    else:
        crPadded = np.zeros((hPadded_cbSub, wPadded_cbSub))
        cbPadded = np.zeros((hPadded_cbSub, wPadded_cbSub))
        for i in range(h_cbSub):
            for j in range(w_cbSub):
                crPadded[i, j] += crSub420[i, j]
                cbPadded[i, j] += cbSub420[i, j]

    # Compute DCT 
    crDct = np.zeros((hPadded_cbSub, wPadded_cbSub))
    crDctAccumulated = np.zeros((blockSize, blockSize))
    cbDct = np.zeros((hPadded_cbSub, wPadded_cbSub))
    cbDctAccumulated = np.zeros((blockSize, blockSize))

    for i in range(nbh_cbSub):
        row_ind_1 = i*blockSize
        row_ind_2 = row_ind_1+blockSize

        for j in range(nbw_cbSub):
            col_ind_1 = j*blockSize
            col_ind_2 = col_ind_1+blockSize

            crBlock = crPadded[row_ind_1:row_ind_2, col_ind_1:col_ind_2]
            crDct[row_ind_1:row_ind_2, col_ind_1:col_ind_2] = (T.dot(crBlock)).dot(np.transpose(T))
            crDctAccumulated += crDct[row_ind_1:row_ind_2, col_ind_1:col_ind_2]
        
            cbBlock = cbPadded[row_ind_1:row_ind_2, col_ind_1:col_ind_2]
            cbDct[row_ind_1:row_ind_2, col_ind_1:col_ind_2] = (T.dot(cbBlock)).dot(np.transpose(T))
            cbDctAccumulated += cbDct[row_ind_1:row_ind_2, col_ind_1:col_ind_2]

    # Calculer la moyenne des blocs DCT
    crDctMean = crDctAccumulated / (nbh_cbSub * nbw_cbSub)
    cbDctMean = cbDctAccumulated / (nbh_cbSub * nbw_cbSub)

    # ********************************************************#
    #   Visualisation des canaux Y, Cr et Cb après la DCT     #
    # ******************************************************* #

    fig=plt.figure(figsize=(15,7.5))
    ax=fig.add_subplot(1,3,1)
    plt.title('yDCT')
    plt.imshow(np.uint8(yDct),cmap='gray')
    fig.add_subplot(1,3,2)
    plt.title('crDCT')
    plt.imshow(np.uint8(crDct),cmap='gray')
    fig.add_subplot(1,3,3)
    plt.title('cbDCT')
    plt.imshow(np.uint8(cbDct),cmap='gray')

    plt.show()

    # Sauvegarde de la figure 
    fig.savefig("channels_YCrCb_after_DCT.png")
    

    # ********************************************************#
    # Visualisation de la moyenne de la DCT de tous les blocs #
    # ******************************************************* #

    fig=plt.figure(figsize=(15,7.5))
    ax=fig.add_subplot(2,3,1)
    plt.title('yDCT')
    plt.imshow(yDctMean,cmap=cm.jet)
    plt.colorbar(shrink=1)
    ax.set_xticks(np.arange(yDctMean.shape[0]), np.arange(yDctMean.shape[1]))
    ax.set_yticks(np.arange(yDctMean.shape[0]), np.arange(yDctMean.shape[1]))
    fig.add_subplot(2,3,2)
    plt.title('crDCT')
    plt.imshow(crDctMean,cmap=cm.jet)
    plt.colorbar(shrink=1)
    ax.set_xticks(np.arange(crDctMean.shape[0]), np.arange(crDctMean.shape[1]))
    ax.set_yticks(np.arange(crDctMean.shape[0]), np.arange(crDctMean.shape[1]))
    fig.add_subplot(2,3,3)
    plt.title('cbDCT')
    plt.imshow(cbDctMean,cmap=cm.jet)
    plt.colorbar(shrink=1)
    ax.set_xticks(np.arange(cbDctMean.shape[0]), np.arange(cbDctMean.shape[1]))
    ax.set_yticks(np.arange(cbDctMean.shape[0]), np.arange(cbDctMean.shape[1]))

    # Création d'une grille 3D à partir de la taille des données DCT
    x, y = np.meshgrid(np.arange(yDctMean.shape[0]), np.arange(yDctMean.shape[1]))
    
    ax1 = fig.add_subplot(234, projection='3d')
    ax1.plot_surface(x, y, yDctMean, cmap='viridis')  # Tracé de la surface 3D
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('yDCT Coefficient')
    ax1.set_xticks(np.arange(yDctMean.shape[0]), np.arange(yDctMean.shape[1]))
    ax1.set_yticks(np.arange(yDctMean.shape[0]), np.arange(yDctMean.shape[1]))

    ax2 = fig.add_subplot(235, projection='3d')
    ax2.plot_surface(x, y, cbDctMean, cmap='viridis')  # Tracé de la surface 3D
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('cbDCT Coefficient')
    ax2.set_xticks(np.arange(cbDctMean.shape[0]), np.arange(cbDctMean.shape[1]))
    ax2.set_yticks(np.arange(cbDctMean.shape[0]), np.arange(cbDctMean.shape[1]))

    ax3 = fig.add_subplot(236, projection='3d')
    ax3.plot_surface(x, y, crDctMean, cmap='viridis')  # Tracé de la surface 3D
    ax3.set_xlabel('X')
    ax3.set_ylabel('Y')
    ax3.set_zlabel('crDCT Coefficient')
    ax3.set_xticks(np.arange(crDctMean.shape[0]), np.arange(crDctMean.shape[1]))
    ax3.set_yticks(np.arange(crDctMean.shape[0]), np.arange(crDctMean.shape[1]))
    
    plt.show()

    # Sauvegarde de la figure 
    fig.savefig('mean_of_DCT_for_yCrCb_channels.png')

    # ******************************************************* #
    # Visualisation de la DCT pour un bloc choisis au hasard  #
    # ******************************************************* #

    i = np.random.randint(0, nbh-1)
    j = np.random.randint(0, nbw-1) 
    row_ind_1 = i*blockSize
    row_ind_2 = row_ind_1+blockSize
    col_ind_1 = j*blockSize
    col_ind_2 = col_ind_1+blockSize

    fig=plt.figure(figsize=(15,7.5))
    fig.add_subplot(2,3,1)
    plt.title('yDCT')
    plt.imshow(yDct[row_ind_1:row_ind_2, col_ind_1:col_ind_2],cmap=cm.jet)
    plt.colorbar(shrink=1)

    i = np.random.randint(0, nbh_cbSub-1)
    j = np.random.randint(0, nbw_cbSub-1) 
    row_ind_1 = i*blockSize
    row_ind_2 = row_ind_1+blockSize
    col_ind_1 = j*blockSize
    col_ind_2 = col_ind_1+blockSize

    fig.add_subplot(2,3,2)
    plt.title('cbDCT')
    plt.imshow(cbDct[row_ind_1:row_ind_2, col_ind_1:col_ind_2],cmap=cm.jet)
    plt.colorbar(shrink=1)

    fig.add_subplot(2,3,3)
    plt.title('crDCT')
    plt.imshow(crDct[row_ind_1:row_ind_2, col_ind_1:col_ind_2],cmap=cm.jet)
    plt.colorbar(shrink=1)

    ax1 = fig.add_subplot(234, projection='3d')
    ax1.plot_surface(x, y, yDct[row_ind_1:row_ind_2, col_ind_1:col_ind_2], cmap='viridis')  # Tracé de la surface 3D
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('yDCT Coefficient')
    ax1.set_xticks(np.arange(8,8))
    ax1.set_yticks(np.arange(8,8))

    ax2 = fig.add_subplot(235, projection='3d')
    ax2.plot_surface(x, y, cbDct[row_ind_1:row_ind_2, col_ind_1:col_ind_2], cmap='viridis')  # Tracé de la surface 3D
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('cbDCT Coefficient')
    ax2.set_xticks(np.arange(8,8))
    ax2.set_yticks(np.arange(8,8))

    ax3 = fig.add_subplot(236, projection='3d')
    ax3.plot_surface(x, y, crDct[row_ind_1:row_ind_2, col_ind_1:col_ind_2], cmap='viridis')  # Tracé de la surface 3D
    ax3.set_xlabel('X')
    ax3.set_ylabel('Y')
    ax3.set_zlabel('crDCT Coefficient')
    ax3.set_xticks(np.arange(8,8))
    ax3.set_yticks(np.arange(8,8))
        
    plt.show()

    # Sauvegarde de la figure 
    fig.savefig('DCT_for_a_random_selected_block.png')
    
