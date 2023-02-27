'''
Project Name: Image compression

Student: Vincent ROBIN, ENSTA Bretagne, promotion 2023
Contact: vincent.robin@ensta-bretagne.org

File name: compression.py 
Creation Date: 

Description: Reads an image (any format and any size) and compresses it according to the following process:
- conversion from RGB to YCrCb colour space
- chrominance subsampling (4:4:4 to 4:2:2)
- cutting into 8*8 blocks 
- zero-padding (for images with dimensions not divisible by the block size)
- DCT (Discrete Cosine Transform)
- quantization (with a given quantization level)
- replay of the blocks according to a Zigzag sequence
- Run Length Encoding (RLE) 
- Variable Length Coding (VLC) with Huffman.
- writing output bitstream to be transmitted to the decoder

The program generates 4 files in the output directory: 
- a binary file (data_compressed.bin)
- the Huffman dictionaries for the three components Y,Cr,Cb
It also several graphics in the analysis directory.

The binary file contains a header before the compressed data to transmit the information necessary 
to decode the image (quantization level, image dimensions, ...).
Different information is given to the user in the terminal: 
- dimensions of the original image
- zero-padding, or not
- quantization level
- correctly generated files
- compression rate 
- execution time
- statistics on the Huffman code.

Packages: 
  - matplotlib (pip install matplotlib)
  - numpy (pip install matplotlib)

Revision: Revision 0.01 - File Created

Additional Comments: Run the program with the command "python3 -B compression.py img_to_compress.jpg -q 80".

"-B" : to ignore the bytes codes generated in the __pycache__ folder
Argument 1: image to be compressed (present in the "/imgs" directory)
Argument 2 optional 2 : quantization level (between 1 and 99). Default value = 50 
The higher this level, the better the quality of the image, but the compression rate will be lower.

'''


import os
import time
import argparse
import numpy as np
import matplotlib.image as img
import matplotlib.pyplot as plt

# My functions in the directory "functions"
from functions.run_length_encoding import run_length_encoding
from functions.zigzag import zigzag, viewing_zigzag_table
from functions.encoded_bitstream import write_to_file, create_header
from functions.zero_padding import make_zero_padding
from functions.huffman import huffman_encoding, view_huffman_stats, save_huffman_dict
from functions.dct import compute_dct_coeffs, viewing_dct_matrix, viewing_dct_for_a_random_selected_block
from functions.colorspace import rgb_to_ycrcb, viewing_converted_picture_into_YCrCb_colorspace, viewing_subsampled_channels, viewing_luminance_and_chrominance_channels
from functions.quantization import quantize, viewing_quantization_matrix, viewing_quantized_zigzaged_random_block, viewing_YCrCb_channels_after_DCT_and_quantization


BLOCK_SIZE = 8   # the block size is always 8
OUTPUT_DIR = "outputs/"  # output directory
ANALYSE_DIR = "analyse/"


if __name__ == '__main__':

    ### Gets the two command line arguments

    parser = argparse.ArgumentParser(description='Picture compression')
    parser.add_argument('arg1', help='Path of the image to be decompressed', type=str) # 1st argument: the image to be compressed
    parser.add_argument('-q', '--arg2', help='Quantification level (1 to 99)', type=int, default='50') # 2nd argument: quantization level which is optional. Default value: 50
    args = parser.parse_args()

    if not (os.path.exists(OUTPUT_DIR) and os.path.exists(ANALYSE_DIR)):  # creation of output directories if they doesn't exist
        os.mkdir(OUTPUT_DIR)
        os.mkdir(ANALYSE_DIR)
    
    start_time = time.time()  # start the timer

    ### Read the image to be compressed 

    PATH = "imgs/" + args.arg1  # according to the 1st argument of the command line
    original_picture = img.imread(PATH)
   
    plt.imsave(OUTPUT_DIR+"original_picture.jpg", original_picture) # save to the output directory to compare with the uncompressed image
    
    height, width, channels = original_picture.shape  # original image size
    print("\nOriginal picture dimension: ({0} x {1})".format(height, width))
    
  
    total_number_of_bits = (height * width * channels * 8) # number of bits before compression. (x8) because pixels are coded on 8 bites (value between 0 and 255)
    print("Total number of bits: ", total_number_of_bits)

    ### Colorspace conversion (RGB to Y,Cr,Cb)

    img_ycrcb = rgb_to_ycrcb(original_picture)

    y =  img_ycrcb[:,:,0]  # extraction of Y (luminance)
    cr = img_ycrcb[:,:,1]  # extraction of Cr (Chrominance red)
    cb = img_ycrcb[:,:,2]  # extraction of Cb (Chrominance blue)

    ### Chroma subsampling (4:4:4 to 4:2:2)

    crSub422 = cr[::2, ::2]
    cbSub422 = cb[::2, ::2]
    
    h_luma, w_luma = y.shape  # subsampled channel dimensions
    h_chroma, w_chroma = cbSub422.shape  # or crSub.shape because the chrominance signals have the same dimensions!

    ### Zero-padding: only for images that have dimensions not divisible by the block size

    yPadded,crPadded,cbPadded,nbh_luma,nbw_luma,nbh_chroma,nbw_chroma,hPadded_luma,wPadded_luma,hPadded_chroma,wPadded_chroma = make_zero_padding(y, crSub422, cbSub422, BLOCK_SIZE)

    ### DCT (Discrete Cosine Transform), Quantization and Zig-zag independently on luminance and chrominance channels
    
    QLevel = args.arg2  # quantization level (between 1 and 99), according to the 2nd argument of the command line (default value=50)
    print("Quantization level is (1-99): ", QLevel)
    
    T = compute_dct_coeffs(BLOCK_SIZE)  # calculation of the matrix of 64 coefficients of the DCT
    
    # ******************************************* #
    #            Process for luminance            #
    # ******************************************* #
    Q_luma = quantize(QLevel, channel='luminance')  # quantification matrix calculation

    yDct = np.zeros((hPadded_luma, wPadded_luma))
    yQuantized = np.zeros((hPadded_luma, wPadded_luma))
    yZigzag = np.zeros((hPadded_luma, wPadded_luma))
    
    for i in range(nbh_luma):
        row_ind_1 = i*BLOCK_SIZE
        row_ind_2 = row_ind_1+BLOCK_SIZE

        for j in range(nbw_luma):
            col_ind_1 = j*BLOCK_SIZE
            col_ind_2 = col_ind_1+BLOCK_SIZE

            yBlock = yPadded[row_ind_1:row_ind_2, col_ind_1:col_ind_2]  # one 8*8 block
            yDct[row_ind_1:row_ind_2, col_ind_1:col_ind_2] = (T.dot(yBlock)).dot(np.transpose(T))  # mathematical expression of the DCT. T is the matrix of the 64 coefficients of the DCT
            yQuantized[row_ind_1:row_ind_2, col_ind_1:col_ind_2] = np.round(yDct[row_ind_1:row_ind_2, col_ind_1:col_ind_2]/ Q_luma)  # by default, the round() function rounds to the nearest integer
            yZigzag[row_ind_1:row_ind_2, col_ind_1:col_ind_2] = np.reshape(zigzag(yQuantized[row_ind_1:row_ind_2, col_ind_1:col_ind_2]),(BLOCK_SIZE, BLOCK_SIZE))
    
    yZigzag = yZigzag.astype(np.int16)  # because after DCT and quantization the values are floating

    # ********************************************* #
    #        Process for chrominance  Cr,Cb         #
    # ********************************************* #
    Q_chroma = quantize(QLevel, channel='chrominance')

    crDct = np.zeros((hPadded_chroma, wPadded_chroma))
    cbDct = np.zeros((hPadded_chroma, wPadded_chroma))
    crQuantized = np.zeros((hPadded_chroma, wPadded_chroma))
    cbQuantized = np.zeros((hPadded_chroma, wPadded_chroma))
    crZigzag = np.zeros((hPadded_chroma, wPadded_chroma))
    cbZigzag = np.zeros((hPadded_chroma, wPadded_chroma))

    for i in range(nbh_chroma):
        row_ind_1 = i*BLOCK_SIZE
        row_ind_2 = row_ind_1+BLOCK_SIZE

        for j in range(nbw_chroma):
            col_ind_1 = j*BLOCK_SIZE
            col_ind_2 = col_ind_1+BLOCK_SIZE

            cbBlock = cbPadded[row_ind_1:row_ind_2, col_ind_1:col_ind_2]
            cbDct[row_ind_1:row_ind_2, col_ind_1:col_ind_2] = (T.dot(cbBlock)).dot(np.transpose(T))
            cbQuantized[row_ind_1:row_ind_2, col_ind_1:col_ind_2] = np.round(cbDct[row_ind_1:row_ind_2, col_ind_1:col_ind_2]/ Q_chroma)
            cbZigzag[row_ind_1:row_ind_2, col_ind_1:col_ind_2] = np.reshape(zigzag(cbQuantized[row_ind_1:row_ind_2, col_ind_1:col_ind_2]), (BLOCK_SIZE, BLOCK_SIZE))

            crBlock = crPadded[row_ind_1:row_ind_2, col_ind_1:col_ind_2]
            crDct[row_ind_1:row_ind_2, col_ind_1:col_ind_2] = (T.dot(crBlock)).dot(np.transpose(T))
            crQuantized[row_ind_1:row_ind_2, col_ind_1:col_ind_2] = np.round(crDct[row_ind_1:row_ind_2, col_ind_1:col_ind_2]/ Q_chroma)
            crZigzag[row_ind_1:row_ind_2, col_ind_1:col_ind_2] = np.reshape(zigzag(crQuantized[row_ind_1:row_ind_2, col_ind_1:col_ind_2]), (BLOCK_SIZE, BLOCK_SIZE))

    cbZigzag = cbZigzag.astype(np.int16)  # because after DCT and quantization the values are floating
    crZigzag = crZigzag.astype(np.int16)

    ### Run-Length Encoding (RLE)
    
    yRle  = run_length_encoding(yZigzag.flatten())
    cbRle = run_length_encoding(cbZigzag.flatten())
    crRle = run_length_encoding(crZigzag.flatten())

    ### Huffman encoding
    
    yCompressed, yHuffman_dict, yFreq = huffman_encoding(yRle)
    cbCompressed, cbHuffman_dict, cbFreq = huffman_encoding(cbRle)
    crCompressed, crHuffman_dict, crFreq = huffman_encoding(crRle)

    save_huffman_dict(yHuffman_dict, cbHuffman_dict, crHuffman_dict, OUTPUT_DIR)  # Saving the Huffman dictionaries in JSON format in the "output" directory

    ### Bitstream writing

    header = create_header(height, width, h_luma, w_luma, h_chroma, w_chroma, QLevel)  # create header with useful information for decoding (quality level, image size,...)
    write_to_file(header, yCompressed, crCompressed, cbCompressed, OUTPUT_DIR+"/compressed_data.bin")

    files = os.listdir(OUTPUT_DIR)  # check that the output files have been generated successfully...
    print("\nFiles correctly generated: ")
    for file in files:
        if file.endswith(".bin") or file.endswith(".json"):
            print("  -->", file)  #... and print them on the terminal

    ### Displaying some metrics (compression rate and execution time)

    total_number_of_bits_after_compression = os.path.getsize(OUTPUT_DIR+"compressed_data.bin")+os.path.getsize(OUTPUT_DIR+"yHuffman_dict.json")+os.path.getsize(OUTPUT_DIR+"cbHuffman_dict.json")+os.path.getsize(OUTPUT_DIR+"crHuffman_dict.json")
    print("\nNumber of bits after compression: ", total_number_of_bits_after_compression)
    
    compression_rate = (total_number_of_bits / total_number_of_bits_after_compression)
    print("Compression rate:  {:.2f}".format(compression_rate))

    end_time = time.time()  # stop timer
    execution_time = end_time - start_time
    print("Execution time:  {:.2f}sec".format(execution_time))

    view_huffman_stats(yFreq, yHuffman_dict, yRle, cbFreq, cbHuffman_dict, cbRle, crFreq, crHuffman_dict, crRle)  # print Huffman code statistics

    ### Different graphical analyses: save the graphs in the "analysis" directory

    viewing_dct_matrix(T, ANALYSE_DIR)
    viewing_zigzag_table(BLOCK_SIZE, BLOCK_SIZE, ANALYSE_DIR)
    viewing_quantization_matrix(Q_luma, 'luminance', ANALYSE_DIR)
    viewing_quantization_matrix(Q_chroma, 'chrominance', ANALYSE_DIR)
    viewing_luminance_and_chrominance_channels(y, cr, cb, ANALYSE_DIR)
    viewing_subsampled_channels(cr, crSub422, cb, cbSub422, ANALYSE_DIR)
    viewing_converted_picture_into_YCrCb_colorspace(img_ycrcb, ANALYSE_DIR)
    viewing_quantized_zigzaged_random_block(yQuantized, yZigzag, h_luma, w_luma, BLOCK_SIZE, ANALYSE_DIR)
    viewing_YCrCb_channels_after_DCT_and_quantization(yQuantized, crQuantized, cbQuantized, QLevel, ANALYSE_DIR)
    viewing_dct_for_a_random_selected_block(yDct, crDct, cbDct, h_luma, w_luma, h_chroma, w_chroma, BLOCK_SIZE, ANALYSE_DIR)
 