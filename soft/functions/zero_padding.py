import numpy as np 
from math import ceil
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw


def make_zero_padding(y, crSub, cbSub, blockSize):

    # Process for luminance (Y)                
    h_luma, w_luma = y.shape   # number of blocks in height and width : nbh et nbw
    nbh_luma = ceil(h_luma / blockSize)  
    nbw_luma = ceil(w_luma / blockSize)
    hPadded_luma = blockSize * nbh_luma  # height and width of padded image: hPadded, wPadded
    wPadded_luma = blockSize * nbw_luma

    if (h_luma % blockSize == 0) and (w_luma % blockSize == 0):
        print("Zero padding: not required")
        yPadded = y.copy()
    else:
        print("Zero padding: is required")
        yPadded = np.zeros((hPadded_luma, wPadded_luma))
        for i in range(h_luma):
            for j in range(w_luma):
                yPadded[i, j] += y[i, j]

    # Process for chrominance (Cr,Cb)
    h_chroma, w_chroma = cbSub.shape  # or crSub.shape because the chrominance signals have the same dimensions
    nbh_chroma = ceil(h_chroma / blockSize)
    nbw_chroma = ceil(w_chroma / blockSize)
    hPadded_chroma = blockSize * nbh_chroma
    wPadded_chroma = blockSize * nbw_chroma

    if (h_chroma % blockSize == 0) and (w_chroma % blockSize == 0):
        crPadded = crSub.copy()
        cbPadded = cbSub.copy()
    else:
        crPadded = np.zeros((hPadded_chroma, wPadded_chroma))
        cbPadded = np.zeros((hPadded_chroma, wPadded_chroma))
        for i in range(h_chroma):
            for j in range(w_chroma):
                crPadded[i, j] += crSub[i, j]
                cbPadded[i, j] += cbSub[i, j]

    return yPadded, crPadded, cbPadded, nbh_luma, nbw_luma, nbh_chroma, nbw_chroma, hPadded_luma, wPadded_luma, hPadded_chroma, wPadded_chroma



def viewing_blocks(image, h, w, blocksize, output_dir):

    image=image[:h,:w]
    PIL_image = Image.fromarray(np.uint8(image))
    draw = ImageDraw.Draw(PIL_image)
    y_start = 0
    y_end = PIL_image.height

    for x in range(0, PIL_image.width, blocksize):
        line = ((x, y_start), (x, y_end))
        draw.line(line, fill=(255,255,255))

    x_start = 0
    x_end = PIL_image.width

    for y in range(0, PIL_image.height, blocksize):
        line = ((x_start, y), (x_end, y))
        draw.line(line, fill=(255,255,255))
    
    #print("Number of rows: {}, Number of cols: {}".format(int(y_end/blocksize),int(x_end/blocksize)))
    plt.title("Image split into blocks\n N_rows={0}, N_cols={1}".format(int(y_end/blocksize),int(x_end/blocksize)))
    plt.imshow(PIL_image)
    
    plt.savefig(output_dir+"image_splitted_into_blocks.png")