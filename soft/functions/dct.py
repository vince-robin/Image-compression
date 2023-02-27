import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def compute_dct_coeffs(blockSize):
    
    T = np.zeros((blockSize, blockSize))
    
    T[0, :] = np.sqrt(1.0/blockSize)
    
    for i in range(1, blockSize):
        for j in range(blockSize):
            T[i][j] = np.sqrt(2.0/blockSize)*np.cos(np.pi*(2.0*j+1.0)*i/(2.0*blockSize))

    return T


def viewing_dct_matrix(dct_matrix, out_dir):
  
    fig, ax = plt.subplots()
    ax.matshow(dct_matrix, cmap='viridis')
    for (i, j), z in np.ndenumerate(dct_matrix):
        if z < -0.35:   # for better visualization when the colour is dark
            ax.text(j, i, np.round(z,2), ha='center', va='center', color='white')  
        else:
            ax.text(j, i, np.round(z,2), ha='center', va='center', color='black')
    plt.title("The 64 DCT coefficients")

    plt.savefig(out_dir+"dct_matrix.png")


def viewing_dct_for_a_random_selected_block(yDCT, crDCT, cbDCT, h_luma, w_luma, h_chroma, w_chroma, blockSize, out_dir):

    xlabels=[0,1,2,3,4,5,6,7]
    ylabels=[0,1,2,3,4,5,6,7]

    nbh_luma = np.ceil(h_luma / blockSize)
    nbw_luma = np.ceil(w_luma / blockSize)
    i = np.random.randint(0, nbh_luma-1)
    j = np.random.randint(0, nbw_luma-1) 
    row_ind_1 = i*blockSize
    row_ind_2 = row_ind_1+blockSize
    col_ind_1 = j*blockSize
    col_ind_2 = col_ind_1+blockSize

    fig=plt.figure(figsize=(15,7.5))
    fig.suptitle("DCT for randoms selected Y,Cb,Cr blocks")
    ax = fig.add_subplot(2,3,1)
    plt.title('yDCT')
    plt.imshow(yDCT[row_ind_1:row_ind_2, col_ind_1:col_ind_2],cmap='jet')
    plt.colorbar(shrink=1)
    ax.set_xticks(xlabels, xlabels)
    ax.set_yticks(ylabels, ylabels)

    ax = fig.add_subplot(234, projection='3d')
    x, y = np.meshgrid(np.arange(blockSize), np.arange(blockSize))  # creating a 3D grid from the size of one block
    ax.plot_surface(x, y, yDCT[row_ind_1:row_ind_2, col_ind_1:col_ind_2], cmap='jet')  # drawing of the 3D-surface
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('yDCT Coefficient')
    ax.set_xticks(xlabels, xlabels)
    ax.set_yticks(ylabels, ylabels)

    nbh_chroma = np.ceil(h_chroma / blockSize)
    nbw_chroma = np.ceil(w_chroma / blockSize)
    i = np.random.randint(0, nbh_chroma-1)
    j = np.random.randint(0, nbw_chroma-1) 
    row_ind_1 = i*blockSize
    row_ind_2 = row_ind_1+blockSize
    col_ind_1 = j*blockSize
    col_ind_2 = col_ind_1+blockSize

    ax = fig.add_subplot(2,3,2)
    plt.title('cbDCT')
    plt.imshow(cbDCT[row_ind_1:row_ind_2, col_ind_1:col_ind_2],cmap='jet')
    plt.colorbar(shrink=1)
    ax.set_xticks(xlabels, xlabels)
    ax.set_yticks(ylabels, ylabels)

    ax = fig.add_subplot(2,3,3)
    plt.title('crDCT')
    plt.imshow(crDCT[row_ind_1:row_ind_2, col_ind_1:col_ind_2],cmap='jet')
    plt.colorbar(shrink=1)
    ax.set_xticks(xlabels, xlabels)
    ax.set_yticks(ylabels, ylabels)

    ax = fig.add_subplot(235, projection='3d')
    ax.plot_surface(x, y, cbDCT[row_ind_1:row_ind_2, col_ind_1:col_ind_2], cmap='jet') 
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('cbDCT Coefficient')
    ax.set_xticks(xlabels, xlabels)
    ax.set_yticks(ylabels, ylabels)

    ax = fig.add_subplot(236, projection='3d')
    ax.plot_surface(x, y, crDCT[row_ind_1:row_ind_2, col_ind_1:col_ind_2], cmap='jet')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('crDCT Coefficient')
    ax.set_xticks(xlabels, xlabels)
    ax.set_yticks(ylabels, ylabels)
    
    plt.savefig(out_dir+"dct_for_a_random_selected_block.png")
