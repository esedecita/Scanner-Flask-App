from PIL import Image
im = Image.open("C:/Users/gpatil/Desktop/Scanner Flask App/static/images/2016-06-27_12-56-08.png")
im = im.rotate(-90, expand=True)
im.save("out.png")