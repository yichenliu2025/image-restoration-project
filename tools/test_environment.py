import sys
import cv2
import numpy
from PIL import Image
import PySide6


print("=" * 60)

print("Python executable:")
print(sys.executable)

print()

print("Python version:")
print(sys.version)

print()

print("OpenCV:", cv2.__version__)
print("NumPy:", numpy.__version__)
print("Pillow:", Image.__version__)
print("PySide6:", PySide6.__version__)

print()

print(
    "OpenCV ximgproc available:",
    hasattr(cv2, "ximgproc")
)

print("=" * 60)