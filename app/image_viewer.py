from PySide6.QtCore import (
    Qt,
    Signal
)

from PySide6.QtGui import (
    QColor,
    QPainter,
    QPixmap
)

from PySide6.QtWidgets import (
    QGraphicsView,
    QGraphicsScene
)


class ImageViewer(QGraphicsView):

    # zoom factor relative to Fit mode,
    # followed by normalized X/Y centre.
    viewChanged = Signal(
        float,
        float,
        float
    )

    # Actual screen scale percentage.
    zoomPercentChanged = Signal(float)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._scene = QGraphicsScene(self)

        self.setScene(self._scene)

        self._pixmap_item = None

        self._zoom_factor = 1.0

        self._sync_blocked = False

        # ----------------------------------------
        # Viewer appearance
        # ----------------------------------------

        self.setBackgroundBrush(
            QColor("#202020")
        )

        self.setRenderHint(
            QPainter.RenderHint.SmoothPixmapTransform,
            True
        )

        self.setMinimumSize(
            350,
            300
        )

        # ----------------------------------------
        # Mouse behaviour
        # ----------------------------------------

        self.setDragMode(
            QGraphicsView.DragMode.ScrollHandDrag
        )

        self.setTransformationAnchor(
            QGraphicsView.ViewportAnchor.AnchorUnderMouse
        )

        self.setResizeAnchor(
            QGraphicsView.ViewportAnchor.AnchorViewCenter
        )

        # ----------------------------------------
        # Detect panning
        # ----------------------------------------

        self.horizontalScrollBar().valueChanged.connect(
            self._on_view_moved
        )

        self.verticalScrollBar().valueChanged.connect(
            self._on_view_moved
        )

        self.clear_image(
            "No image loaded"
        )

    # =====================================================
    # Image
    # =====================================================

    def set_pixmap(self, pixmap):

        self._sync_blocked = True

        self._scene.clear()

        self._pixmap_item = (
            self._scene.addPixmap(pixmap)
        )

        self._pixmap_item.setTransformationMode(
            Qt.TransformationMode.SmoothTransformation
        )

        self._scene.setSceneRect(
            self._pixmap_item.boundingRect()
        )

        self._sync_blocked = False

        self.fit_to_window()

    def clear_image(
        self,
        message="No image loaded"
    ):

        self._sync_blocked = True

        self._scene.clear()

        self._pixmap_item = None

        self.resetTransform()

        self._zoom_factor = 1.0

        text_item = self._scene.addText(
            message
        )

        text_item.setDefaultTextColor(
            QColor("#AAAAAA")
        )

        text_rect = (
            text_item.boundingRect()
        )

        text_item.setPos(
            -text_rect.width() / 2,
            -text_rect.height() / 2
        )

        self._scene.setSceneRect(
            -200,
            -100,
            400,
            200
        )

        self.centerOn(0, 0)

        self._sync_blocked = False

    def has_image(self):

        return self._pixmap_item is not None

    # =====================================================
    # Fit
    # =====================================================

    def fit_to_window(self):

        if not self.has_image():
            return

        self._sync_blocked = True

        self.resetTransform()

        self.fitInView(
            self._pixmap_item,
            Qt.AspectRatioMode.KeepAspectRatio
        )

        self._zoom_factor = 1.0

        self.centerOn(
            self._pixmap_item.boundingRect().center()
        )

        self._sync_blocked = False

        self._emit_view_state()

    # =====================================================
    # 100% view
    # =====================================================

    def actual_size(self):

        if not self.has_image():
            return

        normalized_x, normalized_y = (
            self._normalized_center()
        )

        self._sync_blocked = True

        # First determine Fit scale.
        self.resetTransform()

        self.fitInView(
            self._pixmap_item,
            Qt.AspectRatioMode.KeepAspectRatio
        )

        fit_scale = self.transform().m11()

        # 1 image pixel = 1 screen pixel.
        self.resetTransform()

        if fit_scale > 0:

            self._zoom_factor = (
                1.0 / fit_scale
            )

        rect = (
            self._pixmap_item.boundingRect()
        )

        center_x = (
            rect.left()
            + normalized_x * rect.width()
        )

        center_y = (
            rect.top()
            + normalized_y * rect.height()
        )

        self.centerOn(
            center_x,
            center_y
        )

        self._sync_blocked = False

        self._emit_view_state()

    # =====================================================
    # Mouse wheel zoom
    # =====================================================

    def wheelEvent(self, event):

        if not self.has_image():

            super().wheelEvent(event)

            return

        delta = event.angleDelta().y()

        if delta == 0:
            return

        if delta > 0:
            factor = 1.25
        else:
            factor = 0.8

        new_zoom = (
            self._zoom_factor * factor
        )

        # Prevent extreme zoom levels.
        if not 0.1 <= new_zoom <= 30.0:
            return

        self._sync_blocked = True

        self.scale(
            factor,
            factor
        )

        self._zoom_factor = (
            new_zoom
        )

        self._sync_blocked = False

        self._emit_view_state()

        event.accept()

    # =====================================================
    # View synchronization
    # =====================================================

    def _normalized_center(self):

        if not self.has_image():

            return 0.5, 0.5

        rect = (
            self._pixmap_item.boundingRect()
        )

        centre = self.mapToScene(
            self.viewport().rect().center()
        )

        if rect.width() == 0:
            normalized_x = 0.5
        else:
            normalized_x = (
                centre.x() - rect.left()
            ) / rect.width()

        if rect.height() == 0:
            normalized_y = 0.5
        else:
            normalized_y = (
                centre.y() - rect.top()
            ) / rect.height()

        normalized_x = max(
            0.0,
            min(1.0, normalized_x)
        )

        normalized_y = max(
            0.0,
            min(1.0, normalized_y)
        )

        return (
            normalized_x,
            normalized_y
        )

    def get_view_state(self):

        normalized_x, normalized_y = (
            self._normalized_center()
        )

        return (
            self._zoom_factor,
            normalized_x,
            normalized_y
        )

    def apply_view_state(
        self,
        zoom_factor,
        normalized_x,
        normalized_y
    ):

        if not self.has_image():
            return

        self._sync_blocked = True

        # Establish the Fit transformation first.
        self.resetTransform()

        self.fitInView(
            self._pixmap_item,
            Qt.AspectRatioMode.KeepAspectRatio
        )

        # Then apply relative zoom.
        self.scale(
            zoom_factor,
            zoom_factor
        )

        self._zoom_factor = (
            zoom_factor
        )

        rect = (
            self._pixmap_item.boundingRect()
        )

        centre_x = (
            rect.left()
            + normalized_x * rect.width()
        )

        centre_y = (
            rect.top()
            + normalized_y * rect.height()
        )

        self.centerOn(
            centre_x,
            centre_y
        )

        self._sync_blocked = False

        self.zoomPercentChanged.emit(
            self.transform().m11() * 100.0
        )

    # =====================================================
    # Signals
    # =====================================================

    def _on_view_moved(self):

        if self._sync_blocked:
            return

        self._emit_view_state()

    def _emit_view_state(self):

        if (
            self._sync_blocked
            or not self.has_image()
        ):
            return

        normalized_x, normalized_y = (
            self._normalized_center()
        )

        self.viewChanged.emit(
            self._zoom_factor,
            normalized_x,
            normalized_y
        )

        self.zoomPercentChanged.emit(
            self.transform().m11() * 100.0
        )

    # =====================================================
    # Resize
    # =====================================================

    def resizeEvent(self, event):

        if not self.has_image():

            super().resizeEvent(event)

            return

        state = (
            self.get_view_state()
        )

        super().resizeEvent(event)

        self.apply_view_state(
            *state
        )