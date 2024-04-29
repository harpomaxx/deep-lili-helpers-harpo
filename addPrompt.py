#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont
import os
import sys

# some color helper globals
WHITE = (255, 255, 255, 0)
BLACK = (0, 0, 0, 0)

def drawTextOnImg(text, imgSize):
    """
    Creates a new image with text.

    Args:
        text (str): the text to put into the image
        imgSize (tuple): the size of the image

    Returns:
        New image created.
    """

    image = Image.new("RGB", imgSize, WHITE)
    font = ImageFont.truetype("DejaVuSans.ttf", size=24)
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=font, fill=BLACK)

    return image

def combineImageWithText(imagePath, text, outPath):
    """
    Combines a PNG image and text into a new image.

    Args:
        imagePath (str): The path to the PNG image.
        text (str): The text to be added to the image.
        outPath (str): The path to save the new image.

    Returns:
        Nothing, creates a new image on disk.
    """

    image = Image.open(imagePath)
    # calculate new image with prompt added size
    textImgSizeY = int(image.size[1] * 0.33)
    newSizeY = image.size[1] + textImgSizeY
    textImgSize = (image.size[0], textImgSizeY)
    newImgSize = (image.size[0], newSizeY)

    # Create a new image to hold original and new image with text
    newImage = Image.new("RGBA", newImgSize)

    textImg = drawTextOnImg(text, textImgSize)

    # combine both images into the new one
    newImage.paste(image, (0, 0))
    newImage.paste(textImg, (0, image.size[1]))

    newImage.save(outPath)

def readTextFile(filePath):
    """
    Reads the contents of a text file and saves it into a variable.

    Args:
        filePath (str): The path to the text file.

    Returns:
        str: The contents of the text file.
    """
    with open(filePath, 'r') as file:
        fileContents = file.read()

    return fileContents

import os

def getFolderListing(folderPath):
    """
    Gets a list of all folders in the specified directory, ignoring files.

    Args:
        folderPath (str): the path to the folder containing the data.

    Returns:
        folder listing of folders, omitting all files.
    """

    result = []
    folderListing = os.listdir(folderPath)

    for fileName in folderListing:
        path = os.path.join(folderPath, fileName)
        if os.path.isdir(path):
            result.append(path)

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <basePath>")
        sys.exit(1)

    basePath = sys.argv[1]
    folders = getFolderListing(basePath)

    for folder in folders:
        imgPath = os.path.join(folder, "image.png")
        promptPath = os.path.join(folder, "prompt.txt")
        outPath = os.path.join(folder, "output.png")
        promptText = readTextFile(promptPath)
        combineImageWithText(imgPath, promptText, outPath)
