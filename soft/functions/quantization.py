import numpy as np
import matplotlib.pyplot as plt


QTY = np.array([
    [16, 11, 10, 16,  24,  40,  51,  61],  # luminance quantization table from JPEG standard
    [12, 12, 14, 19,  26,  58,  60,  55],
    [14, 13, 16, 24,  40,  57,  69,  56],
    [14, 17, 22, 29,  51,  87,  80,  62],
    [18, 22, 37, 56,  68, 109, 103,  77],
    [24, 35, 55, 64,  81, 104, 113,  92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103,  99]])

QTC = np.array([
    [17, 18, 24, 47, 99, 99, 99, 99],  # chrominance quantization table from JPEG standard
    [18, 21, 26, 66, 99, 99, 99, 99],
    [24, 26, 56, 99, 99, 99, 99, 99],
    [47, 66, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99]])


def quantize(QLevel, channel):

    if channel == 'luminance' : 
        Q_mat = QTY
    elif channel == 'chrominance':
        Q_mat = QTC

    if QLevel < 50 and QLevel > 1:
        Q = (50 / QLevel) * Q_mat
    elif QLevel < 100:
        Q = ((100 - QLevel) / 50) * Q_mat
    else:
        print("Quantization level must be in the range [1..99]")
    
    return np.uint8(Q)


def viewing_quantization_matrix(quantization_matrix, channel, out_dir):
  
    fig, ax = plt.subplots()
    ax.matshow(quantization_matrix, cmap='viridis')
    for (i, j), z in np.ndenumerate(quantization_matrix):
        ax.text(j, i, int(z), ha='center', va='center', color='black')
    plt.title("Quantization matrix for "+channel)

    plt.savefig(out_dir+channel+"_quantization_matrix.png")



def viewing_quantized_zigzaged_random_block(yQuantized, yZigzag, h_luma, w_luma, blockSize, out_dir):
    
    nbh_luma = np.ceil(h_luma / blockSize)
    nbw_luma = np.ceil(w_luma / blockSize)
    i = np.random.randint(0, nbh_luma-1)
    j = np.random.randint(0, nbw_luma-1) 
    row_ind_1 = i*blockSize
    row_ind_2 = row_ind_1+blockSize
    col_ind_1 = j*blockSize
    col_ind_2 = col_ind_1+blockSize
   
    fig=plt.figure(figsize=(12,6))
    ax=fig.add_subplot(1,2,1)
    ax.matshow(yQuantized[row_ind_1:row_ind_2, col_ind_1:col_ind_2], cmap='viridis')
    for (ki, kj), z in np.ndenumerate(yQuantized[row_ind_1:row_ind_2, col_ind_1:col_ind_2]):
        ax.text(ki, kj, int(z), ha='center', va='center', color='black')
    plt.title("One chrominance block quantized")

    ax=fig.add_subplot(1,2,2)
    ax.plot(yZigzag[row_ind_1:row_ind_2, col_ind_1:col_ind_2].flatten())
    plt.title("Zig-zag scan")
    plt.xlabel("Index")
    plt.ylabel("Zig zag value")

    plt.savefig(out_dir+"quantized_zigzaged_random_Yblock.png")


def viewing_YCrCb_channels_after_DCT_and_quantization(yQuantized, crQuantized, cbQuantized, QLevel, out_dir):
    
    fig = plt.figure(figsize=(10,4))
    fig.suptitle("Y, Cr, Cb after DCT + Quantization (QLevel={0})".format(QLevel))
    fig.add_subplot(1, 3, 1)
    plt.imshow(np.uint8(yQuantized), cmap='gray')
    fig.add_subplot(1, 3, 2)
    plt.imshow(np.uint8(crQuantized), cmap='gray')
    fig.add_subplot(1, 3, 3)
    plt.imshow(np.uint8(cbQuantized), cmap='gray')

    plt.savefig(out_dir+"YCrCb_channels_after_DCT_and_quantization.png")
