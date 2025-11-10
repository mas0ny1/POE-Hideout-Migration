import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QSpinBox, QMessageBox
)
from PyQt6.QtCore import Qt
from hideout_migration import migrate_hideout

class HideoutMigrationGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.source_file = ""
        self.target_file = ""
        self.output_file = ""
        self.initUI()

    def initUI(self):
        self.setWindowTitle('POE Hideout Migration Tool')
        self.setMinimumWidth(600)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # Source file selection
        source_layout = QHBoxLayout()
        self.source_label = QLabel('No source file selected')
        source_btn = QPushButton('Select Source Hideout')
        source_btn.clicked.connect(self.select_source)
        source_layout.addWidget(QLabel('Source:'))
        source_layout.addWidget(self.source_label, 1)
        source_layout.addWidget(source_btn)
        layout.addLayout(source_layout)

        # Target file selection
        target_layout = QHBoxLayout()
        self.target_label = QLabel('No target file selected')
        target_btn = QPushButton('Select Target Hideout')
        target_btn.clicked.connect(self.select_target)
        target_layout.addWidget(QLabel('Target:'))
        target_layout.addWidget(self.target_label, 1)
        target_layout.addWidget(target_btn)
        layout.addLayout(target_layout)

        # Output file selection
        output_layout = QHBoxLayout()
        self.output_label = QLabel('No output file selected')
        output_btn = QPushButton('Select Output Location')
        output_btn.clicked.connect(self.select_output)
        output_layout.addWidget(QLabel('Output:'))
        output_layout.addWidget(self.output_label, 1)
        output_layout.addWidget(output_btn)
        layout.addLayout(output_layout)

        # Offset controls
        offset_layout = QHBoxLayout()
        
        # X offset
        x_layout = QHBoxLayout()
        x_layout.addWidget(QLabel('X Offset:'))
        self.x_spin = QSpinBox()
        self.x_spin.setRange(-1000, 1000)
        self.x_spin.setValue(0)
        x_layout.addWidget(self.x_spin)
        offset_layout.addLayout(x_layout)
        
        # Y offset
        y_layout = QHBoxLayout()
        y_layout.addWidget(QLabel('Y Offset:'))
        self.y_spin = QSpinBox()
        self.y_spin.setRange(-1000, 1000)
        self.y_spin.setValue(0)
        y_layout.addWidget(self.y_spin)
        offset_layout.addLayout(y_layout)
        
        layout.addLayout(offset_layout)

        # Help text
        help_text = """
        Instructions:
        1. Select the source hideout file (from hideoutshowcase.com)
        2. Select the target hideout file (exported from your game)
        3. Choose where to save the output file
        4. Adjust X and Y offsets to move decorations
        5. Click 'Migrate Hideout' to generate the new hideout file
        """
        help_label = QLabel(help_text)
        help_label.setWordWrap(True)
        layout.addWidget(help_label)

        # Migrate button
        migrate_btn = QPushButton('Migrate Hideout')
        migrate_btn.clicked.connect(self.migrate)
        migrate_btn.setMinimumHeight(40)
        layout.addWidget(migrate_btn)

    def select_source(self):
        file, _ = QFileDialog.getOpenFileName(
            self,
            "Select Source Hideout File",
            "",
            "Hideout Files (*.hideout);;All Files (*.*)"
        )
        if file:
            self.source_file = file
            self.source_label.setText(os.path.basename(file))

    def select_target(self):
        file, _ = QFileDialog.getOpenFileName(
            self,
            "Select Target Hideout File",
            "",
            "Hideout Files (*.hideout);;All Files (*.*)"
        )
        if file:
            self.target_file = file
            self.target_label.setText(os.path.basename(file))

    def select_output(self):
        file, _ = QFileDialog.getSaveFileName(
            self,
            "Select Output Location",
            "",
            "Hideout Files (*.hideout);;All Files (*.*)"
        )
        if file:
            self.output_file = file
            self.output_label.setText(os.path.basename(file))

    def migrate(self):
        if not all([self.source_file, self.target_file, self.output_file]):
            QMessageBox.warning(
                self,
                "Missing Files",
                "Please select all required files (source, target, and output) before migrating."
            )
            return

        try:
            # If spinboxes are at 0, use automatic waypoint-based offsets
            x_offset = None if self.x_spin.value() == 0 else self.x_spin.value()
            y_offset = None if self.y_spin.value() == 0 else self.y_spin.value()
            
            x_used, y_used = migrate_hideout(
                self.source_file,
                self.target_file,
                x_offset,
                y_offset,
                self.output_file
            )
            
            # Update spinboxes with the actually used values
            self.x_spin.setValue(x_used)
            self.y_spin.setValue(y_used)
            QMessageBox.information(
                self,
                "Success",
                f"Hideout successfully migrated!\nSaved to: {self.output_file}\n\n"
                f"Applied offsets: X={self.x_spin.value()}, Y={self.y_spin.value()}"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"An error occurred while migrating the hideout:\n{str(e)}"
            )

def main():
    app = QApplication(sys.argv)
    window = HideoutMigrationGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()