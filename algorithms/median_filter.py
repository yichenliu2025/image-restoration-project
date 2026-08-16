import cv2


class MedianFilter:
    """
    Median filter.

    Replaces each pixel with the median value inside
    its neighbourhood.

    Particularly effective for salt-and-pepper noise.
    """

    @staticmethod
    def process(image, kernel_size):
        return cv2.medianBlur(
            image,
            kernel_size
        )