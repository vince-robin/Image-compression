
def write_lines_to_file(data, filename: str, file_format: str = None):
    if file_format is not None and not filename.lower().endswith(file_format):
        if not file_format.startswith('.'):
            file_format = "." + file_format

        filename = filename.rstrip('.') + file_format

    with open(filename, 'w') as file:
        file.write(data)


def save_into_ppm(filename: str, type, width, height, depth, pixels):
 
    ppm_file_format = "{0}\n{1}\n{2}\n{3}"

    image_string = ""
    for line in pixels:
        for pixel in line:
            image_string += "{0}\n{1}\n{2}\n".format(pixel[0], pixel[1], pixel[2])

    ppm_image = ppm_file_format.format(type,"{0} {1}".format(width, height), depth, image_string)

    write_lines_to_file(ppm_image, filename, ".ppm")
