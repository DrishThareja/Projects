# 1st pic = MyQRCode.png
# 2nd pic = A.png
# 3rd pic = B.jpg
# 4th pic = C.png
# 5th pic = D.jpg
# 6th pic = MyQRCode.svg

# import the FPDF class from the fpdf library
from fpdf import FPDF

# create an object of the FPDF class to generate a PDF
pdf = FPDF()

# List of image files
# copy image name 
image_list = ["MyQRCode.png", "A.png", "B.jpg", "C.png", "D.jpg", "MyQRCode.svg"]
# It doesn't matter what is the file extension if it can be change 
# to pdf it will be converted 

# set the top - left corner (x , y coordinates )
x, y = 10, 10

# set the width and height
w, h = 190, 277

# Loop to add image to the pdf
for image in image_list:
    pdf.add_page()
    pdf.image(image, x, y, w, h)    

# save the pdf to local system with name of ur choice
pdf.output("Project_4.pdf")
