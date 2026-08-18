# Image Restoration & Super-Resolution project

A Python desktop application for exploring classical image filtering, image restoration, and modern super-resolution techniques.

This project began as a rebuild of a series of image-processing experiments I originally created in high school using Python and OpenCV. The original scripts explored basic image-processing techniques such as mean, Gaussian, median, bilateral, and guided filtering.

The goal of this project is to gradually transform those early experiments into a complete image restoration and super-resolution application, while documenting the progression from classical image-processing algorithms to modern deep-learning approaches.

---

## Current Version

**v0.2 - Advanced Traditional Filtering**

Version 0.2 expands the original filtering application into a more complete traditional image-processing laboratory.

The application now provides six classical filtering and denoising methods, algorithm-specific parameter controls, synchronized image viewers, pixel-level zoom inspection, and processing-time measurement.

---

## Features

### Image Processing

* Mean Filter
* Gaussian Filter
* Median Filter
* Bilateral Filter
* Guided Filter
* Non-Local Means Denoising

### User Interface

* PySide6 desktop interface
* Local image loading
* Processed image export
* Original and processed image comparison
* Dynamic algorithm-specific parameter controls
* Mouse-wheel zoom
* Mouse-drag panning
* Synchronized Original / Processed viewers
* Fit-to-window mode
* 100% pixel view
* Processing runtime display
* Automatic image-position synchronization

---

## Algorithms

### Mean Filter

The Mean Filter replaces each pixel with the average value of the pixels inside its local neighbourhood.

All pixels within the kernel contribute equally to the output.

For a kernel of size `(2r + 1) x (2r + 1)`, the filtering operation can be written as:

$$ I_{\mathrm{out}}(x,y)=\frac{1}{(2r+1)^2}\sum_{i=-r}^{r}\sum_{j=-r}^{r}I(x+i,y+j) $$

where:

- `I(x, y)` is the original image intensity
- `r` determines the radius of the kernel
- `I_out(x, y)` is the filtered output

Because every pixel inside the neighbourhood receives the same weight, increasing the kernel size produces stronger smoothing.

A larger kernel therefore reduces more local variation, but also removes more fine image detail and softens edges.

**Main parameters:**

- Kernel Size

**Typical use:**

- Basic image smoothing
- Simple noise reduction
- Demonstrating spatial averaging

---

### Gaussian Filter

The Gaussian Filter performs weighted averaging using a Gaussian distribution.

Unlike the Mean Filter, neighbouring pixels do not contribute equally. Pixels closer to the centre of the kernel receive greater weight.

The two-dimensional Gaussian weighting function is:

$$ G(x,y)=\frac{1}{2\pi\sigma^2}\exp\left(-\frac{x^2+y^2}{2\sigma^2}\right) $$

The filtered image is obtained by convolving the original image with the Gaussian kernel:

$$ I_{\mathrm{out}}(x,y)=\sum_i\sum_jG(i,j)\,I(x-i,y-j) $$

where:

- `G(i, j)` is the Gaussian kernel weight
- `sigma` controls the spread of the Gaussian distribution
- `I(x, y)` is the original image
- `I_out(x, y)` is the filtered image

A small `sigma` concentrates most of the weight near the centre of the kernel.

A larger `sigma` spreads the weight across a wider area, resulting in stronger smoothing.

This also explains why increasing the kernel size alone may not significantly increase blur if `sigma` remains small.

**Main parameters:**

- Kernel Size
- Sigma

**Typical use:**

- Gaussian noise reduction
- Image smoothing
- Pre-processing for other computer-vision algorithms

---

### Median Filter

The Median Filter replaces each pixel with the median value inside its local neighbourhood.

Unlike Mean and Gaussian filtering, it does not calculate an average.

The operation can be represented as:

$$ I_{\mathrm{out}}(x,y)=\underset{(i,j)\in\Omega}{\mathrm{median}}\left[I(x+i,y+j)\right] $$

where:

- `Omega` represents the local neighbourhood around the current pixel
- `I(x + i, y + j)` represents the pixel values inside that neighbourhood
- The median is the middle value after all neighbourhood values are ordered

For example, consider the following neighbourhood values:

```text
10, 11, 10, 12, 255, 9, 10, 11, 10
```


## Image Viewer

Version 0.2 introduces a new image viewer based on `QGraphicsView`.

The viewer provides significantly more control than the basic image display used in v0.1.

### Zoom

The mouse wheel can be used to zoom into or out of the image.

This is particularly useful when examining pixel-level differences between filtering algorithms.

### Pan

When an image is enlarged beyond the viewer window, the image can be moved by clicking and dragging with the mouse.

### Fit Mode

The **Fit** button automatically scales the image so that the entire image remains visible while preserving its aspect ratio.

### 100% View

The **100%** button displays the image at its actual pixel size:

```text
1 image pixel = 1 screen pixel
```

This makes it possible to inspect image-processing results without the additional smoothing introduced by display scaling.

### Synchronized Viewers

The Original and Processed viewers can be synchronized.

When synchronization is enabled:

* Zooming one viewer zooms the other
* Panning one viewer moves the other
* Both viewers remain focused on approximately the same image region

The synchronization system uses normalized image coordinates rather than absolute scrollbar positions.

This design is important for future super-resolution algorithms, where the processed image may have a much higher resolution than the original image.

---

## Processing Runtime

Version 0.2 measures the execution time of each filtering operation.

The runtime is displayed in the application status bar after processing.

Example:

```text
Non-Local Means completed | 2560 × 1013 | 2.431 s
```

This feature will later be expanded into a more complete benchmarking system for comparing traditional filters and deep-learning super-resolution models.

---

## Project Structure

```text
image-restoration-lab/
│
├── main.py
├── requirements.txt
│
├── algorithms/
│   ├── __init__.py
│   ├── mean_filter.py
│   ├── gaussian_filter.py
│   ├── median_filter.py
│   ├── bilateral_filter.py
│   ├── guided_filter.py
│   └── non_local_means.py
│
├── app/
│   ├── __init__.py
│   ├── main_window.py
│   └── image_viewer.py
│
└── tools/
    └── environment_check.py
```

The project uses a modular structure so that image-processing algorithms remain separated from the graphical user interface.

This architecture will allow future super-resolution algorithms to be added without redesigning the entire application.

---

## Requirements

The current version uses:

* Python 3.10+
* NumPy
* OpenCV Contrib
* Pillow
* PySide6

The current development environment uses:

```text
numpy==2.2.6
opencv-contrib-python==5.0.0.93
Pillow==12.3.0
PySide6==6.11.1
```

---

## Installation

Clone or download the repository.

Create a Python virtual environment:

```bash
python -m venv .venv
```

Activate the environment and install the required dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

---

## Development History

### v0.1 - Basic Filtering GUI

The first working version established the basic desktop application and image-processing pipeline.

Implemented:

* PySide6 desktop GUI
* Local image loading
* Image export
* Original / Processed comparison
* Mean Filter
* Gaussian Filter
* Median Filter
* Adjustable kernel size
* Adjustable Gaussian sigma

This version transformed the original standalone OpenCV experiments into a modular desktop application.

---

### v0.2 - Advanced Traditional Filtering

Version 0.2 completes the main traditional filtering stage of the project.

New algorithms:

* Bilateral Filter
* Guided Filter
* Non-Local Means

New application features:

* Dynamic parameter panels
* Dedicated `QGraphicsView` image viewer
* Mouse-wheel zoom
* Mouse-drag panning
* Synchronized Original / Processed navigation
* Fit-to-window mode
* 100% pixel inspection
* Normalized image-position synchronization
* Processing runtime measurement
* Expanded algorithm descriptions

This version establishes the viewer and application architecture that will be reused when super-resolution algorithms are introduced.

---

## Development Roadmap

### Completed

* [x] v0.1 - Basic Filtering GUI
* [x] v0.2 - Advanced Traditional Filtering

### Next: v0.3 - Image Upscaling & Super-Resolution Foundations

The next stage will begin the transition from traditional image filtering to image upscaling and super-resolution.

Planned topics include:

* Bicubic interpolation
* Resolution scaling
* 2× and 4× image upscaling
* Original / Upscaled comparison
* Resolution and scale-factor display
* Traditional interpolation baseline
* Preparation for neural-network super-resolution models

### Future Development

Later versions are planned to explore:

* FSRCNN
* EDSR
* Real-ESRGAN
* SwinIR
* Additional modern super-resolution models
* Multi-algorithm comparison mode
* PSNR benchmarking
* SSIM benchmarking
* CPU / GPU performance comparison
* NVIDIA CUDA acceleration
* Model management
* Advanced image restoration
* Final polished desktop interface

---

## Long-Term Goal

The long-term goal of this project is to create a complete visual environment for studying the progression of image-restoration techniques:

```text
Classical Filtering
        ↓
Image Interpolation
        ↓
CNN Super-Resolution
        ↓
Residual Networks
        ↓
GAN-Based Restoration
        ↓
Transformer Super-Resolution
```

The final application is intended to serve both as a practical image-restoration tool and as a record of the learning process behind each algorithm.

---

## Project Origin

This project originated from a collection of Python and OpenCV experiments I created while learning image processing in high school.

Those early programs explored individual filtering techniques using simple scripts and basic image display methods.

Several years later, the project was rebuilt from the ground up as a structured desktop application.

Rather than replacing the original ideas, the current project uses them as the starting point for exploring the development of modern image-restoration and super-resolution techniques.

---

## Status

**v0.2 complete**

Traditional image-filtering stage completed.

Next milestone:

**v0.3 - Image Upscaling & Super-Resolution Foundations**
