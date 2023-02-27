import numpy as np


def snr(original_img, decompressed_img):

    signal_power = np.sum(original_img.astype("float")**2)
    noise_power = np.sum((original_img.astype("float") - decompressed_img.astype("float")) ** 2)
    snr = 10 * np.log10(signal_power / noise_power)
    
    return snr


def mse(imageA, imageB):
    
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    return err
