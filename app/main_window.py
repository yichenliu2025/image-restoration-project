import time
import cv2

from PySide6.QtCore import Qt

from PySide6.QtGui import (
    QImage,
    QPixmap
)

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

from algorithms.bilateral_filter import (
    BilateralFilter
)

from algorithms.guided_filter import (
    GuidedFilter
)

from algorithms.non_local_means import (
    NonLocalMeansFilter
)

from app.image_viewer import ImageViewer


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # ==================================================
        # Window
        # ==================================================

        self.setWindowTitle(
            "Image Restoration & Super-Resolution Lab v0.2"
        )

        self.resize(
            1450,
            900
        )

        # ==================================================
        # Image data
        # ==================================================

        self.original_image = None
        self.processed_image = None

        # ==================================================
        # Main widget
        # ==================================================

        central_widget = QWidget()

        self.setCentralWidget(
            central_widget
        )

        main_layout = QVBoxLayout(
            central_widget
        )

        # ==================================================
        # Title
        # ==================================================

        title_label = QLabel(
            "Image Restoration & Super-Resolution Lab"
        )

        title_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title_label.setStyleSheet(
            """
            QLabel {
                font-size: 26px;
                font-weight: bold;
                padding: 8px;
            }
            """
        )

        version_label = QLabel(
            "v0.2 · Advanced Traditional Filtering"
        )

        version_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        version_label.setStyleSheet(
            """
            QLabel {
                color: #888888;
                font-size: 13px;
                padding-bottom: 6px;
            }
            """
        )

        main_layout.addWidget(
            title_label
        )

        main_layout.addWidget(
            version_label
        )

        # ==================================================
        # Viewer toolbar
        # ==================================================

        viewer_toolbar = QHBoxLayout()

        self.fit_button = QPushButton(
            "Fit"
        )

        self.actual_size_button = QPushButton(
            "100%"
        )

        self.sync_checkbox = QCheckBox(
            "Synchronize Viewers"
        )

        self.sync_checkbox.setChecked(
            True
        )

        self.zoom_label = QLabel(
            "Zoom: --"
        )

        viewer_toolbar.addWidget(
            self.fit_button
        )

        viewer_toolbar.addWidget(
            self.actual_size_button
        )

        viewer_toolbar.addWidget(
            self.sync_checkbox
        )

        viewer_toolbar.addStretch()

        viewer_toolbar.addWidget(
            self.zoom_label
        )

        main_layout.addLayout(
            viewer_toolbar
        )

        # ==================================================
        # Image viewers
        # ==================================================

        viewer_layout = QHBoxLayout()

        # Original
        original_group = QGroupBox(
            "Original"
        )

        original_layout = QVBoxLayout(
            original_group
        )

        self.original_viewer = ImageViewer()

        original_layout.addWidget(
            self.original_viewer
        )

        # Processed
        processed_group = QGroupBox(
            "Processed"
        )

        processed_layout = QVBoxLayout(
            processed_group
        )

        self.processed_viewer = ImageViewer()

        self.processed_viewer.clear_image(
            "No processed image"
        )

        processed_layout.addWidget(
            self.processed_viewer
        )

        viewer_layout.addWidget(
            original_group,
            stretch=1
        )

        viewer_layout.addWidget(
            processed_group,
            stretch=1
        )

        main_layout.addLayout(
            viewer_layout,
            stretch=1
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

        # Algorithm selection
        algorithm_row = QHBoxLayout()

        algorithm_label = QLabel(
            "Algorithm:"
        )

        self.algorithm_combo = QComboBox()

        self.algorithm_combo.addItems(
            [
                "Mean Filter",
                "Gaussian Filter",
                "Median Filter",
                "Bilateral Filter",
                "Guided Filter",
                "Non-Local Means",
            ]
        )

        algorithm_row.addWidget(
            algorithm_label
        )

        algorithm_row.addWidget(
            self.algorithm_combo,
            stretch=1
        )

        controls_layout.addLayout(
            algorithm_row
        )

        # ==================================================
        # Dynamic parameter panel
        # ==================================================

        self.parameter_stack = (
            QStackedWidget()
        )

        self._create_mean_page()

        self._create_gaussian_page()

        self._create_median_page()

        self._create_bilateral_page()

        self._create_guided_page()

        self._create_nlm_page()

        controls_layout.addWidget(
            self.parameter_stack
        )

        # ==================================================
        # Algorithm information
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

        button_layout = QHBoxLayout()

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

        button_layout.addWidget(
            self.open_button
        )

        button_layout.addWidget(
            self.process_button
        )

        button_layout.addWidget(
            self.reset_button
        )

        button_layout.addWidget(
            self.save_button
        )

        main_layout.addLayout(
            button_layout
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

        # ==================================================
        # Signals
        # ==================================================

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

        self.actual_size_button.clicked.connect(
            self.actual_size_views
        )

        self.sync_checkbox.toggled.connect(
            self.sync_toggled
        )

        # Original -> Processed
        self.original_viewer.viewChanged.connect(
            self.sync_from_original
        )

        # Processed -> Original
        self.processed_viewer.viewChanged.connect(
            self.sync_from_processed
        )

        self.original_viewer.zoomPercentChanged.connect(
            self.update_zoom_label
        )

        self.processed_viewer.zoomPercentChanged.connect(
            self.update_zoom_label
        )

        # ==================================================
        # Status
        # ==================================================

        self.statusBar().showMessage(
            "Ready"
        )

        self.algorithm_changed(
            0
        )

    # ======================================================
    # Parameter page helpers
    # ======================================================

    def _make_spinbox(
        self,
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

    def _make_double_spinbox(
        self,
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
    # Mean parameters
    # ======================================================

    def _create_mean_page(self):

        page = QWidget()

        form = QFormLayout(
            page
        )

        self.mean_kernel = (
            self._make_spinbox(
                1,
                31,
                5,
                2
            )
        )

        form.addRow(
            "Kernel Size:",
            self.mean_kernel
        )

        self.parameter_stack.addWidget(
            page
        )

    # ======================================================
    # Gaussian parameters
    # ======================================================

    def _create_gaussian_page(self):

        page = QWidget()

        form = QFormLayout(
            page
        )

        self.gaussian_kernel = (
            self._make_spinbox(
                1,
                31,
                5,
                2
            )
        )

        self.gaussian_sigma = (
            self._make_double_spinbox(
                0.0,
                20.0,
                1.0,
                0.1,
                2
            )
        )

        form.addRow(
            "Kernel Size:",
            self.gaussian_kernel
        )

        form.addRow(
            "Sigma:",
            self.gaussian_sigma
        )

        self.parameter_stack.addWidget(
            page
        )

    # ======================================================
    # Median parameters
    # ======================================================

    def _create_median_page(self):

        page = QWidget()

        form = QFormLayout(
            page
        )

        self.median_kernel = (
            self._make_spinbox(
                3,
                31,
                5,
                2
            )
        )

        form.addRow(
            "Kernel Size:",
            self.median_kernel
        )

        self.parameter_stack.addWidget(
            page
        )

    # ======================================================
    # Bilateral parameters
    # ======================================================

    def _create_bilateral_page(self):

        page = QWidget()

        form = QFormLayout(
            page
        )

        self.bilateral_diameter = (
            self._make_spinbox(
                1,
                31,
                9,
                2
            )
        )

        self.bilateral_sigma_color = (
            self._make_double_spinbox(
                1.0,
                250.0,
                75.0,
                5.0,
                1
            )
        )

        self.bilateral_sigma_space = (
            self._make_double_spinbox(
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

        self.parameter_stack.addWidget(
            page
        )

    # ======================================================
    # Guided parameters
    # ======================================================

    def _create_guided_page(self):

        page = QWidget()

        form = QFormLayout(
            page
        )

        self.guided_radius = (
            self._make_spinbox(
                1,
                50,
                15,
                1
            )
        )

        self.guided_epsilon = (
            self._make_double_spinbox(
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

        self.parameter_stack.addWidget(
            page
        )

    # ======================================================
    # NLM parameters
    # ======================================================

    def _create_nlm_page(self):

        page = QWidget()

        form = QFormLayout(
            page
        )

        self.nlm_strength = (
            self._make_double_spinbox(
                0.0,
                30.0,
                10.0,
                1.0,
                1
            )
        )

        self.nlm_color_strength = (
            self._make_double_spinbox(
                0.0,
                30.0,
                10.0,
                1.0,
                1
            )
        )

        self.nlm_template = (
            self._make_spinbox(
                3,
                15,
                7,
                2
            )
        )

        self.nlm_search = (
            self._make_spinbox(
                7,
                35,
                21,
                2
            )
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

        self.parameter_stack.addWidget(
            page
        )

    # ======================================================
    # Algorithm selection
    # ======================================================

    def algorithm_changed(
        self,
        index
    ):

        self.parameter_stack.setCurrentIndex(
            index
        )

        descriptions = {

            "Mean Filter":
                "Simple averaging filter. "
                "All pixels inside the kernel contribute "
                "equally to the output.",

            "Gaussian Filter":
                "Weighted smoothing using a Gaussian "
                "distribution. Nearby pixels receive "
                "larger weights.",

            "Median Filter":
                "Replaces each pixel with the median of "
                "its neighbourhood. Particularly useful "
                "for impulse noise.",

            "Bilateral Filter":
                "Edge-preserving smoothing based on both "
                "spatial distance and color similarity.",

            "Guided Filter":
                "Edge-preserving filter based on a local "
                "linear relationship with a guidance image.",

            "Non-Local Means":
                "Denoising method that searches for similar "
                "image patches over a larger area instead "
                "of using only immediate neighbours.",
        }

        algorithm = (
            self.algorithm_combo.currentText()
        )

        self.algorithm_info.setText(
            descriptions[algorithm]
        )

    # ======================================================
    # Utility
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

        if value % 2 == 0:
            value += 1

        return value

    # ======================================================
    # Open image
    # ======================================================

    def open_image(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            "",
            (
                "Image Files "
                "(*.png *.jpg *.jpeg *.bmp *.tif *.tiff)"
            )
        )

        if not file_path:
            return

        image = cv2.imread(
            file_path,
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

        original_pixmap = (
            self.cv_image_to_pixmap(
                image
            )
        )

        self.original_viewer.set_pixmap(
            original_pixmap
        )

        self.processed_viewer.clear_image(
            "No processed image"
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

        height, width = (
            image.shape[:2]
        )

        self.statusBar().showMessage(
            f"Loaded image: {width} × {height}"
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

        self.process_button.setEnabled(
            False
        )

        QApplication.setOverrideCursor(
            Qt.CursorShape.WaitCursor
        )

        start_time = (
            time.perf_counter()
        )

        try:

            # ----------------------------------------------
            # Mean
            # ----------------------------------------------

            if algorithm == "Mean Filter":

                kernel = (
                    self.mean_kernel.value()
                )

                self.processed_image = (
                    MeanFilter.process(
                        self.original_image,
                        kernel
                    )
                )

                parameter_text = (
                    f"Kernel={kernel}"
                )

            # ----------------------------------------------
            # Gaussian
            # ----------------------------------------------

            elif algorithm == "Gaussian Filter":

                kernel = self.make_odd(
                    self.gaussian_kernel.value()
                )

                sigma = (
                    self.gaussian_sigma.value()
                )

                self.processed_image = (
                    GaussianFilter.process(
                        self.original_image,
                        kernel,
                        sigma
                    )
                )

                parameter_text = (
                    f"Kernel={kernel}, "
                    f"Sigma={sigma:.2f}"
                )

            # ----------------------------------------------
            # Median
            # ----------------------------------------------

            elif algorithm == "Median Filter":

                kernel = self.make_odd(
                    self.median_kernel.value(),
                    3
                )

                self.processed_image = (
                    MedianFilter.process(
                        self.original_image,
                        kernel
                    )
                )

                parameter_text = (
                    f"Kernel={kernel}"
                )

            # ----------------------------------------------
            # Bilateral
            # ----------------------------------------------

            elif algorithm == "Bilateral Filter":

                diameter = (
                    self.bilateral_diameter.value()
                )

                sigma_color = (
                    self.bilateral_sigma_color.value()
                )

                sigma_space = (
                    self.bilateral_sigma_space.value()
                )

                self.processed_image = (
                    BilateralFilter.process(
                        self.original_image,
                        diameter,
                        sigma_color,
                        sigma_space
                    )
                )

                parameter_text = (
                    f"d={diameter}, "
                    f"σColor={sigma_color:.1f}, "
                    f"σSpace={sigma_space:.1f}"
                )

            # ----------------------------------------------
            # Guided
            # ----------------------------------------------

            elif algorithm == "Guided Filter":

                radius = (
                    self.guided_radius.value()
                )

                epsilon = (
                    self.guided_epsilon.value()
                )

                self.processed_image = (
                    GuidedFilter.process(
                        self.original_image,
                        radius,
                        epsilon
                    )
                )

                parameter_text = (
                    f"Radius={radius}, "
                    f"Epsilon={epsilon:.4f}"
                )

            # ----------------------------------------------
            # Non-Local Means
            # ----------------------------------------------

            elif algorithm == "Non-Local Means":

                strength = (
                    self.nlm_strength.value()
                )

                color_strength = (
                    self.nlm_color_strength.value()
                )

                template_window = (
                    self.make_odd(
                        self.nlm_template.value(),
                        3
                    )
                )

                search_window = (
                    self.make_odd(
                        self.nlm_search.value(),
                        7
                    )
                )

                self.processed_image = (
                    NonLocalMeansFilter.process(
                        self.original_image,
                        strength,
                        color_strength,
                        template_window,
                        search_window
                    )
                )

                parameter_text = (
                    f"h={strength:.1f}, "
                    f"hColor={color_strength:.1f}, "
                    f"Template={template_window}, "
                    f"Search={search_window}"
                )

            else:
                return

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

        elapsed_time = (
            time.perf_counter()
            - start_time
        )

        # ----------------------------------------------
        # Display
        # ----------------------------------------------

        processed_pixmap = (
            self.cv_image_to_pixmap(
                self.processed_image
            )
        )

        self.processed_viewer.set_pixmap(
            processed_pixmap
        )

        # Match the current original view.
        if self.sync_checkbox.isChecked():

            state = (
                self.original_viewer.get_view_state()
            )

            self.processed_viewer.apply_view_state(
                *state
            )

        self.save_button.setEnabled(
            True
        )

        height, width = (
            self.processed_image.shape[:2]
        )

        self.statusBar().showMessage(
            (
                f"{algorithm} completed | "
                f"{parameter_text} | "
                f"{width} × {height} | "
                f"{elapsed_time:.3f} s"
            )
        )

    # ======================================================
    # Reset
    # ======================================================

    def reset_result(self):

        self.processed_image = None

        self.processed_viewer.clear_image(
            "No processed image"
        )

        self.save_button.setEnabled(
            False
        )

        self.statusBar().showMessage(
            "Processing result reset"
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

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Processed Image",
            "processed_image.png",
            (
                "PNG Image (*.png);;"
                "JPEG Image (*.jpg *.jpeg);;"
                "Bitmap Image (*.bmp)"
            )
        )

        if not file_path:
            return

        success = cv2.imwrite(
            file_path,
            self.processed_image
        )

        if success:

            self.statusBar().showMessage(
                f"Saved: {file_path}"
            )

        else:

            QMessageBox.critical(
                self,
                "Save Error",
                "The image could not be saved."
            )

    # ======================================================
    # OpenCV -> Qt
    # ======================================================

    @staticmethod
    def cv_image_to_pixmap(
        image
    ):

        rgb_image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )

        height, width, channels = (
            rgb_image.shape
        )

        bytes_per_line = (
            channels * width
        )

        q_image = QImage(
            rgb_image.data,
            width,
            height,
            bytes_per_line,
            QImage.Format.Format_RGB888
        )

        q_image = q_image.copy()

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

        if not self.sync_checkbox.isChecked():
            return

        if not self.processed_viewer.has_image():
            return

        self.processed_viewer.apply_view_state(
            zoom,
            x,
            y
        )

    def sync_from_processed(
        self,
        zoom,
        x,
        y
    ):

        if not self.sync_checkbox.isChecked():
            return

        if not self.original_viewer.has_image():
            return

        self.original_viewer.apply_view_state(
            zoom,
            x,
            y
        )

    def sync_toggled(
        self,
        checked
    ):

        if not checked:
            return

        if (
            self.original_viewer.has_image()
            and self.processed_viewer.has_image()
        ):

            state = (
                self.original_viewer.get_view_state()
            )

            self.processed_viewer.apply_view_state(
                *state
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

    def actual_size_views(self):

        if self.original_viewer.has_image():

            self.original_viewer.actual_size()

        if (
            not self.sync_checkbox.isChecked()
            and self.processed_viewer.has_image()
        ):

            self.processed_viewer.actual_size()

    def update_zoom_label(
        self,
        percent
    ):

        self.zoom_label.setText(
            f"Zoom: {percent:.0f}%"
        )