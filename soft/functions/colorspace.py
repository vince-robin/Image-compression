import numpy as np
import matplotlib.pyplot as plt


def rgb_to_ycrcb(im):
    
    xform = np.array([[.299, .587, .114], [.5, -.4187, -.0813], [-.1687, -.3313, .5]])
    ycbcr = im.dot(xform.T)
    ycbcr[:,:,[1,2]] += 128

    return np.uint8(ycbcr)


def ycrcb_to_rgb(im):

    xform = np.array([[1, 1.402, 0], [1, -.71414, -0.34414], [1, 0, 1.772]])
    rgb = im.astype(float) 
    rgb[:,:,[1,2]] -= 128
    rgb = rgb.dot(xform.T)
    np.putmask(rgb, rgb > 255, 255)
    np.putmask(rgb, rgb < 0, 0)
    
    return np.uint8(rgb)


def viewing_converted_picture_into_YCrCb_colorspace(img_YCrCb, out_dir):
    
    fig=plt.figure(figsize=(8,6))
    plt.title("Image originale (YUV)")
    plt.imshow(img_YCrCb)

    plt.savefig(out_dir+"original_picture_YCrCb.png")


def viewing_luminance_and_chrominance_channels(y, cr, cb, out_dir):
     
    fig=plt.figure(figsize=(10,4))
    fig.add_subplot(1, 3, 1)
    plt.title("Composante Y")
    plt.imshow(y)
    fig.add_subplot(1, 3, 2)
    plt.title("Composante Cr")
    plt.imshow(cr)
    fig.add_subplot(1, 3, 3)
    plt.title("Composante Cb")
    plt.imshow(cb)
    
    plt.savefig(out_dir+"luminance_and_chrominance_channels.png")


def viewing_subsampled_channels(cr, crSub422, cb, cbSub422, out_dir):

    fig=plt.figure(figsize=(12,7))
    fig.add_subplot(2, 2, 1)
    plt.title("Composante Cr")
    plt.imshow(cr)
    fig.add_subplot(2, 2, 2)
    plt.title("Composante Cr Sub 4:2:2")
    plt.imshow(crSub422)
    fig.add_subplot(2, 2, 3)
    plt.title("Composante Cb")
    plt.imshow(cb)
    fig.add_subplot(2, 2, 4)
    plt.title("Composante Cb Sub 4:2:2")
    plt.imshow(cbSub422)

    plt.savefig(out_dir+"subsampled_channels.png")


def viewing_luminance_and_chrominance_channels_decompressed(y, cr, cb, out_dir):
     
    fig=plt.figure(figsize=(10,4))
    fig.suptitle("Channels Y,Cr,Cb decompressed")
    fig.add_subplot(1, 3, 1)
    plt.imshow(y)
    fig.add_subplot(1, 3, 2)
    plt.imshow(cr)
    fig.add_subplot(1, 3, 3)
    plt.imshow(cb)
    
    plt.savefig(out_dir+"luminance_and_chrominance_channels_decompressed.png")
