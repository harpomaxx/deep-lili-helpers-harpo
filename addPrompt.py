#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont
from hyphen.textwrap2 import fill
from hyphen import Hyphenator
import os
import sys
import semchunk
import argparse
from tqdm import tqdm


# some color helper globals
WHITE = (255, 255, 255, 0)
BLACK = (0, 0, 0, 0)
GREEN = (0, 128, 0)
YELLOW = (255, 255, 0)
RED = (252, 65, 0)
YELLOW2 = (255, 197, 90)
BLUE = (0, 33, 94)
BROWN = (50, 1, 47)
LIGHT_WHITE = (226, 223, 208)
ORANGE = (249, 115, 0)


def drawTextOnImg(text, imgSize):
    """
    Creates a new image with text.

    Args:
        text (str): the text to put into the image
        imgSize (tuple): the size of the image

    Returns:
        New image created.
    """

    image = Image.new("RGB", imgSize, BROWN)
    font = ImageFont.truetype("DejaVuSans.ttf", size=22)
    font_big = ImageFont.truetype("Ubuntu-B.ttf", size=32)
    draw = ImageDraw.Draw(image)
    #print(imgSize)
    text = text[:-10]
    h_es = Hyphenator("es_ES")
    if len(text) > 150:
        text = text[:150] + "..."
    wrapped_text = fill(text,width=39,use_hyphenator=h_es)
    #print(wrapped_text)

    draw.text((10, 10), '"'+wrapped_text+'"', font=font, fill=LIGHT_WHITE,align='center')
    draw.text((345, 120), "deeplili.co", font=font_big, fill=ORANGE)


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
    parser = argparse.ArgumentParser(description="Process some folders.")
    parser.add_argument("--basePath", help="Base path to the folders")
    parser.add_argument("--force", action="store_true", help="Force the generation of output.png even if it exists")

    args = parser.parse_args()

    basePath = args.basePath
    folders = getFolderListing(basePath)

    for folder in tqdm(folders, desc="Processing folders"):
        imgPath = os.path.join(folder, "image.png")
        promptPath = os.path.join(folder, "prompt.txt")
        outPath = os.path.join(folder, "output.png")

        # Check if output exists and handle based on --force flag
        if not os.path.exists(outPath) or args.force:
            promptText = readTextFile(promptPath)
            combineImageWithText(imgPath, promptText, outPath)
        else:
            print(f"Skipping {outPath} as it already exists. Use --force to override.")
