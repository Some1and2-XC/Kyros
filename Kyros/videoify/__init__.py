#!/usr/bin/env python3

import cv2
import numpy as np
import glob
import re

from ..ExecTime import ExecTime
from .. import printutils as pu

class videoify:

    def __init__(self, name):
        # Name usually has part of a file path in it (ex: path\\path)
        self.name = name

    @ExecTime
    def save(self):
        pu.line()

        ImageArray = []

        # Goes through all the file names and adds them to the `ImageArray` list in proper order
        for filename in sorted(glob.glob(f"{self.name}*.png"), key=self.SortByNumber):
            img = cv2.imread(filename)
            ImageArray.append(img)
            pu.InfoOut(" - IMPORTING : {file}".format(file=filename.split("\\")[-1]), end="\r")

        # Uses the fact that img is a numpy array (`cv2.imread()` returns numpy array)
        # to get parameters to get the shape of the array
        height, width, _ = img.shape
        size = (width, height)

        up.InfoOut()
        pu.line()

        # AVC3 uses the HEVC codec or H.264
        # To make this codec work correctly, the `.dll` file is required (cv2 gets angry without it)
        CodecFilename = "openh264-1.8.0-win64.dll"
        try:
            # Tries to open .dll file to try and use H.264 codec
            with open(CodecFilename, "rb") as file:
                file.close()
            codec = "avc3"
        except FileNotFoundError:
            # On exception uses builtin codec
            pu.InfoOut(f"\nExporting with `mp4v`, add {CodecFilename} near main file")
            codec = "mp4v"

        video = cv2.VideoWriter(f"{self.name} - {codec.upper()}.mp4", cv2.VideoWriter_fourcc(*codec), 25, size)

        # Add each Image in `ImageArray` to the video output file
        for image in [*ImageArray[0:], *ImageArray[-2:0:-1]]:
            video.write(image)
        video.release()

    def SortByNumber(self, value):
        # Function for sorting through the image files by the numbers in
        # The file name between `#` & `.`
        parts = re.findall(r"#[0-9]+.", value)[0][1:-1]
        parts = [int(parts)]
        parts[1::2] = map(int, parts[1::2])
        return parts
