from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QDoubleSpinBox,
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from ..core.compressor import SUPPORTED_OUTPUT_FORMATS, resize_and_compress

BYTES_PER_MB = 1024 * 1024


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Image Resizer")
        self.setMinimumWidth(700)

        self.input_path_edit = QLineEdit()
        self.input_path_edit.setPlaceholderText("Choose the source image")

        self.output_path_edit = QLineEdit()
        self.output_path_edit.setPlaceholderText("Choose where to save the resized image")

        self.width_spin = QSpinBox()
        self.width_spin.setRange(1, 10000)
        self.width_spin.setValue(1280)

        self.height_spin = QSpinBox()
        self.height_spin.setRange(1, 10000)
        self.height_spin.setValue(720)

        self.quality_spin = QSpinBox()
        self.quality_spin.setRange(1, 95)
        self.quality_spin.setValue(85)

        self.keep_ratio_check = QCheckBox("Keep aspect ratio")
        self.keep_ratio_check.setChecked(True)

        self.target_size_check = QCheckBox("Target file size")
        self.target_size_check.toggled.connect(self._toggle_target_size)

        self.target_size_spin = QDoubleSpinBox()
        self.target_size_spin.setRange(0.1, 500.0)
        self.target_size_spin.setDecimals(1)
        self.target_size_spin.setSingleStep(0.5)
        self.target_size_spin.setSuffix(" MB")
        self.target_size_spin.setValue(5.0)
        self.target_size_spin.setEnabled(False)

        self.status_label = QLabel("Select an image to begin.")
        self.status_label.setWordWrap(True)
        self.status_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        self.status_label.setObjectName("statusLabel")

        self._build_ui()

    def _build_ui(self) -> None:
        root = QWidget()
        self.setCentralWidget(root)

        main_layout = QVBoxLayout(root)
        main_layout.setContentsMargins(18, 18, 18, 18)
        main_layout.setSpacing(16)

        main_layout.addWidget(self._build_files_group())

        settings_row = QHBoxLayout()
        settings_row.setSpacing(16)
        settings_row.addWidget(self._build_resize_group(), 1)
        settings_row.addWidget(self._build_compression_group(), 1)
        main_layout.addLayout(settings_row)

        run_btn = QPushButton("Resize && Save")
        run_btn.setMinimumHeight(42)
        run_btn.clicked.connect(self._run_resize)

        status_group = QGroupBox("Status")
        status_layout = QVBoxLayout(status_group)
        status_layout.setContentsMargins(14, 12, 14, 12)
        status_layout.addWidget(self.status_label)

        main_layout.addWidget(run_btn)
        main_layout.addWidget(status_group)

        root.setStyleSheet(
            """
            QGroupBox {
                font-weight: 600;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 4px;
            }
            #statusLabel {
                color: #303030;
            }
            """
        )

    def _build_files_group(self) -> QGroupBox:
        group = QGroupBox("Files")
        layout = QVBoxLayout(group)
        layout.setContentsMargins(14, 18, 14, 14)
        layout.setSpacing(12)

        layout.addWidget(
            self._build_labeled_path_row("Input image", self.input_path_edit, self._pick_input)
        )
        layout.addWidget(
            self._build_labeled_path_row("Output image", self.output_path_edit, self._pick_output)
        )
        return group

    def _build_resize_group(self) -> QGroupBox:
        group = QGroupBox("Resize Settings")
        layout = QGridLayout(group)
        layout.setContentsMargins(14, 18, 14, 14)
        layout.setHorizontalSpacing(12)
        layout.setVerticalSpacing(12)
        layout.setColumnStretch(1, 1)

        layout.addWidget(self._make_right_label("Max width"), 0, 0)
        layout.addWidget(self.width_spin, 0, 1)
        layout.addWidget(self._make_right_label("Max height"), 1, 0)
        layout.addWidget(self.height_spin, 1, 1)
        layout.addWidget(self._make_right_label("Aspect ratio"), 2, 0)
        layout.addWidget(self._left_aligned_widget(self.keep_ratio_check), 2, 1)
        return group

    def _build_compression_group(self) -> QGroupBox:
        group = QGroupBox("Compression")
        layout = QGridLayout(group)
        layout.setContentsMargins(14, 18, 14, 14)
        layout.setHorizontalSpacing(12)
        layout.setVerticalSpacing(12)
        layout.setColumnStretch(1, 1)

        target_row = QHBoxLayout()
        target_row.setSpacing(10)
        target_row.setContentsMargins(0, 0, 0, 0)
        target_row.addWidget(self.target_size_check)
        target_row.addWidget(self.target_size_spin)
        target_row.addStretch(1)

        target_widget = QWidget()
        target_widget.setLayout(target_row)

        layout.addWidget(self._make_right_label("Max quality"), 0, 0)
        layout.addWidget(self.quality_spin, 0, 1)
        layout.addWidget(self._make_right_label("Size target"), 1, 0)
        layout.addWidget(target_widget, 1, 1)
        return group

    def _build_labeled_path_row(
        self,
        label_text: str,
        line_edit: QLineEdit,
        browse_handler,
    ) -> QWidget:
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        label = QLabel(label_text)

        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(10)
        row.addWidget(line_edit)

        button = QPushButton("Browse")
        button.setFixedWidth(110)
        button.clicked.connect(browse_handler)
        row.addWidget(button)

        layout.addWidget(label)
        layout.addLayout(row)
        return container

    def _make_right_label(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        return label

    def _left_aligned_widget(self, child: QWidget) -> QWidget:
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(child)
        layout.addStretch(1)
        return container

    def _pick_input(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select input image",
            "",
            "Images (*.png *.jpg *.jpeg *.webp *.bmp *.tiff)",
        )
        if path:
            self.input_path_edit.setText(path)
            p = Path(path)
            default_output = p.with_name(f"{p.stem}_resized.jpg")
            self.output_path_edit.setText(str(default_output))

    def _pick_output(self) -> None:
        filters = ";;".join(
            [
                "JPEG (*.jpg *.jpeg)",
                "PNG (*.png)",
                "WEBP (*.webp)",
            ]
        )
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Select output image",
            self.output_path_edit.text() or "output.jpg",
            filters,
        )
        if path:
            self.output_path_edit.setText(path)

    def _toggle_target_size(self, checked: bool) -> None:
        self.target_size_spin.setEnabled(checked)

    def _run_resize(self) -> None:
        input_path = self.input_path_edit.text().strip()
        output_path = self.output_path_edit.text().strip()

        if not input_path:
            QMessageBox.warning(self, "Missing input", "Please select an input image.")
            return
        if not output_path:
            QMessageBox.warning(self, "Missing output", "Please choose an output path.")
            return
        if Path(output_path).suffix.lower() not in SUPPORTED_OUTPUT_FORMATS:
            supported = ", ".join(sorted(SUPPORTED_OUTPUT_FORMATS))
            QMessageBox.warning(
                self,
                "Invalid output format",
                f"Please use one of these extensions: {supported}.",
            )
            return

        target_size_bytes = None
        if self.target_size_check.isChecked():
            target_size_bytes = int(self.target_size_spin.value() * BYTES_PER_MB)

        try:
            result = resize_and_compress(
                input_path=input_path,
                output_path=output_path,
                width=self.width_spin.value(),
                height=self.height_spin.value(),
                quality=self.quality_spin.value(),
                keep_aspect_ratio=self.keep_ratio_check.isChecked(),
                target_size_bytes=target_size_bytes,
            )
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self, "Resize failed", str(exc))
            self.status_label.setText(f"Error: {exc}")
            return

        output_size_mb = Path(result).stat().st_size / BYTES_PER_MB
        self.status_label.setText(
            f"Saved resized image to: {result} ({output_size_mb:.2f} MB)"
        )
        QMessageBox.information(
            self,
            "Done",
            f"Saved to:\n{result}\n\nFinal size: {output_size_mb:.2f} MB",
        )
