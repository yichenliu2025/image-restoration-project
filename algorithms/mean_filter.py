import cv2


class MeanFilter:
    """
    Mean / Box filter.

    Each output pixel is calculated as the average
    of the neighbouring pixels inside the kernel.
    """

    @staticmethod
    def process(image, kernel_size):
        return cv2.blur(
            image,
            (kernel_size, kernel_size)
        )