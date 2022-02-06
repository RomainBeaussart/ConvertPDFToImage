from pdf2image import convert_from_path
import os
import tempfile
from pdf2image import convert_from_path
from PIL import Image

def convert (inDir, outDir):
    if not os.path.exists(outDir):
        os.makedirs(outDir)

    for file in os.listdir(inDir):
        convertPdf(inDir + file, outDir, file)


def convertPdf(filePath, outDir, fileName):
    with tempfile.TemporaryDirectory() as tempDir:
        images = convert_from_path(filePath, output_folder=tempDir)
        tempImages = []
        for i in range(len(images)):
            imagePath = f'{tempDir}/{i}.jpg'
            images[i].save(imagePath, 'JPEG')
            tempImages.append(imagePath)

        imgs = list(map(Image.open, tempImages))

    minImgWidth = min(i.width for i in imgs)
    totalHeight = 0
    for i, img in enumerate(imgs):
        totalHeight += imgs[i].height

    mergedImage = Image.new(imgs[0].mode, (minImgWidth, totalHeight))
    y = 0
    for img in imgs:
        mergedImage.paste(img, (0, y))
        y += img.height

    mergedImage.save(f'{outDir}{fileName}.jpg')

    return outDir


outDir = "./imgs/"
inDir = "./pdfs/"

convert(inDir, outDir)