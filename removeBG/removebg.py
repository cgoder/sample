from rembg import remove
from PIL import Image

input = Image.open('winnie.jpg')
output = remove(input)
output.save('winnie.png')