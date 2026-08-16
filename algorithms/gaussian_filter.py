import cv2


class GaussianFilter:
    """
    Gaussian filter.

    Nearby pixels are averaged using weights based
    on a Gaussian distribution.

    Pixels closer to the centre of the kernel receive
    larger weights.
    """

    @staticmethod
    def process(image, kernel_size, sigma):
        return cv2.GaussianBlur(
            image,
            (kernel_size, kernel_size),
            sigmaX=sigma
        )