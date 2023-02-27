import array
import numpy as np


def write_to_file(header,channelY, channelCr, channelCb, name):

    data = header + channelY + channelCr + channelCb

    missing_bits = (8 - (len(data)+3+20+20+20))%8 
    needed_bits = missing_bits

    while needed_bits > 0:
        data+='0'
        needed_bits-=1

    missing_bits = '{0:03b}'.format(missing_bits)
    len_channelY = '{0:020b}'.format(len(channelY))
    len_channelCr = '{0:020b}'.format(len(channelCr))
    len_channelCb = '{0:020b}'.format(len(channelCb))

    data = missing_bits + len_channelY + len_channelCr + len_channelCb + data

    data = np.array(list(data))
    message = data.reshape(int(data.shape[0]/8), 8)
    file = array.array('B')

    for msg in range(len(message)):
        str_message = ''.join(message[msg]) 
        bin_message = int(str_message, 2)
        file.append(bin_message)

    f = open(name, 'wb')
    file.tofile(f)
    f.close()


def read_from_file(name):
    
    file = np.fromfile(name, dtype=np.uint8)
    
    bits_list = ['{0:08b}'.format(value) for value in file]
    bits = ''.join(bits_list)
   
    padding = int(bits[0:3], 2)
    len_channelY = int(bits[3:23], 2)
    len_channelCr = int(bits[23:43], 2)
    len_channelCb = int(bits[43:63], 2)

    header = bits[63:len(bits)-len_channelY-len_channelCr-len_channelCb-padding]
    channelY = bits[63+73: len(bits)-len_channelCr-len_channelCb-padding]  # adding the size of the header (=73)
    channelCr = bits[63+73+len_channelY : len(bits)-len_channelCb-padding]
    channelCb = bits[63+73+len_channelY+len_channelCr : len(bits)-padding]

    return header, channelY, channelCr, channelCb


def create_header(h_original, w_original, h_luma, w_luma, h_chroma, w_chroma, quality):
     
    h_original_img_bin = '{0:011b}'.format(h_original)  # 11 bits allow for an image size of up to 2048
    w_original_img_bin = '{0:011b}'.format(w_original)
    h_luma_bin = '{0:011b}'.format(h_luma)              
    w_luma_bin = '{0:011b}'.format(w_luma) 
    h_chroma_bin = '{0:011b}'.format(h_chroma) 
    w_chroma_bin = '{0:011b}'.format(w_chroma) 
    quality_bin = '{0:07b}'.format(quality)             # 7 bits are sufficient because max quantization level is 99

    header = h_original_img_bin+w_original_img_bin+h_luma_bin+w_luma_bin+h_chroma_bin+w_chroma_bin+quality_bin

    return header


def read_header(header):

    height = int(header[0:11], 2)
    width = int(header[11:22], 2)
    h_luma = int(header[22:33], 2)
    w_luma = int(header[33:44], 2)
    h_chroma = int(header[44:55], 2)
    w_chroma = int(header[55:66], 2)
    QLevel = int(header[66:73], 2)

    return height, width, h_luma, w_luma, h_chroma, w_chroma, QLevel