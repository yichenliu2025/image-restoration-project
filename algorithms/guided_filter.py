import cv2
import numpy as np


class GuidedFilter:
    """
    Guided filter.

    Uses a guidance image to perform edge-preserving
    smoothing based on a local linear model.
    """

    @staticmethod
    def process(
        image,
        radius,
        epsilon
    ):
        # Convert image to floating point [0, 1].
        source = (
            image.astype(np.float32) / 255.0
        )

        # Use grayscale image as guidance.
        guide = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        guide = (
            guide.astype(np.float32) / 255.0
        )

        # Apply guided filter.
        filtered = cv2.ximgproc.guidedFilter(
            guide=guide,
            src=source,
            radius=radius,
            eps=epsilon
        )

        # Convert back to uint8.
        filtered = np.clip(
            filtered * 255.0,
            0,
            255
        )

        return filtered.astype(np.uint8)