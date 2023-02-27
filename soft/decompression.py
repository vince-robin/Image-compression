'''
Project Name: Image compression

Student: Vincent ROBIN, ENSTA Bretagne, promotion 2023
Contact: vincent.robin@ensta-bretagne.org

File name: decompression.py 
Creation Date: 

Description: decompresses the bitstream of the compressed image to reconstruct it with the following process:
- reading bitstream
- decode the Variable Length Code (VLC) with Huffman dictionnaries transmitted by the encoder
- Run-Length Decoding (RLE)
- inverse Zigzag
- reformats the data stream into 8*8 blocks 
- dequantization (with the quantization level transmitted by the encoder)
- Inverse DCT (Discrete Cosine Transform)
- chroma upsampling (4:2:2 to 4:4:4)
- reconstructs the image from the Y,Cr,Cb channels (with the original image dimensions transmitted by the decoder)
- colorspace conversion (YCrCb to RGB)
- comparison with the original image 
The program generates the decompressed picture in the output directory.

Different information is given to the user: 
- dimensions of the original image
- quantization level
- Mean Square Error (MSE) 
- Signal to Noise Ratio (SNR)
- execution time

Packages: 
  - matplotlib (pip install matplotlib)
  - numpy (pip install matplotlib)

Revision: Revision 0.01 - File Created

Additional Comments: Run the program with the command "python3 -B decompression.py".

"-B" : to ignore the bytes codes generated in the __pycache__ folder

'''

import cv2
import time
import numpy as np
from math import ceil
import matplotlib.pyplot as plt

# My functions in the directory "functions"
from functions.encoded_bitstream import read_from_file, read_header
from functions.huffman import huffman_decoding, open_huffman_dict
from functions.run_length_encoding import run_length_decoding
from functions.dct import compute_dct_coeffs
from functions.quantization import quantize
from functions.zigzag import inverse_zigzag
from functions.get_metrics import mse, snr
from functions.ppm_file import save_into_ppm
from functions.colorspace import ycrcb_to_rgb


BLOCK_SIZE = 8  # the block size is always 8
OUTPUT_DIR = "outputs/"  # output directory
ANALYSE_DIR = "analyse/"


if __name__ == '__main__':

    start_time = time.time()  # start timer to calculate execution time
    
    ### Reading bitstream 
    header, yCompressed, crCompressed, cbCompressed = read_from_file(OUTPUT_DIR+"/compressed_data.bin")  # extract header and the 3 channels from the binary file
    
    height, width, h_luma, w_luma, h_chroma, w_chroma, QLevel = read_header(header)  # reading the parameters of the header

    nbh_luma = ceil(h_luma / BLOCK_SIZE)  # determinates the others utils paramaters for image reconstruction (number of blocks in height and width: nbh et nbw)
    nbw_luma = ceil(w_luma / BLOCK_SIZE)
    nbh_chroma = ceil(h_chroma / BLOCK_SIZE)
    nbw_chroma = ceil(w_chroma / BLOCK_SIZE)

    hPadded_luma = BLOCK_SIZE * nbh_luma  # height and width of padded image: hPadded, wPadded
    wPadded_luma = BLOCK_SIZE * nbw_luma
    hPadded_chroma = BLOCK_SIZE * nbh_chroma
    wPadded_chroma = BLOCK_SIZE * nbw_chroma

    print("\nOriginal picture dimensions: {0}x{1}".format(height, width))  # picture dimensions and quantization level transmitted by the encoder
    print("Quantization level (1-99):", QLevel)

    ### Huffman decoding

    yHuffman_dict, cbHuffman_dict, crHuffman_dict = open_huffman_dict(OUTPUT_DIR)  # opens the dictionaries of the 3 channels in JSON format

    yDecompressed = huffman_decoding(yCompressed, yHuffman_dict)
    cbDecompressed = huffman_decoding(cbCompressed, cbHuffman_dict)
    crDecompressed = huffman_decoding(crCompressed, crHuffman_dict)

    ### Run-Length Decoding (RLD)

    yRld = run_length_decoding(yDecompressed, hPadded_luma, wPadded_luma)
    cbRld = run_length_decoding(cbDecompressed, hPadded_chroma, wPadded_chroma)
    crRld = run_length_decoding(crDecompressed, hPadded_chroma, wPadded_chroma)

    yRld  = np.reshape(yRld, (hPadded_luma, wPadded_luma))
    cbRld = np.reshape(cbRld, (hPadded_chroma, wPadded_chroma))
    crRld = np.reshape(crRld, (hPadded_chroma, wPadded_chroma))

    ### Inverse zigzag, Dequantization and Inverse DCT independently on luminance and chrominance channels
    
    T = compute_dct_coeffs(BLOCK_SIZE)  # calculation of the matrix of 64 coefficients of the DCT

    # ******************************************* #
    #            Process for luminance            #
    # ******************************************* #
    Q_luma = quantize(QLevel, channel='luminance')  #  quantization matrix calculation (according to the quantization level "QLevel" transmitted by the encoder)
    
    yIdct = np.zeros((hPadded_luma, wPadded_luma))
    yDequantize = np.zeros((hPadded_luma, wPadded_luma))

    for i in range(nbh_luma):
        row_ind_1 = i*BLOCK_SIZE
        row_ind_2 = row_ind_1+BLOCK_SIZE

        for j in range(nbw_luma):
            col_ind_1 = j*BLOCK_SIZE
            col_ind_2 = col_ind_1+BLOCK_SIZE

            yBlock = yRld[row_ind_1:row_ind_2, col_ind_1:col_ind_2]
            yInvZigzag = inverse_zigzag(yBlock.flatten(), BLOCK_SIZE, BLOCK_SIZE)
            yDequantize[row_ind_1:row_ind_2, col_ind_1:col_ind_2] = np.multiply(Q_luma, yInvZigzag)
            yIdct[row_ind_1:row_ind_2, col_ind_1:col_ind_2] = (np.transpose(T).dot(yDequantize[row_ind_1:row_ind_2, col_ind_1:col_ind_2])).dot(T)  # mathematical expression of the I-DCT. T is the matrix of the 64 coefficients of the DCT


    # ********************************************* #
    #        Process for chrominance  Cr,Cb         #
    # ********************************************* #
    Q_chroma = quantize(QLevel, channel='chrominance')

    cbIdct = np.zeros((hPadded_chroma, wPadded_chroma))
    cbDequantize = np.zeros((hPadded_chroma, wPadded_chroma))
    crIdct = np.zeros((hPadded_chroma, wPadded_chroma))
    crDequantize = np.zeros((hPadded_chroma, wPadded_chroma))

    for i in range(nbh_chroma):
        row_ind_1 = i*BLOCK_SIZE
        row_ind_2 = row_ind_1+BLOCK_SIZE

        for j in range(nbw_chroma):
            col_ind_1 = j*BLOCK_SIZE
            col_ind_2 = col_ind_1+BLOCK_SIZE

            cbBlock = cbRld[row_ind_1:row_ind_2, col_ind_1:col_ind_2]
            cbInvZigzag = inverse_zigzag(cbBlock.flatten(), BLOCK_SIZE, BLOCK_SIZE)
            cbDequantize[row_ind_1:row_ind_2, col_ind_1:col_ind_2] = np.multiply(Q_chroma, cbInvZigzag)
            cbIdct[row_ind_1:row_ind_2, col_ind_1:col_ind_2] = (np.transpose(T).dot(cbDequantize[row_ind_1:row_ind_2, col_ind_1:col_ind_2])).dot(T)

            crBlock = crRld[row_ind_1:row_ind_2, col_ind_1:col_ind_2]
            crInvZigzag = inverse_zigzag(crBlock.flatten(), BLOCK_SIZE, BLOCK_SIZE)
            crDequantize[row_ind_1:row_ind_2, col_ind_1:col_ind_2] = np.multiply(Q_chroma, crInvZigzag)
            crIdct[row_ind_1:row_ind_2, col_ind_1:col_ind_2] = (np.transpose(T).dot(crDequantize[row_ind_1:row_ind_2, col_ind_1:col_ind_2])).dot(T)


    ### Chroma upsampling (4:2:2 --> 4:4:4)
    
    cbIdct = np.repeat(cbIdct, 2, axis=1)
    cbIdct = np.repeat(cbIdct, 2, axis=0)

    crIdct = np.repeat(crIdct, 2, axis=1)
    crIdct = np.repeat(crIdct, 2, axis=0)

    ### Image reconstruction with the original dimensions transmitted by the encoder
    
    imgDecompressed = np.zeros((height,width,3))
    
    imgDecompressed[:, :, 0] = yIdct[:height,:width]
    imgDecompressed[:, :, 1] = crIdct[:height,:width]
    imgDecompressed[:, :, 2] = cbIdct[:height,:width]

    ### Colorspace conversion (YCrCb to RGB)

    decompressed_picture = ycrcb_to_rgb(imgDecompressed)

    plt.imsave(OUTPUT_DIR+"decompressed_picture.jpg", decompressed_picture)   # save in JPEG format in the output directory
    save_into_ppm(OUTPUT_DIR+"decompressed_picture.ppm", "P3", width, height, 255, decompressed_picture)  # saved in PPM format in the output directory (use Irfanview software to view it)

    end_time = time.time()   #  end of decompression process: stop timer to determinate the execution time
    execution_time = end_time - start_time
    print("Execution time: {:.2f} sec".format(execution_time))

    ### Comparison with the original image

    original_picture = plt.imread(OUTPUT_DIR+"original_picture.jpg")  # reading the original image present in the output directory
    
    signal_to_noise_ratio = snr(original_picture, decompressed_picture)  # SNR in logarithmic scale: tends to 0 when the images are totally different
    print("SNR: {:.2f} dB".format(signal_to_noise_ratio))
    
    mean_squared_error = mse(original_picture, decompressed_picture)  # MSE: tends to 0 when the images are similar
    print("MSE: {:.2f}".format(mean_squared_error))
    
    x1 = cv2.cvtColor(original_picture, cv2.COLOR_RGB2GRAY)  # grayscale conversion to use cv2.absdiff and cv2.subtract functions
    x2 = cv2.cvtColor(decompressed_picture, cv2.COLOR_RGB2GRAY)
    absdiff = cv2.absdiff(x1, x2)  # absolute difference between original picture (x1) and reconstructed picture (x2)
    diff = cv2.subtract(x1, x2)

    fig=plt.figure(figsize=(16,10))
    fig.add_subplot(1,2,1)
    plt.title("Image décompressée \n QLevel={0}, SNR={1:.2f}dB, MSE={2:.2f}".format(QLevel, signal_to_noise_ratio, mean_squared_error))
    plt.imshow(decompressed_picture)
    fig.add_subplot(1,2,2)
    plt.title("Différence image d'origine/décompressée")
    plt.imshow(np.uint8(diff), cmap='gray')
    plt.savefig(ANALYSE_DIR+"comparing_original_decompressed_picture.png")  # saving comparison figure into the analyse directory
    
    plt.show()  # to be kept if the user wants to see the figure live on his screen
