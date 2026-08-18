# Image Restoration & Super-Resolution project

A Python desktop application for exploring classical image filtering, image restoration, and modern super-resolution techniques.

This project began as a rebuild of a series of image-processing experiments I originally created in high school using Python and OpenCV. The original scripts explored basic image-processing techniques such as mean, Gaussian, median, bilateral, and guided filtering.

The goal of this project is to gradually transform those early experiments into a complete image restoration and super-resolution application, while documenting the progression from classical image-processing algorithms to modern deep-learning approaches.

---

## Current Version **v0.3 - Image Upscaling & Super-Resolution Foundations** 
Version 0.3 introduces the first image-upscaling stage of the project. 
The application now supports four traditional interpolation methods and allows images to be enlarged by 2x, 3x, or 4x while comparing the original and processed images at different resolutions. 
This version establishes the traditional interpolation baseline that will later be used to compare classical upscaling against neural-network super-resolution models.

---

## Features

### Image Processing

* Mean Filter
* Gaussian Filter
* Median Filter
* Bilateral Filter
* Guided Filter
* Non-Local Means Denoising

### Image Upscaling 
- Nearest Neighbor Interpolation
- Bilinear Interpolation
- Bicubic Interpolation
- Lanczos Interpolation
- 2x image upscaling
- 3x image upscaling
- 4x image upscaling
- Automatic target-resolution calculation
- Original and processed resolution display
- Different-resolution synchronized comparison

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

### Bilateral Filter

The Bilateral Filter performs edge-preserving smoothing.

Unlike Gaussian Filtering, the weight assigned to neighbouring pixels depends on both their spatial distance and their color or intensity difference.

The filtered value at pixel `p` can be written as:

$$ I_{\mathrm{out}}(p)=\frac{1}{W_p}\sum_{q\in\Omega}w(p,q)\,I(q) $$

The bilateral weight is:

$$ w(p,q)=\exp\left(-\frac{\|p-q\|^2}{2\sigma_{\mathrm{space}}^2}\right)\exp\left(-\frac{\|I(p)-I(q)\|^2}{2\sigma_{\mathrm{color}}^2}\right) $$

The normalization factor is:

$$ W_p=\sum_{q\in\Omega}w(p,q) $$

The first exponential term represents **spatial similarity**.

Pixels that are farther away from the centre pixel receive less weight.

The second exponential term represents **color or intensity similarity**.

Pixels that have very different colors receive less influence even if they are physically close.

As a result, neighbouring pixels located on opposite sides of a strong edge have less influence on each other.

This allows the Bilateral Filter to smooth relatively uniform image regions while preserving important edges.

**Main parameters:**

- Diameter
- Sigma Color
- Sigma Space

**Diameter** controls the size of the neighbourhood used during filtering.

**Sigma Color** controls how different pixel colors may be while still influencing each other.

**Sigma Space** controls how far spatial influence extends.

**Typical use:**

- Edge-preserving smoothing
- Noise reduction
- Surface smoothing
- Image enhancement

---

### Guided Filter

The Guided Filter is an edge-preserving filtering technique based on a local linear model.

Instead of directly defining spatial and color weights, the Guided Filter assumes that the output image has a locally linear relationship with a guidance image.

Inside a local window:

$$ q_i=a_kI_i+b_k $$

where:

- `q_i` is the filtered output
- `I_i` is the guidance image
- `a_k` and `b_k` are locally estimated coefficients

The coefficient `a_k` can be written as:

$$ a_k=\frac{\frac{1}{|\omega_k|}\sum_{i\in\omega_k}I_ip_i-\mu_k\bar{p}_k}{\sigma_k^2+\epsilon} $$

The second coefficient is:

$$ b_k=\bar{p}_k-a_k\mu_k $$

where:

- `p` is the input image being filtered
- `mu_k` is the local mean of the guidance image
- `sigma_k^2` is the local variance of the guidance image
- `p_bar_k` is the local mean of the input image
- `epsilon` is a regularization parameter
- `omega_k` represents the local window

In the current implementation, a grayscale representation of the original image is used as the guidance image.

The local linear relationship allows the filter to smooth image regions while preserving important structural boundaries.

The `epsilon` parameter also prevents instability when the local variance is very small and influences the balance between smoothing and edge preservation.

**Main parameters:**

- Radius
- Epsilon

**Radius** controls the size of the local region used to estimate the linear model.

**Epsilon** controls the regularization strength and influences the balance between smoothing and edge preservation.

**Typical use:**

- Edge-preserving smoothing
- Detail enhancement
- Image restoration
- Structure-aware filtering

---

### Non-Local Means

Non-Local Means uses a fundamentally different approach from traditional local filters.

Instead of estimating a pixel only from immediately neighbouring pixels, the algorithm searches a larger region for image patches with similar structure.

The estimated value of a pixel `p` can be expressed as:

$$ I_{\mathrm{out}}(p)=\frac{1}{Z(p)}\sum_{q\in\Omega}w(p,q)\,I(q) $$

The normalization factor is:

$$ Z(p)=\sum_{q\in\Omega}w(p,q) $$

The similarity weight between two image patches can be represented as:

$$ w(p,q)=\exp\left(-\frac{\|P(p)-P(q)\|^2}{h^2}\right) $$

where:

- `P(p)` is the image patch surrounding pixel `p`
- `P(q)` is another image patch inside the search region
- The patch-distance term measures how different the two patches are
- `h` controls the denoising strength

When two image patches are very similar:

$$ \|P(p)-P(q)\|^2\approx0 $$

their similarity weight becomes relatively large.

When two patches are very different, their similarity weight becomes small.

This allows Non-Local Means to use repeated textures and structures from different locations when estimating cleaner pixel values.

Because many patches must be compared, Non-Local Means is significantly more computationally expensive than simpler local filters.

**Main parameters:**

- Strength
- Color Strength
- Template Window
- Search Window

**Strength** controls the overall denoising strength.

**Color Strength** controls the denoising strength applied to color information.

**Template Window** determines the size of the image patches being compared.

**Search Window** determines how large an area is searched for similar patches.

**Typical use:**

- Image denoising
- Texture-preserving noise reduction
- Photographic noise removal

---

## Image Upscaling

Version 0.3 introduces traditional image interpolation as the first step toward super-resolution.

Unlike filtering algorithms, which modify existing pixel values while keeping the image resolution unchanged, upscaling algorithms generate additional pixels to increase the dimensions of an image.

If an original image has resolution:

```text
Width x Height
```

and is enlarged by a scale factor `s`, the output resolution becomes:

```text
(s x Width) x (s x Height)
```

For example:

```text
640 x 480
    ↓ 4x
2560 x 1920
```

Although interpolation increases the number of pixels, it does not recover genuinely new image information. Instead, the new pixel values are estimated from the existing pixels.

This makes traditional interpolation an important baseline for the neural-network super-resolution methods that will be introduced in later versions.

---

### Nearest Neighbor Interpolation

Nearest Neighbor is the simplest image interpolation method.

For every pixel in the enlarged image, the algorithm identifies the closest corresponding pixel in the original image and directly copies its value.

If the scale factor is `s`, the source coordinates corresponding to an output position `(x', y')` can be approximated as:

$$ x=\frac{x'}{s},\qquad y=\frac{y'}{s} $$

The output pixel is then obtained from the nearest source pixel:

$$ I_{\mathrm{out}}(x',y')=I\left(\mathrm{round}\left(\frac{x'}{s}\right),\mathrm{round}\left(\frac{y'}{s}\right)\right) $$

where:

- `I_out(x', y')` is a pixel in the enlarged image
- `I(x, y)` is a pixel in the original image
- `s` is the scale factor
- `round()` selects the nearest source coordinate

For integer scale factors, this effectively causes each original pixel to be repeated across a larger region.

Conceptually:

```text
Original:

A B
C D

2x Nearest Neighbor:

A A B B
A A B B
C C D D
C C D D
```

Nearest Neighbor performs almost no smoothing.

As a result, individual source pixels become clearly visible when the image is enlarged significantly.

**Main parameter:**

- Scale Factor

**Advantages:**

- Extremely fast
- Very simple computation
- Preserves exact original pixel values
- Useful for pixel art and discrete image labels

**Limitations:**

- Blocky appearance
- Jagged diagonal edges
- Poor photographic enlargement quality

**Typical use:**

- Fast image resizing
- Pixel-art enlargement
- Segmentation masks
- Baseline upscaling comparison

---

### Bilinear Interpolation

Bilinear Interpolation produces smoother results by using the four nearest source pixels instead of copying only one pixel.

First, the output coordinate is mapped back to a continuous position in the source image:

$$ x=\frac{x'}{s},\qquad y=\frac{y'}{s} $$

Let the surrounding source pixels be defined by:

$$ x_0=\lfloor x\rfloor,\qquad x_1=x_0+1,\qquad y_0=\lfloor y\rfloor,\qquad y_1=y_0+1 $$

The fractional distances are:

$$ \alpha=x-x_0,\qquad \beta=y-y_0 $$

The interpolated output value is then:

$$ I_{\mathrm{out}}(x',y')=(1-\alpha)(1-\beta)I(x_0,y_0)+\alpha(1-\beta)I(x_1,y_0)+(1-\alpha)\beta I(x_0,y_1)+\alpha\beta I(x_1,y_1) $$

The four neighbouring pixels therefore contribute according to how close they are to the desired source position.

Conceptually:

```text
I(x0,y0) -------- I(x1,y0)
     |                |
     |       X        |
     |                |
I(x0,y1) -------- I(x1,y1)
```

Compared with Nearest Neighbor, Bilinear Interpolation greatly reduces visible pixel blocks and produces smoother transitions.

However, averaging neighbouring pixels also tends to soften fine details and sharp edges.

**Main parameter:**

- Scale Factor

**Advantages:**

- Fast
- Smooth output
- Better photographic appearance than Nearest Neighbor
- Low computational cost

**Limitations:**

- Softens edges
- Blurs fine texture
- Cannot reconstruct missing detail

**Typical use:**

- General-purpose image resizing
- Smooth image enlargement
- Real-time image scaling
- Traditional interpolation baseline

---

### Bicubic Interpolation

Bicubic Interpolation extends the idea of Bilinear Interpolation by using a larger neighbourhood.

Instead of using only four nearby pixels, Bicubic Interpolation typically evaluates a `4 x 4` neighbourhood containing 16 source pixels.

For a mapped source position `(x, y)`, the interpolated value can be represented as:

$$ I_{\mathrm{out}}(x',y')=\sum_{m=-1}^{2}\sum_{n=-1}^{2}I(x_0+m,y_0+n)\,W(x-x_0-m)\,W(y-y_0-n) $$

where:

- `I_out(x', y')` is the interpolated output pixel
- `(x, y)` is the mapped continuous source position
- `(x0, y0)` identifies the nearby integer source location
- `m` and `n` select pixels inside the `4 x 4` neighbourhood
- `W()` is a cubic interpolation kernel

Conceptually:

```text
x x x x
x x x x
x x X x
x x x x

16 surrounding source samples
contribute to the new pixel X
```

The cubic weighting function creates smoother transitions than Bilinear Interpolation while generally preserving edges and gradients more effectively.

Bicubic Interpolation is especially important in this project because it will serve as one of the primary traditional baselines for later neural-network super-resolution models.

Future models such as FSRCNN, EDSR, and Real-ESRGAN can therefore be compared against a strong non-learning-based enlargement method.

**Main parameter:**

- Scale Factor

**Advantages:**

- Better visual quality than Nearest Neighbor and Bilinear
- Smooth gradients
- More natural edge transitions
- Strong traditional super-resolution baseline

**Limitations:**

- More computationally expensive than Bilinear
- Can still blur very fine detail
- Generated pixels are still mathematically interpolated rather than reconstructed from learned information

**Typical use:**

- High-quality traditional image enlargement
- Photographic resizing
- Image-processing pipelines
- Super-resolution baseline comparison

---

### Lanczos Interpolation

Lanczos Interpolation is a higher-order interpolation method based on a windowed sinc function.

The ideal sinc function used in signal reconstruction is:

$$ \mathrm{sinc}(x)=\frac{\sin(\pi x)}{\pi x} $$

Lanczos limits this function to a finite neighbourhood by multiplying it with another scaled sinc function.

The Lanczos kernel can be written as:

$$ L(x)=\mathrm{sinc}(x)\,\mathrm{sinc}\left(\frac{x}{a}\right),\qquad |x|<a $$

Outside the interpolation window:

$$ L(x)=0,\qquad |x|\geq a $$

where:

- `a` controls the size of the Lanczos window
- `sinc(x)` provides the reconstruction weighting
- nearby source pixels contribute according to the Lanczos kernel

OpenCV's `INTER_LANCZOS4` implementation uses a Lanczos window with `a = 4`, resulting in an `8 x 8` source neighbourhood.

For two-dimensional images, the interpolation is applied in both spatial directions.

A general representation is:

$$ I_{\mathrm{out}}(x',y')=\sum_i\sum_j I(i,j)\,L(x-i)\,L(y-j) $$

Lanczos often preserves high-frequency image information and sharp edges better than simpler interpolation methods.

However, strong transitions can occasionally produce **ringing artifacts**, where faint bright or dark oscillations appear near high-contrast boundaries.

**Main parameter:**

- Scale Factor

**Advantages:**

- Sharp output
- Strong preservation of high-frequency detail
- High-quality photographic resizing
- Often sharper than Bilinear and Bicubic interpolation

**Limitations:**

- More computationally expensive
- Can introduce ringing near strong edges
- Does not reconstruct information that is absent from the original image

**Typical use:**

- High-quality image resizing
- Sharp photographic enlargement
- Downsampling and upscaling
- Comparison with Bicubic interpolation

---

### Traditional Upscaling vs. Super-Resolution

All four interpolation algorithms introduced in v0.3 increase the number of pixels in an image.

For a scale factor `s`, the output width and height become:

$$ W_{\mathrm{out}}=sW_{\mathrm{in}},\qquad H_{\mathrm{out}}=sH_{\mathrm{in}} $$

The total number of pixels therefore increases by:

$$ N_{\mathrm{out}}=s^2N_{\mathrm{in}} $$

For example, a `4x` enlargement produces:

$$ 4^2=16 $$

times as many pixels.

However, those additional pixels are estimated entirely from the original image.

Traditional interpolation therefore performs:

```text
Existing Pixels
      ↓
Mathematical Estimation
      ↓
More Pixels
```

It does **not** perform:

```text
Low-Resolution Image
      ↓
Learned Image Model
      ↓
Predicted Fine Detail
```

This distinction establishes the motivation for the next stage of the project: **Neural Super-Resolution**.


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

### Different-Resolution Comparison

Version 0.3 extends the synchronized viewer system to support comparisons between images with different pixel resolutions.

Traditional filtering keeps the original image dimensions unchanged.

Image upscaling introduces a new situation where the source and processed images may contain very different numbers of pixels.

For example:

```text
Original
640 x 480

    ↓ 4x Upscaling

Processed
2560 x 1920
```

If synchronization were based only on absolute pixel coordinates or scrollbar positions, the two viewers would no longer remain aligned.

Instead, the application uses **normalized image coordinates**.

For an image with width `W` and height `H`, a position `(x, y)` can be represented as:

```text
normalized_x = x / W
normalized_y = y / H
```

These normalized values describe the relative position inside the image rather than an absolute pixel coordinate.

For example:

```text
Original image:
x = 320
W = 640

normalized_x = 320 / 640 = 0.5
```

The same normalized position can then be mapped onto a 4x enlarged image:

```text
Processed image:
W = 2560

x = 0.5 x 2560
x = 1280
```

Both viewers therefore remain focused on approximately the same physical region of the image even when their resolutions are different.

### Independent 100% Views

Version 0.3 also separates the previous 100% viewing control into:

- **Original 100%**
- **Result 100%**

This is necessary because one source pixel may correspond to multiple output pixels after enlargement.

For example, with 4x upscaling:

```text
Original
1 pixel

    ↓ 4x in width and height

Processed
4 x 4 = 16 pixels
```

Viewing the original at 100% therefore represents a different physical screen scale from viewing the processed image at 100%.

The separate controls make it possible to inspect:

- the original source-pixel structure
- the newly interpolated output-pixel structure
- edge behaviour
- smoothing
- block artifacts
- ringing artifacts
- differences between interpolation algorithms

### Resolution Display

The viewer titles now display the resolution of both images.

Example:

```text
Original · 640 x 480

Processed · 2560 x 1920
```

The application also calculates the target resolution before processing whenever the scale factor is changed.

This makes the relationship between the source resolution and output resolution immediately visible.

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
image-restoration-project/
│
├── main.py
├── requirements.txt
│
├── algorithms/
│   ├── __init__.py
│   │
│   ├── mean_filter.py
│   ├── gaussian_filter.py
│   ├── median_filter.py
│   ├── bilateral_filter.py
│   ├── guided_filter.py
│   ├── non_local_means.py
│   │
│   └── upscaling/
│       ├── __init__.py
│       ├── nearest_neighbor.py
│       ├── bilinear.py
│       ├── bicubic.py
│       └── lanczos.py
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

### `algorithms/`

Contains the traditional image-filtering algorithms introduced in v0.1 and v0.2.

```text
Mean
Gaussian
Median
Bilateral
Guided
Non-Local Means
```

### `algorithms/upscaling/`

Introduced in v0.3.

This package contains the traditional image-interpolation algorithms:

```text
Nearest Neighbor
Bilinear
Bicubic
Lanczos
```

Separating interpolation from filtering prepares the project for additional super-resolution categories in future versions.

The architecture can later expand into a structure such as:

```text
algorithms/
│
├── traditional filters
│
├── upscaling
│
└── super_resolution
    ├── FSRCNN
    ├── EDSR
    ├── Real-ESRGAN
    └── SwinIR
```

### `app/`

Contains the PySide6 graphical user interface and synchronized image-viewing system.

`main_window.py` manages:

- algorithm categories
- parameter controls
- image processing
- resolution information
- runtime measurement
- application state

`image_viewer.py` manages:

- image display
- zoom
- pan
- fit-to-window
- 100% viewing
- normalized-coordinate synchronization

### `tools/`

Contains development and environment-diagnostic utilities.

The Python virtual environment is intentionally excluded from the repository and can be recreated using `requirements.txt`.

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

### v0.3 - Image Upscaling & Super-Resolution Foundations

Version 0.3 introduces traditional image interpolation and marks the project's transition from filtering toward image super-resolution.

The previous versions focused on modifying pixel values while preserving the original image dimensions.

Version 0.3 introduces algorithms that actively generate additional pixels and increase the output resolution.

**New interpolation algorithms:**

- Nearest Neighbor
- Bilinear Interpolation
- Bicubic Interpolation
- Lanczos Interpolation

**New upscaling capabilities:**

- 2x image enlargement
- 3x image enlargement
- 4x image enlargement
- Automatic target-resolution calculation
- Original resolution display
- Processed resolution display

**Viewer improvements:**

- Separate Original 100% and Result 100% controls
- Independent Original and Result zoom-percentage display
- Different-resolution synchronized zoom
- Different-resolution synchronized panning
- Normalized-coordinate viewer synchronization

**Architecture improvements:**

- Added a dedicated `algorithms/upscaling/` package
- Separated interpolation algorithms from traditional filters
- Added algorithm categories to the user interface
- Added shared scale-factor controls
- Added upscaling-specific parameter handling
- Preserved compatibility with all v0.1 and v0.2 filtering algorithms

**Measurement and output:**

- Processing runtime remains available for all interpolation algorithms
- Output resolution is displayed after processing
- Enlarged images can be exported at their true generated resolution

This version establishes four traditional interpolation methods as baselines for the neural-network super-resolution algorithms that will be introduced in future versions.

The project has now progressed through:

```text
Classical Local Filtering
        ↓
Edge-Preserving Filtering
        ↓
Patch-Based Denoising
        ↓
Traditional Image Interpolation
        ↓
Neural Super-Resolution
        (next stage)
```

## Development Roadmap

## Development Roadmap

### Completed

- [x] **v0.1 - Basic Filtering GUI**
  - Mean Filter
  - Gaussian Filter
  - Median Filter
  - Basic PySide6 interface
  - Image loading and export
  - Adjustable filter parameters

- [x] **v0.2 - Advanced Traditional Filtering**
  - Bilateral Filter
  - Guided Filter
  - Non-Local Means
  - Dynamic algorithm parameter panels
  - QGraphicsView-based image viewer
  - Mouse-wheel zoom
  - Mouse-drag panning
  - Fit-to-window mode
  - 100% pixel inspection
  - Synchronized Original / Processed viewers
  - Processing runtime measurement

- [x] **v0.3 - Image Upscaling & Super-Resolution Foundations**
  - Nearest Neighbor Interpolation
  - Bilinear Interpolation
  - Bicubic Interpolation
  - Lanczos Interpolation
  - 2x, 3x, and 4x image enlargement
  - Automatic target-resolution calculation
  - Original and processed resolution display
  - Different-resolution viewer synchronization
  - Independent Original / Result 100% viewing
  - Traditional interpolation baseline for future super-resolution

---

### Next

#### v0.4 - Neural Super-Resolution Foundations

Version 0.4 will introduce the first learned image super-resolution models.

Planned development:

- FSRCNN
- EDSR
- Neural-network model loading
- Pre-trained model management
- CNN-based image super-resolution
- 2x and 4x neural upscaling
- Traditional interpolation vs. neural super-resolution comparison
- Model inference runtime measurement
- Preparation for GPU-accelerated inference

The main goal of v0.4 will be to demonstrate the transition from:

```text
Mathematical Interpolation
        ↓
Learned Image Reconstruction
```

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
