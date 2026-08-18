import cv2


class BilinearUpscaler:
    """
    Image upscaling using bilinear interpolation.
    """

    @staticmethod
    def process(image, scale_factor):

        height, width = image.shape[:2]

        new_width = width * scale_factor
        new_height = height * scale_factor

        return cv2.resize(
            image,
            (new_width, new_height),
            interpolation=cv2.INTER_LINEAR
        )