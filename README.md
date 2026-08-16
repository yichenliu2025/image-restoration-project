# image-restoration-lab
A Python desktop application for exploring classical image filtering, image restoration, and super-resolution algorithms.
# Image Restoration & Super-Resolution Lab

A Python desktop application for exploring image filtering, restoration, and modern super-resolution techniques.

This project began as a rebuild of a series of image-processing experiments I originally created in high school using Python and OpenCV. The original scripts explored basic filtering methods such as mean, Gaussian, median, bilateral, and guided filtering.

The goal of this project is to gradually develop those experiments into a complete image restoration and super-resolution application, while comparing classical image-processing algorithms with modern deep-learning approaches.

## Current Version

**v0.1 - Basic Filtering GUI**

The first version establishes the basic desktop application and image-processing pipeline.

### Implemented

* PySide6 desktop GUI
* Local image loading
* Original and processed image comparison
* Mean Filter
* Gaussian Filter
* Median Filter
* Adjustable kernel size
* Adjustable Gaussian sigma
* Image export
* Automatic image scaling while preserving aspect ratio

## Algorithms

### Mean Filter

The mean filter replaces each pixel with the average value of the pixels inside its local neighbourhood.

It provides simple smoothing, but strong filtering can significantly blur edges and fine details.

### Gaussian Filter

The Gaussian filter performs weighted averaging using a Gaussian distribution.

Pixels near the centre of the kernel receive greater weight than pixels farther away. Both kernel size and Gaussian sigma affect the resulting smoothing behaviour.

### Median Filter

The median filter replaces each pixel with the median value of its neighbourhood.

It is particularly effective for removing impulse or salt-and-pepper noise while often preserving edges better than simple averaging.

## Project Structure

```text
image-restoration-lab/
│
├── main.py
├── requirements.txt
│
├── algorithms/
│   ├── mean_filter.py
│   ├── gaussian_filter.py
│   └── median_filter.py
│
├── app/
│   └── main_window.py
│
└── tools/
    └── environment_check.py
```

## Installation

Create a Python virtual environment and install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the application with:

```bash
python main.py
```

## Development Roadmap

### v0.2 - Advanced Traditional Filtering

Planned additions:

* Bilateral Filter
* Guided Filter
* Non-Local Means
* Dynamic algorithm parameter controls
* Improved image viewer
* Zoom and pan
* Synchronized original/result comparison

### Future Versions

Planned development includes:

* Bicubic image upscaling
* CNN-based super-resolution
* FSRCNN
* EDSR
* Real-ESRGAN
* SwinIR
* Algorithm comparison
* PSNR and SSIM benchmarking
* Performance comparison between CPU and GPU inference

## Long-Term Goal

The final application will provide a visual environment for comparing the progression from classical image filtering to modern image restoration and super-resolution methods.

The project is also intended to document the development process and the underlying principles of each algorithm as the software evolves.

## Status

🚧 **Under active development**
