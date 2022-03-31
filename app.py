from pdf2image import convert_from_path
import os
import tempfile
from PIL import Image
from docx2pdf import convert

def converts (inDir, outDir):
    if not os.path.exists(outDir):
        os.makedirs(outDir)

    for file in os.listdir(inDir):
        extention = (file.split(".")[-1]).upper()
        if extention == 'PDF':
            convertPdf(inDir + file, outDir, file)
        elif extention == 'DOCX':
            convertToPDF(inDir + file, outDir, file)


def convertPdf (filePath, outDir, fileName):
    with tempfile.TemporaryDirectory() as tempDir:
        images = convert_from_path(filePath, output_folder=tempDir)
        tempImages = []
        for i in range(len(images)):
            imagePath = f'{tempDir}/{i}.png'
            images[i].save(imagePath, 'PNG')
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

    mergedImage.save(f'{outDir}{fileName}.png')

    return outDir

def convertToPDF(filePath, outDir, fileName):
    # outFileName=fileName.replace("docx","pdf")
    inputFile = "./src/docxToPDF.docx"
    outputFile = "./result/docxToPDF.pdf"
    file = open(outputFile, "w")
    file.close()

    convert(inputFile, outputFile)
    # convert('./src/docxToPDF.docx', './result/docxToPDF.pdf')

outDir = "./result/"
inDir = "./src/"

converts(inDir, outDir)