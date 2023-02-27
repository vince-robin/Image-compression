'''
Project Name: Video compression

Student: Vincent ROBIN, ENSTA Bretagne, promotion 2023
Contact: vincent.robin@ensta-bretagne.org

File name: drawingShape.py 
Create Date: 11/19/2022, 11:19:41 AM

Description: draws a shape in a .ppm file. The image display can be done directly 
in the Python script with the OpenCV2 library, or by opening the ppm file with a utility 
such as IrfanView (download it here: https://www.irfanview.com/)

Packages: 
  - cv2 (pip install opencv-python)

Revision: Revision 0.01 - File Created
Additional Comments:

'''

import cv2    # to read and display the generated ppm image


# some uesefuls colours
BLACK   = (0,0,0)
WHITE   = (255,255,255)
RED     = (255,0,0)
GREEN   = (0,255,0)
BLUE    = (0,0,255)
CYAN    = (0,255,255)
YELLOW  = (255,255,0)
MAGENTA = (255,0,255)
PURPLE  = (127,0,255)
GRAY    = (127,127,127)
ORANGE  = (255,127,0)


'''
Draws circle for a given colors, and ray
'''
def circle(file, color, width, height, ray=0):

    abscisse = width//2     # abscissa of the centre of the circle
    ordinate = height//2    # ordinate of the centre of the circle
    b=int((ray+0.5)**2)     # maximum distance between a pixel and the centre

    for i in range(height):        
        for j in range(width):    
            if (j-abscisse)**2+(i-ordinate)**2 in range(0,b): 
                file.write('{0} {1} {2} \n'.format(color[0], color[1], color[2]))     
            else :
                file.write('{0} {1} {2} \n'.format(WHITE[0], WHITE[1], WHITE[2]))   

'''
Draws a colour gradient like a rainbow
'''
def rainbow(file, width, height):

    for line in range(height):
        for x in range(width):
            if (0 <= x) and (x <= 209):
                r, v, b = 255, x, 0
            elif (210 <= x) and (x <= 419):
                r, v, b = 419-x, 255, 0
            elif (420 <= x) and (x <= 629):
                r, v, b = 0, 255, x-420
            elif (630 <= x) and (x <= 839):
                r, v, b = 0, 839-x, 255
            else:
                r, v, b = x-840, 0, 255

            file.write('{} {} {} \n'.format(r, v, b))
        file.write('\n')

'''
Draws the test pattern used in television domain
'''
def mire(file, l, h):
    
    colors = [WHITE, YELLOW, CYAN, GREEN, MAGENTA, RED, BLUE, BLACK]

    for line in range(h):
        for x in range(l):
            for j in range(0,8):
                if (j*(l//8) <= x) and (x <= (j+1)*(l//8)):
                    color = colors[j]
            file.write('{}\n'.format(color[0]))
            file.write('{}\n'.format(color[1]))
            file.write('{}\n'.format(color[2]))


if __name__ == '__main__':

    WIDTH, HEIGHT = 840, 640	# VGA output format (840x640)
    PATH ='output.ppm'          # path of the ppm file we will generate on the current repository

    # Shape selection by the user in the terminal
    picture_choice = 0
    print("\nPlease select a shape to drawing between from these 3 choices: \n --> TV test pattern (1) \n --> Red Circle (2) \n --> Rainbow (3)\n")
    picture_choice = input("Your choice : \t")
    picture_choice = int(picture_choice)  # cast into integer! The user entry is in str() type by default with input() function

    # manage wrong choices
    while (picture_choice > 3) or (picture_choice < 1):
        print("\nYour choice is invalid: please retry with a number between 1 and 3!")
        picture_choice = input("Your choice : \t")   # ask to choose again
        picture_choice = int(picture_choice)  # cast into integer! The user entry is in str() type by default with input() function
   
    f = open(PATH, 'w')

    # writing the header of the ppm file
    f.write('P3\n')						      # magic number 'P3' on line 1 to declare the .ppm format then move to line
    f.write('# PPM file generation\n')        # comment
    f.write('{} {}\n'.format(WIDTH, HEIGHT))  # width and height of the image, separated by a space
    f.write('255\n')						  # maximum intensity of the RGB components
    
    # drawing the shape
    if picture_choice == 1:
        mire(f, WIDTH, HEIGHT)
    elif picture_choice == 2:
        circle(f, RED, WIDTH, HEIGHT, ray=100)
    else:
        rainbow(f, WIDTH, HEIGHT)

    f.close()

    generated_ppm_frame = cv2.imread('output.ppm')          # reads the generated ppm file with OpenCV2
    cv2.imshow('generated_ppm_frame', generated_ppm_frame)  # displays the generated ppm file with OpenCV2

    cv2.waitKey(0)
    cv2.destroyAllWindows()