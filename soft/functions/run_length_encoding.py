
def run_length_encoding(image):
    
    i = 0
    skip = 0
    stream = []    
    while i < image.shape[0]:
        if image[i] != 0:     
            stream.append((image[i],skip))   
            skip = 0
        else:
            skip = skip + 1
        i = i + 1

    return stream


def run_length_decoding(encoded, h, w):
    
    i = 0
    skip = 0
    image = []
    while i != len(encoded):
        if encoded[i][1] != 0:
            while skip != (encoded[i][1]):
                image.append(0)
                skip = skip + 1
        image.append(encoded[i][0])
        i = i + 1
        skip = 0
    
    if i == len(encoded):
        for _ in range(0, ((h*w)-len(image))):
            image.append(0)

    return image
