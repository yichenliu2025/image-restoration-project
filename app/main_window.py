import time
import cv2

from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QComboBox,
    QSpinBox,
    QDoubleSpinBox,
    QCheckBox,
    QStackedWidget,
    QHBoxLayout,
    QVBoxLayout,
    QGroupBox,
    QFormLayout,
)

from algorithms.mean_filter import MeanFilter
from algorithms.gaussian_filter import GaussianFilter
from algorithms.median_filter import MedianFilter
from algorithms.bilateral_filter import BilateralFilter
from algorithms.guided_filter import GuidedFilter
from algorithms.non_local_means import NonLocalMeansFilter

from algorithms.upscaling.nearest_neighbor import NearestNeighborUpscaler
from algorithms.upscaling.bilinear import BilinearUpscaler
from algorithms.upscaling.bicubic import BicubicUpscaler
from algorithms.upscaling.lanczos import LanczosUpscaler

from app.image_viewer import ImageViewer


class MainWindow(QMainWindow):

    FILTER_ALGORITHMS = [
        "Mean Filter",
        "Gaussian Filter",
        "Median Filter",
        "Bilateral Filter",
        "Guided Filter",
        "Non-Local Means",
    ]

    UPSCALING_ALGORITHMS = [
        "Nearest Neighbor",
        "Bilinear",
        "Bicubic",
        "Lanczos",
    ]

    DESCRIPTIONS = {

        "Mean Filter":
            "Simple averaging filter. Every pixel inside "
            "the kernel contributes equally.",

        "Gaussian Filter":
            "Weighted smoothing using a Gaussian distribution. "
            "Nearby pixels receive larger weights.",

        "Median Filter":
            "Non-linear neighbourhood filter that replaces "
            "each pixel with the local median.",

        "Bilateral Filter":
            "Edge-preserving smoothing based on both spatial "
            "distance and color similarity.",

        "Guided Filter":
            "Edge-preserving filtering based on a local linear "
            "relationship with a guidance image.",

        "Non-Local Means":
            "Patch-based denoising that searches a larger "
            "region for similar local structures.",

        "Nearest Neighbor":
            "Upscaling by copying the nearest source pixel. "
            "Extremely fast, but often visibly blocky.",

        "Bilinear":
            "Upscaling by blending nearby source pixels. "
            "Smoother than nearest neighbor, but softer.",

        "Bicubic":
            "Cubic interpolation over a larger neighbourhood. "
            "A strong traditional enlargement baseline.",

        "Lanczos":
            "High-quality interpolation using a Lanczos kernel. "
            "Often sharp, but can ring near hard edges.",
    }

    def __init__(self):
        super().__init__()

        # ==================================================
        # Window
        # ==================================================

        self.setWindowTitle(
            "Image Restoration & Super-Resolution Lab v0.3"
        )

        self.resize(
            1500,
            920
        )

        # ==================================================
        # Data
        # ==================================================

        self.original_image = None
        self.processed_image = None

        self.parameter_page_indices = {}

        # Prevent synchronization loops while a viewer
        # is being programmatically updated.
        self._syncing_viewers = False

        # ==================================================
        # Main widget
        # ==================================================

        central = QWidget()

        self.setCentralWidget(
            central
        )

        main_layout = QVBoxLayout(
            central
        )

        # ==================================================
        # Header
        # ==================================================

        title = QLabel(
            "Image Restoration & Super-Resolution Lab"
        )

        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title.setStyleSheet(
            """
            QLabel {
                font-size: 26px;
                font-weight: bold;
                padding: 6px;
            }
            """
        )

        version = QLabel(
            "v0.3 · Image Upscaling & Super-Resolution Foundations"
        )

        version.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        version.setStyleSheet(
            """
            QLabel {
                color: #888888;
                font-size: 13px;
                padding-bottom: 4px;
            }
            """
        )

        main_layout.addWidget(
            title
        )

        main_layout.addWidget(
            version
        )

        # ==================================================
        # Viewer toolbar
        # ==================================================

        toolbar = QHBoxLayout()

        self.fit_button = QPushButton(
            "Fit"
        )

        self.original_100_button = QPushButton(
            "Original 100%"
        )

        self.result_100_button = QPushButton(
            "Result 100%"
        )

        self.sync_checkbox = QCheckBox(
            "Synchronize Viewers"
        )

        self.sync_checkbox.setChecked(
            True
        )

        self.original_zoom_label = QLabel(
            "Original: --"
        )

        self.result_zoom_label = QLabel(
            "Result: --"
        )

        toolbar.addWidget(
            self.fit_button
        )

        toolbar.addWidget(
            self.original_100_button
        )

        toolbar.addWidget(
            self.result_100_button
        )

        toolbar.addWidget(
            self.sync_checkbox
        )

        toolbar.addStretch()

        toolbar.addWidget(
            self.original_zoom_label
        )

        toolbar.addWidget(
            self.result_zoom_label
        )

        main_layout.addLayout(
            toolbar
        )

        # ==================================================
        # Image viewers
        # ==================================================

        viewer_layout = QHBoxLayout()

        self.original_group = QGroupBox(
            "Original"
        )

        original_layout = QVBoxLayout(
            self.original_group
        )

        self.original_viewer = ImageViewer()

        original_layout.addWidget(
            self.original_viewer
        )

        self.processed_group = QGroupBox(
            "Processed"
        )

        processed_layout = QVBoxLayout(
            self.processed_group
        )

        self.processed_viewer = ImageViewer()

        self.processed_viewer.clear_image(
            "No processed image"
        )

        processed_layout.addWidget(
            self.processed_viewer
        )

        viewer_layout.addWidget(
            self.original_group,
            1
        )

        viewer_layout.addWidget(
            self.processed_group,
            1
        )

        main_layout.addLayout(
            viewer_layout,
            1
        )

        # ==================================================
        # Processing controls
        # ==================================================

        controls_group = QGroupBox(
            "Algorithm & Parameters"
        )

        controls_layout = QVBoxLayout(
            controls_group
        )

        # --------------------------------------------------
        # Category
        # --------------------------------------------------

        category_row = QHBoxLayout()

        category_row.addWidget(
            QLabel("Category:")
        )

        self.category_combo = QComboBox()

        self.category_combo.addItems(
            [
                "Traditional Filtering",
                "Image Upscaling",
            ]
        )

        category_row.addWidget(
            self.category_combo,
            1
        )

        controls_layout.addLayout(
            category_row
        )

        # --------------------------------------------------
        # Algorithm
        # --------------------------------------------------

        algorithm_row = QHBoxLayout()

        algorithm_row.addWidget(
            QLabel("Algorithm:")
        )

        self.algorithm_combo = QComboBox()

        algorithm_row.addWidget(
            self.algorithm_combo,
            1
        )

        controls_layout.addLayout(
            algorithm_row
        )

        # ==================================================
        # Dynamic parameter panel
        # ==================================================

        self.parameter_stack = QStackedWidget()

        self._create_parameter_pages()

        controls_layout.addWidget(
            self.parameter_stack
        )

        # ==================================================
        # Algorithm description
        # ==================================================

        self.algorithm_info = QLabel()

        self.algorithm_info.setWordWrap(
            True
        )

        self.algorithm_info.setStyleSheet(
            """
            QLabel {
                color: #888888;
                padding-top: 5px;
                padding-bottom: 5px;
            }
            """
        )

        controls_layout.addWidget(
            self.algorithm_info
        )

        main_layout.addWidget(
            controls_group
        )

        # ==================================================
        # Main buttons
        # ==================================================

        button_row = QHBoxLayout()

        self.open_button = QPushButton(
            "Open Image"
        )

        self.process_button = QPushButton(
            "Process"
        )

        self.reset_button = QPushButton(
            "Reset Result"
        )

        self.save_button = QPushButton(
            "Save Result"
        )

        for button in (
            self.open_button,
            self.process_button,
            self.reset_button,
            self.save_button,
        ):
            button_row.addWidget(
                button
            )

        main_layout.addLayout(
            button_row
        )

        # ==================================================
        # Initial state
        # ==================================================

        self.process_button.setEnabled(
            False
        )

        self.reset_button.setEnabled(
            False
        )

        self.save_button.setEnabled(
            False
        )

        self.result_100_button.setEnabled(
            False
        )

        # ==================================================
        # Signals
        # ==================================================

        self.category_combo.currentIndexChanged.connect(
            self.category_changed
        )

        self.algorithm_combo.currentIndexChanged.connect(
            self.algorithm_changed
        )

        self.open_button.clicked.connect(
            self.open_image
        )

        self.process_button.clicked.connect(
            self.process_image
        )

        self.reset_button.clicked.connect(
            self.reset_result
        )

        self.save_button.clicked.connect(
            self.save_image
        )

        self.fit_button.clicked.connect(
            self.fit_views
        )

        self.original_100_button.clicked.connect(
            self.original_actual_size
        )

        self.result_100_button.clicked.connect(
            self.result_actual_size
        )

        self.sync_checkbox.toggled.connect(
            self.sync_toggled
        )

        self.original_viewer.viewChanged.connect(
            self.sync_from_original
        )

        self.processed_viewer.viewChanged.connect(
            self.sync_from_processed
        )

        self.original_viewer.zoomPercentChanged.connect(
            lambda percent:
            self.original_zoom_label.setText(
                f"Original: {percent:.0f}%"
            )
        )

        self.processed_viewer.zoomPercentChanged.connect(
            lambda percent:
            self.result_zoom_label.setText(
                f"Result: {percent:.0f}%"
            )
        )

        self.upscale_factor.currentIndexChanged.connect(
            self.update_target_resolution
        )

        # ==================================================
        # Status
        # ==================================================

        self.statusBar().showMessage(
            "Ready"
        )

        self.category_changed(
            0
        )

    # ======================================================
    # Parameter page helpers
    # ======================================================

    def _register_page(
        self,
        names,
        page
    ):

        index = self.parameter_stack.addWidget(
            page
        )

        for name in names:

            self.parameter_page_indices[name] = (
                index
            )

    @staticmethod
    def _spin(
        minimum,
        maximum,
        value,
        step=1
    ):

        box = QSpinBox()

        box.setRange(
            minimum,
            maximum
        )

        box.setValue(
            value
        )

        box.setSingleStep(
            step
        )

        return box

    @staticmethod
    def _double_spin(
        minimum,
        maximum,
        value,
        step,
        decimals=2
    ):

        box = QDoubleSpinBox()

        box.setRange(
            minimum,
            maximum
        )

        box.setValue(
            value
        )

        box.setSingleStep(
            step
        )

        box.setDecimals(
            decimals
        )

        return box

    # ======================================================
    # Parameter pages
    # ======================================================

    def _create_parameter_pages(self):

        # --------------------------------------------------
        # Mean
        # --------------------------------------------------

        page = QWidget()

        form = QFormLayout(
            page
        )

        self.mean_kernel = self._spin(
            1,
            31,
            5,
            2
        )

        form.addRow(
            "Kernel Size:",
            self.mean_kernel
        )

        self._register_page(
            ["Mean Filter"],
            page
        )

        # --------------------------------------------------
        # Gaussian
        # --------------------------------------------------

        page = QWidget()

        form = QFormLayout(
            page
        )

        self.gaussian_kernel = self._spin(
            1,
            31,
            5,
            2
        )

        self.gaussian_sigma = self._double_spin(
            0.0,
            20.0,
            1.0,
            0.1,
            2
        )

        form.addRow(
            "Kernel Size:",
            self.gaussian_kernel
        )

        form.addRow(
            "Sigma:",
            self.gaussian_sigma
        )

        self._register_page(
            ["Gaussian Filter"],
            page
        )

        # --------------------------------------------------
        # Median
        # --------------------------------------------------

        page = QWidget()

        form = QFormLayout(
            page
        )

        self.median_kernel = self._spin(
            3,
            31,
            5,
            2
        )

        form.addRow(
            "Kernel Size:",
            self.median_kernel
        )

        self._register_page(
            ["Median Filter"],
            page
        )

        # --------------------------------------------------
        # Bilateral
        # --------------------------------------------------

        page = QWidget()

        form = QFormLayout(
            page
        )

        self.bilateral_diameter = self._spin(
            1,
            31,
            9,
            2
        )

        self.bilateral_sigma_color = (
            self._double_spin(
                1.0,
                250.0,
                75.0,
                5.0,
                1
            )
        )

        self.bilateral_sigma_space = (
            self._double_spin(
                1.0,
                250.0,
                75.0,
                5.0,
                1
            )
        )

        form.addRow(
            "Diameter:",
            self.bilateral_diameter
        )

        form.addRow(
            "Sigma Color:",
            self.bilateral_sigma_color
        )

        form.addRow(
            "Sigma Space:",
            self.bilateral_sigma_space
        )

        self._register_page(
            ["Bilateral Filter"],
            page
        )

        # --------------------------------------------------
        # Guided
        # --------------------------------------------------

        page = QWidget()

        form = QFormLayout(
            page
        )

        self.guided_radius = self._spin(
            1,
            50,
            15
        )

        self.guided_epsilon = (
            self._double_spin(
                0.0001,
                1.0,
                0.01,
                0.005,
                4
            )
        )

        form.addRow(
            "Radius:",
            self.guided_radius
        )

        form.addRow(
            "Epsilon:",
            self.guided_epsilon
        )

        self._register_page(
            ["Guided Filter"],
            page
        )

        # --------------------------------------------------
        # NLM
        # --------------------------------------------------

        page = QWidget()

        form = QFormLayout(
            page
        )

        self.nlm_strength = self._double_spin(
            0.0,
            30.0,
            10.0,
            1.0,
            1
        )

        self.nlm_color_strength = (
            self._double_spin(
                0.0,
                30.0,
                10.0,
                1.0,
                1
            )
        )

        self.nlm_template = self._spin(
            3,
            15,
            7,
            2
        )

        self.nlm_search = self._spin(
            7,
            35,
            21,
            2
        )

        form.addRow(
            "Strength:",
            self.nlm_strength
        )

        form.addRow(
            "Color Strength:",
            self.nlm_color_strength
        )

        form.addRow(
            "Template Window:",
            self.nlm_template
        )

        form.addRow(
            "Search Window:",
            self.nlm_search
        )

        self._register_page(
            ["Non-Local Means"],
            page
        )

        # --------------------------------------------------
        # Shared Upscaling page
        # --------------------------------------------------

        page = QWidget()

        form = QFormLayout(
            page
        )

        self.upscale_factor = QComboBox()

        self.upscale_factor.addItem(
            "2x",
            2
        )

        self.upscale_factor.addItem(
            "3x",
            3
        )

        self.upscale_factor.addItem(
            "4x",
            4
        )

        self.upscale_factor.setCurrentIndex(
            1
        )

        self.target_resolution_label = QLabel(
            "Open an image to calculate target resolution"
        )

        self.target_resolution_label.setWordWrap(
            True
        )

        note = QLabel(
            "Traditional interpolation increases pixel count, "
            "but it does not reconstruct learned image detail."
        )

        note.setWordWrap(
            True
        )

        note.setStyleSheet(
            "color: #888888;"
        )

        form.addRow(
            "Scale Factor:",
            self.upscale_factor
        )

        form.addRow(
            "Target Resolution:",
            self.target_resolution_label
        )

        form.addRow(
            "",
            note
        )

        self._register_page(
            self.UPSCALING_ALGORITHMS,
            page
        )

    # ======================================================
    # Category selection
    # ======================================================

    def category_changed(
        self,
        _index
    ):

        category = (
            self.category_combo.currentText()
        )

        if category == "Traditional Filtering":

            algorithms = (
                self.FILTER_ALGORITHMS
            )

        else:

            algorithms = (
                self.UPSCALING_ALGORITHMS
            )

        self.algorithm_combo.blockSignals(
            True
        )

        self.algorithm_combo.clear()

        self.algorithm_combo.addItems(
            algorithms
        )

        self.algorithm_combo.blockSignals(
            False
        )

        self.algorithm_combo.setCurrentIndex(
            0
        )

        self.algorithm_changed(
            0
        )

    # ======================================================
    # Algorithm selection
    # ======================================================

    def algorithm_changed(
        self,
        _index
    ):

        algorithm = (
            self.algorithm_combo.currentText()
        )

        if not algorithm:
            return

        page_index = (
            self.parameter_page_indices.get(
                algorithm
            )
        )

        if page_index is not None:

            self.parameter_stack.setCurrentIndex(
                page_index
            )

        self.algorithm_info.setText(
            self.DESCRIPTIONS[algorithm]
        )

        if algorithm in self.UPSCALING_ALGORITHMS:

            self.update_target_resolution()

    # ======================================================
    # Utilities
    # ======================================================

    @staticmethod
    def make_odd(
        value,
        minimum=1
    ):

        value = max(
            minimum,
            value
        )

        if value % 2 == 1:
            return value

        return value + 1

    def current_scale_factor(self):

        return int(
            self.upscale_factor.currentData()
        )

    # ======================================================
    # Target resolution
    # ======================================================

    def update_target_resolution(self):

        if self.original_image is None:

            self.target_resolution_label.setText(
                "Open an image to calculate target resolution"
            )

            return

        height, width = (
            self.original_image.shape[:2]
        )

        factor = (
            self.current_scale_factor()
        )

        target_width = (
            width * factor
        )

        target_height = (
            height * factor
        )

        self.target_resolution_label.setText(
            (
                f"{width} × {height}  →  "
                f"{target_width} × {target_height}"
            )
        )

    # ======================================================
    # Open image
    # ======================================================

    def open_image(self):

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            "",
            (
                "Image Files "
                "(*.png *.jpg *.jpeg *.bmp *.tif *.tiff)"
            )
        )

        if not path:
            return

        image = cv2.imread(
            path,
            cv2.IMREAD_COLOR
        )

        if image is None:

            QMessageBox.critical(
                self,
                "Error",
                "The selected image could not be opened."
            )

            return

        self.original_image = image

        self.processed_image = None

        self.original_viewer.set_pixmap(
            self.cv_image_to_pixmap(
                image
            )
        )

        self.processed_viewer.clear_image(
            "No processed image"
        )

        height, width = (
            image.shape[:2]
        )

        self.original_group.setTitle(
            f"Original · {width} × {height}"
        )

        self.processed_group.setTitle(
            "Processed"
        )

        self.process_button.setEnabled(
            True
        )

        self.reset_button.setEnabled(
            True
        )

        self.save_button.setEnabled(
            False
        )

        self.result_100_button.setEnabled(
            False
        )

        self.result_zoom_label.setText(
            "Result: --"
        )

        self.update_target_resolution()

        self.statusBar().showMessage(
            f"Loaded image: {width} × {height}"
        )

    # ======================================================
    # Save
    # ======================================================

    def save_image(self):

        if self.processed_image is None:

            QMessageBox.warning(
                self,
                "No Result",
                "There is no processed image to save."
            )

            return

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Processed Image",
            "processed_image.png",
            (
                "PNG Image (*.png);;"
                "JPEG Image (*.jpg *.jpeg);;"
                "Bitmap Image (*.bmp)"
            )
        )

        if not path:
            return

        success = cv2.imwrite(
            path,
            self.processed_image
        )

        if success:

            self.statusBar().showMessage(
                f"Saved: {path}"
            )

        else:

            QMessageBox.critical(
                self,
                "Save Error",
                "The image could not be saved."
            )

    # ======================================================
    # Reset
    # ======================================================

    def reset_result(self):

        self.processed_image = None

        self.processed_viewer.clear_image(
            "No processed image"
        )

        self.processed_group.setTitle(
            "Processed"
        )

        self.save_button.setEnabled(
            False
        )

        self.result_100_button.setEnabled(
            False
        )

        self.result_zoom_label.setText(
            "Result: --"
        )

        self.statusBar().showMessage(
            "Processing result reset"
        )

    # ======================================================
    # Processing
    # ======================================================

    def process_image(self):

        if self.original_image is None:

            QMessageBox.warning(
                self,
                "No Image",
                "Please open an image first."
            )

            return

        algorithm = (
            self.algorithm_combo.currentText()
        )

        handlers = {

            "Mean Filter":
                self._run_mean,

            "Gaussian Filter":
                self._run_gaussian,

            "Median Filter":
                self._run_median,

            "Bilateral Filter":
                self._run_bilateral,

            "Guided Filter":
                self._run_guided,

            "Non-Local Means":
                self._run_nlm,

            "Nearest Neighbor":
                self._run_nearest,

            "Bilinear":
                self._run_bilinear,

            "Bicubic":
                self._run_bicubic,

            "Lanczos":
                self._run_lanczos,
        }

        self.process_button.setEnabled(
            False
        )

        QApplication.setOverrideCursor(
            Qt.CursorShape.WaitCursor
        )

        start = time.perf_counter()

        try:

            (
                self.processed_image,
                parameter_text
            ) = handlers[algorithm]()

        except Exception as error:

            QMessageBox.critical(
                self,
                "Processing Error",
                str(error)
            )

            return

        finally:

            QApplication.restoreOverrideCursor()

            self.process_button.setEnabled(
                True
            )

        elapsed = (
            time.perf_counter() - start
        )

        # Capture the current source view BEFORE
        # inserting the processed image.

        sync_state = None

        if (
            self.sync_checkbox.isChecked()
            and self.original_viewer.has_image()
        ):

            sync_state = (
                self.original_viewer.get_view_state()
            )

        self._syncing_viewers = True

        try:

            self.processed_viewer.set_pixmap(
                self.cv_image_to_pixmap(
                    self.processed_image
                )
            )

            if sync_state is not None:

                self.processed_viewer.apply_view_state(
                    *sync_state
                )

        finally:

            self._syncing_viewers = False

        height, width = (
            self.processed_image.shape[:2]
        )

        self.processed_group.setTitle(
            f"Processed · {width} × {height}"
        )

        self.save_button.setEnabled(
            True
        )

        self.result_100_button.setEnabled(
            True
        )

        self.statusBar().showMessage(
            (
                f"{algorithm} completed | "
                f"{parameter_text} | "
                f"Output: {width} × {height} | "
                f"{elapsed:.3f} s"
            )
        )

    # ======================================================
    # Filter handlers
    # ======================================================

    def _run_mean(self):

        kernel = (
            self.mean_kernel.value()
        )

        result = MeanFilter.process(
            self.original_image,
            kernel
        )

        return (
            result,
            f"Kernel={kernel}"
        )

    def _run_gaussian(self):

        kernel = self.make_odd(
            self.gaussian_kernel.value()
        )

        sigma = (
            self.gaussian_sigma.value()
        )

        result = GaussianFilter.process(
            self.original_image,
            kernel,
            sigma
        )

        return (
            result,
            (
                f"Kernel={kernel}, "
                f"Sigma={sigma:.2f}"
            )
        )

    def _run_median(self):

        kernel = self.make_odd(
            self.median_kernel.value(),
            3
        )

        result = MedianFilter.process(
            self.original_image,
            kernel
        )

        return (
            result,
            f"Kernel={kernel}"
        )

    def _run_bilateral(self):

        diameter = (
            self.bilateral_diameter.value()
        )

        sigma_color = (
            self.bilateral_sigma_color.value()
        )

        sigma_space = (
            self.bilateral_sigma_space.value()
        )

        result = BilateralFilter.process(
            self.original_image,
            diameter,
            sigma_color,
            sigma_space
        )

        return (
            result,
            (
                f"d={diameter}, "
                f"SigmaColor={sigma_color:.1f}, "
                f"SigmaSpace={sigma_space:.1f}"
            )
        )

    def _run_guided(self):

        radius = (
            self.guided_radius.value()
        )

        epsilon = (
            self.guided_epsilon.value()
        )

        result = GuidedFilter.process(
            self.original_image,
            radius,
            epsilon
        )

        return (
            result,
            (
                f"Radius={radius}, "
                f"Epsilon={epsilon:.4f}"
            )
        )

    def _run_nlm(self):

        strength = (
            self.nlm_strength.value()
        )

        color_strength = (
            self.nlm_color_strength.value()
        )

        template = self.make_odd(
            self.nlm_template.value(),
            3
        )

        search = self.make_odd(
            self.nlm_search.value(),
            7
        )

        result = NonLocalMeansFilter.process(
            self.original_image,
            strength,
            color_strength,
            template,
            search
        )

        return (
            result,
            (
                f"h={strength:.1f}, "
                f"hColor={color_strength:.1f}, "
                f"Template={template}, "
                f"Search={search}"
            )
        )

    # ======================================================
    # Upscaling handlers
    # ======================================================

    def _run_nearest(self):

        factor = (
            self.current_scale_factor()
        )

        result = (
            NearestNeighborUpscaler.process(
                self.original_image,
                factor
            )
        )

        return (
            result,
            f"Scale={factor}x"
        )

    def _run_bilinear(self):

        factor = (
            self.current_scale_factor()
        )

        result = (
            BilinearUpscaler.process(
                self.original_image,
                factor
            )
        )

        return (
            result,
            f"Scale={factor}x"
        )

    def _run_bicubic(self):

        factor = (
            self.current_scale_factor()
        )

        result = (
            BicubicUpscaler.process(
                self.original_image,
                factor
            )
        )

        return (
            result,
            f"Scale={factor}x"
        )

    def _run_lanczos(self):

        factor = (
            self.current_scale_factor()
        )

        result = (
            LanczosUpscaler.process(
                self.original_image,
                factor
            )
        )

        return (
            result,
            f"Scale={factor}x"
        )

    # ======================================================
    # OpenCV -> Qt
    # ======================================================

    @staticmethod
    def cv_image_to_pixmap(
        image
    ):

        rgb = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )

        height, width, channels = (
            rgb.shape
        )

        bytes_per_line = (
            channels * width
        )

        q_image = QImage(
            rgb.data,
            width,
            height,
            bytes_per_line,
            QImage.Format.Format_RGB888
        ).copy()

        return QPixmap.fromImage(
            q_image
        )

    # ======================================================
    # Viewer synchronization
    # ======================================================

    def sync_from_original(
        self,
        zoom,
        x,
        y
    ):

        if (
            self._syncing_viewers
            or not self.sync_checkbox.isChecked()
            or not self.processed_viewer.has_image()
        ):
            return

        self._syncing_viewers = True

        try:

            self.processed_viewer.apply_view_state(
                zoom,
                x,
                y
            )

        finally:

            self._syncing_viewers = False

    def sync_from_processed(
        self,
        zoom,
        x,
        y
    ):

        if (
            self._syncing_viewers
            or not self.sync_checkbox.isChecked()
            or not self.original_viewer.has_image()
        ):
            return

        self._syncing_viewers = True

        try:

            self.original_viewer.apply_view_state(
                zoom,
                x,
                y
            )

        finally:

            self._syncing_viewers = False

    def sync_toggled(
        self,
        checked
    ):

        if (
            checked
            and self.original_viewer.has_image()
            and self.processed_viewer.has_image()
        ):

            self.processed_viewer.apply_view_state(
                *self.original_viewer.get_view_state()
            )

    # ======================================================
    # View controls
    # ======================================================

    def fit_views(self):

        if self.original_viewer.has_image():

            self.original_viewer.fit_to_window()

        if (
            not self.sync_checkbox.isChecked()
            and self.processed_viewer.has_image()
        ):

            self.processed_viewer.fit_to_window()

    def original_actual_size(self):

        if self.original_viewer.has_image():

            self.original_viewer.actual_size()

    def result_actual_size(self):

        if self.processed_viewer.has_image():

            self.processed_viewer.actual_size()