import cv2


class NonLocalMeansFilter:
    """
    Non-Local Means denoising.

    Searches for similar image patches within a larger
    search area and uses them to estimate a cleaner pixel.
    """

    @staticmethod
    def process(
        image,
        strength,
        color_strength,
        template_window,
        search_window
    ):
        return cv2.fastNlMeansDenoisingColored(
            image,
            None,
            strength,
            color_strength,
            template_window,
            search_window
        )