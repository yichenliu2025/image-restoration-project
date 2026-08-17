import cv2


class BilateralFilter:
    """
    Bilateral filter.

    Performs edge-preserving smoothing by considering
    both spatial distance and color/intensity difference.
    """

    @staticmethod
    def process(
        image,
        diameter,
        sigma_color,
        sigma_space
    ):
        return cv2.bilateralFilter(
            image,
            diameter,
            sigma_color,
            sigma_space
        )