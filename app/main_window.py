import cv2

from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QComboBox,
    QSlider,
    QDoubleSpinBox,
    QHBoxLayout,
    QVBoxLayout,
    QGroupBox,
    QFormLayout,
)

from algorithms.mean_filter import MeanFilter
from algorithms.gaussian_filter import GaussianFilter
from algorithms.median_filter import MedianFilter


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # --------------------------------------------------
        # Window
        # --------------------------------------------------

        self.setWindowTitle(
            "Image Restoration & Super-Resolution Lab"
        )

        self.resize(1300, 800)

        # --------------------------------------------------
        # Image data
        # --------------------------------------------------

        self.original_image = None
        self.processed_image = None

        self.original_pixmap = None
        self.processed_pixmap = None

        # --------------------------------------------------
        # Main widget
        # --------------------------------------------------

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # --------------------------------------------------
        # Title
        # --------------------------------------------------

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
                padding: 12px;
            }
            """
        )

        main_layout.addWidget(title_label)

        # --------------------------------------------------
        # Image viewers
        # --------------------------------------------------

        image_layout = QHBoxLayout()

        # Original
        original_group = QGroupBox("Original")

        original_layout = QVBoxLayout(original_group)

        self.original_label = QLabel(
            "Open an image to begin"
        )

        self.prepare_image_label(
            self.original_label
        )

        original_layout.addWidget(
            self.original_label
        )

        # Processed
        processed_group = QGroupBox("Processed")

        processed_layout = QVBoxLayout(
            processed_group
        )

        self.processed_label = QLabel(
            "No processed image"
        )

        self.prepare_image_label(
            self.processed_label
        )

        processed_layout.addWidget(
            self.processed_label
        )

        image_layout.addWidget(
            original_group,
            stretch=1
        )

        image_layout.addWidget(
            processed_group,
            stretch=1
        )

        main_layout.addLayout(
            image_layout,
            stretch=1
        )

        # --------------------------------------------------
        # Controls
        # --------------------------------------------------

        controls_group = QGroupBox(
            "Processing Controls"
        )

        controls_layout = QFormLayout(
            controls_group
        )

        # Algorithm
        self.algorithm_combo = QComboBox()

        self.algorithm_combo.addItems(
            [
                "Mean Filter",
                "Gaussian Filter",
                "Median Filter",
            ]
        )

        self.algorithm_combo.currentTextChanged.connect(
            self.update_parameter_visibility
        )

        controls_layout.addRow(
            "Algorithm:",
            self.algorithm_combo
        )

        # Kernel size
        kernel_widget = QWidget()

        kernel_layout = QHBoxLayout(
            kernel_widget
        )

        kernel_layout.setContentsMargins(
            0, 0, 0, 0
        )

        self.kernel_slider = QSlider(
            Qt.Orientation.Horizontal
        )

        self.kernel_slider.setMinimum(1)
        self.kernel_slider.setMaximum(31)
        self.kernel_slider.setValue(5)

        self.kernel_slider.valueChanged.connect(
            self.kernel_changed
        )

        self.kernel_value_label = QLabel("5")

        self.kernel_value_label.setMinimumWidth(30)

        kernel_layout.addWidget(
            self.kernel_slider
        )

        kernel_layout.addWidget(
            self.kernel_value_label
        )

        controls_layout.addRow(
            "Kernel Size:",
            kernel_widget
        )

        # Gaussian sigma
        self.sigma_spinbox = QDoubleSpinBox()

        self.sigma_spinbox.setRange(
            0.0,
            20.0
        )

        self.sigma_spinbox.setDecimals(2)

        self.sigma_spinbox.setSingleStep(
            0.1
        )

        self.sigma_spinbox.setValue(
            1.0
        )

        controls_layout.addRow(
            "Gaussian Sigma:",
            self.sigma_spinbox
        )

        main_layout.addWidget(
            controls_group
        )

        # --------------------------------------------------
        # Buttons
        # --------------------------------------------------

        button_layout = QHBoxLayout()

        self.open_button = QPushButton(
            "Open Image"
        )

        self.process_button = QPushButton(
            "Process"
        )

        self.reset_button = QPushButton(
            "Reset"
        )

        self.save_button = QPushButton(
            "Save Result"
        )

        self.open_button.clicked.connect(
            self.open_image
        )

        self.process_button.clicked.connect(
            self.process_image
        )

        self.reset_button.clicked.connect(
            self.reset_image
        )

        self.save_button.clicked.connect(
            self.save_image
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

        # --------------------------------------------------
        # Status bar
        # --------------------------------------------------

        self.statusBar().showMessage(
            "Ready"
        )

        self.update_parameter_visibility()

    # ======================================================
    # GUI helpers
    # ======================================================

    def prepare_image_label(self, label):

        label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        label.setMinimumSize(
            400,
            400
        )

        label.setStyleSheet(
            """
            QLabel {
                background-color: #202020;
                color: #aaaaaa;
                border: 1px solid #555555;
                font-size: 16px;
            }
            """
        )

    # ======================================================
    # Kernel size
    # ======================================================

    def kernel_changed(self, value):

        # Filters such as Gaussian and Median generally
        # require an odd kernel size.

        if value % 2 == 0:

            value += 1

            if value > self.kernel_slider.maximum():
                value -= 2

            self.kernel_slider.blockSignals(True)
            self.kernel_slider.setValue(value)
            self.kernel_slider.blockSignals(False)

        self.kernel_value_label.setText(
            str(value)
        )

    def get_kernel_size(self):

        value = self.kernel_slider.value()

        if value % 2 == 0:
            value += 1

        algorithm = (
            self.algorithm_combo.currentText()
        )

        # Median kernel must be greater than 1.
        if algorithm == "Median Filter":
            value = max(3, value)

        return value

    # ======================================================
    # Parameters
    # ======================================================

    def update_parameter_visibility(self):

        algorithm = (
            self.algorithm_combo.currentText()
        )

        self.sigma_spinbox.setEnabled(
            algorithm == "Gaussian Filter"
        )

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

        self.original_pixmap = (
            self.cv_image_to_pixmap(
                self.original_image
            )
        )

        self.processed_pixmap = None

        self.display_original_image()

        self.processed_label.clear()

        self.processed_label.setText(
            "No processed image"
        )

        height, width = image.shape[:2]

        self.statusBar().showMessage(
            f"Loaded: {width} × {height}"
        )

    # ======================================================
    # Process image
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

        kernel_size = (
            self.get_kernel_size()
        )

        try:

            if algorithm == "Mean Filter":

                self.processed_image = (
                    MeanFilter.process(
                        self.original_image,
                        kernel_size
                    )
                )

            elif algorithm == "Gaussian Filter":

                sigma = (
                    self.sigma_spinbox.value()
                )

                self.processed_image = (
                    GaussianFilter.process(
                        self.original_image,
                        kernel_size,
                        sigma
                    )
                )

            elif algorithm == "Median Filter":

                self.processed_image = (
                    MedianFilter.process(
                        self.original_image,
                        kernel_size
                    )
                )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Processing Error",
                str(error)
            )

            return

        self.processed_pixmap = (
            self.cv_image_to_pixmap(
                self.processed_image
            )
        )

        self.display_processed_image()

        height, width = (
            self.processed_image.shape[:2]
        )

        self.statusBar().showMessage(
            (
                f"{algorithm} completed | "
                f"Kernel: {kernel_size} | "
                f"Output: {width} × {height}"
            )
        )

    # ======================================================
    # Reset
    # ======================================================

    def reset_image(self):

        if self.original_image is None:
            return

        self.processed_image = None
        self.processed_pixmap = None

        self.processed_label.clear()

        self.processed_label.setText(
            "No processed image"
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

    def cv_image_to_pixmap(self, image):

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

        # copy() is important because the NumPy array
        # may later be replaced or destroyed.

        q_image = q_image.copy()

        return QPixmap.fromImage(
            q_image
        )

    # ======================================================
    # Display
    # ======================================================

    def display_original_image(self):

        if self.original_pixmap is None:
            return

        scaled = self.original_pixmap.scaled(
            self.original_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.original_label.setPixmap(
            scaled
        )

    def display_processed_image(self):

        if self.processed_pixmap is None:
            return

        scaled = self.processed_pixmap.scaled(
            self.processed_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.processed_label.setPixmap(
            scaled
        )

    # ======================================================
    # Window resize
    # ======================================================

    def resizeEvent(self, event):

        super().resizeEvent(event)

        self.display_original_image()
        self.display_processed_image()
        