# install the library before executing code

import pyqrcode
import png
from pyqrcode import QRCode

a = "Like and Comment"  # string to show when QR Code will be scanned

url = pyqrcode.create(a)    # creating qr code

# save QR Code as svg and png files

url.svg("MyQRCode.svg", scale=8)    # svg file to maintain quality of code
url.png("MyQRCode.png", scale=6)    # png file to scan 

