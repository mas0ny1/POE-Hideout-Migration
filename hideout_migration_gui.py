import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QSpinBox, QMessageBox
)
from PyQt6.QtCore import Qt
from hideout_migration import (
    migrate_hideout, read_hideout_file, extract_language,
    find_waypoint_coords
)

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

        # Offset controls section
        offset_group = QVBoxLayout()
        
        # Current coordinates display
        coords_layout = QHBoxLayout()
        
        # X offset display
        x_layout = QHBoxLayout()
        x_layout.addWidget(QLabel('X Offset:'))
        self.x_spin = QSpinBox()
        self.x_spin.setRange(-1000, 1000)
        self.x_spin.setValue(0)
        self.x_spin.setReadOnly(True)
        x_layout.addWidget(self.x_spin)
        coords_layout.addLayout(x_layout)
        
        # Y offset display
        y_layout = QHBoxLayout()
        y_layout.addWidget(QLabel('Y Offset:'))
        self.y_spin = QSpinBox()
        self.y_spin.setRange(-1000, 1000)
        self.y_spin.setValue(0)
        self.y_spin.setReadOnly(True)
        y_layout.addWidget(self.y_spin)
        coords_layout.addLayout(y_layout)
        
        offset_group.addLayout(coords_layout)
        
        # Step size control
        step_layout = QHBoxLayout()
        step_layout.addWidget(QLabel('Step Size:'))
        self.step_spin = QSpinBox()
        self.step_spin.setRange(1, 100)
        self.step_spin.setValue(30)
        step_layout.addWidget(self.step_spin)
        offset_group.addLayout(step_layout)
        
        # Direction buttons (8 directions + reset)
        buttons_layout = QVBoxLayout()
        
        # North row (NW, N, NE)
        north_layout = QHBoxLayout()
        north_layout.addStretch()
        
        nw_btn = QPushButton('↖')
        nw_btn.setFixedSize(40, 40)
        nw_btn.clicked.connect(lambda: self.move_direction('NW'))
        north_layout.addWidget(nw_btn)
        
        n_btn = QPushButton('↑')
        n_btn.setFixedSize(40, 40)
        n_btn.clicked.connect(lambda: self.move_direction('N'))
        north_layout.addWidget(n_btn)
        
        ne_btn = QPushButton('↗')
        ne_btn.setFixedSize(40, 40)
        ne_btn.clicked.connect(lambda: self.move_direction('NE'))
        north_layout.addWidget(ne_btn)
        
        north_layout.addStretch()
        buttons_layout.addLayout(north_layout)
        
        # Middle row (W, Reset, E)
        middle_layout = QHBoxLayout()
        middle_layout.addStretch()
        
        w_btn = QPushButton('←')
        w_btn.setFixedSize(40, 40)
        w_btn.clicked.connect(lambda: self.move_direction('W'))
        middle_layout.addWidget(w_btn)
        
        reset_btn = QPushButton('R')
        reset_btn.setFixedSize(40, 40)
        reset_btn.clicked.connect(self.reset_offsets)
        middle_layout.addWidget(reset_btn)
        
        e_btn = QPushButton('→')
        e_btn.setFixedSize(40, 40)
        e_btn.clicked.connect(lambda: self.move_direction('E'))
        middle_layout.addWidget(e_btn)
        
        middle_layout.addStretch()
        buttons_layout.addLayout(middle_layout)
        
        # South row (SW, S, SE)
        south_layout = QHBoxLayout()
        south_layout.addStretch()
        
        sw_btn = QPushButton('↙')
        sw_btn.setFixedSize(40, 40)
        sw_btn.clicked.connect(lambda: self.move_direction('SW'))
        south_layout.addWidget(sw_btn)
        
        s_btn = QPushButton('↓')
        s_btn.setFixedSize(40, 40)
        s_btn.clicked.connect(lambda: self.move_direction('S'))
        south_layout.addWidget(s_btn)
        
        se_btn = QPushButton('↘')
        se_btn.setFixedSize(40, 40)
        se_btn.clicked.connect(lambda: self.move_direction('SE'))
        south_layout.addWidget(se_btn)
        
        south_layout.addStretch()
        buttons_layout.addLayout(south_layout)
        
        offset_group.addLayout(buttons_layout)
        layout.addLayout(offset_group)

        # Help text
        help_text = """
        Instructions:
        1. Select the source hideout file (from hideoutshowcase.com)
        2. Select the target hideout file (this should be an empty hideout of the type you want to use)
           NOTE: The target hideout is just for the hideout type - its contents don't matter,
           it's only used to get the correct hideout type information
        3. Choose where to save the output file
        4. Use the directional buttons to adjust the position (step size: 30 units per click)
        5. Click 'Migrate Hideout' to generate the new hideout file
        
        Tip: The 'R' button in the center resets to the waypoint-matched position
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

    def calculate_initial_offsets(self):
        """Calculate initial offsets based on waypoint positions."""
        if not all([self.source_file, self.target_file]):
            return
        
        try:
            # Read both hideout files
            source_lines = read_hideout_file(self.source_file)
            target_lines = read_hideout_file(self.target_file)
            
            # Check languages match
            source_lang = extract_language(source_lines)
            target_lang = extract_language(target_lines)
            
            if source_lang != target_lang:
                QMessageBox.warning(
                    self,
                    "Language Mismatch",
                    f"Source hideout is in {source_lang}, but target hideout is in {target_lang}.\n"
                    "Please use hideout files with matching languages."
                )
                return
            
            # Calculate waypoint-based offsets
            try:
                source_x, source_y = find_waypoint_coords(source_lines)
                target_x, target_y = find_waypoint_coords(target_lines)
                
                x_offset = target_x - source_x
                y_offset = target_y - source_y
                
                self.x_spin.setValue(x_offset)
                self.y_spin.setValue(y_offset)
                
                QMessageBox.information(
                    self,
                    "Offset Calculation",
                    f"Initial offsets calculated based on waypoint positions:\n"
                    f"X offset: {x_offset} (target: {target_x} - source: {source_x})\n"
                    f"Y offset: {y_offset} (target: {target_y} - source: {source_y})"
                )
                
            except ValueError as e:
                QMessageBox.warning(
                    self,
                    "Waypoint Not Found",
                    f"Could not calculate automatic offsets: {str(e)}\n"
                    "Starting with default offsets (0,0)."
                )
                self.x_spin.setValue(0)
                self.y_spin.setValue(0)
                
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"An error occurred while calculating initial offsets:\n{str(e)}"
            )

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
            # Calculate initial offsets once all files are selected
            self.calculate_initial_offsets()

    def move_direction(self, direction: str):
        """
        Move the offset in the specified direction by the current step size.
        On the isometric grid:
        - Increasing X moves Northeast
        - Decreasing X moves Southwest
        - Increasing Y moves Northwest
        - Decreasing Y moves Southeast
        """
        step = self.step_spin.value()
        
        # Direction to coordinate changes mapping for isometric grid
        direction_changes = {
            'N': {'x': step, 'y': step},      # North (NE + NW)
            'S': {'x': -step, 'y': -step},    # South (SW + SE)
            'E': {'x': step, 'y': -step},     # East (NE + SE)
            'W': {'x': -step, 'y': step},     # West (NW + SW)
            'NE': {'x': step, 'y': 0},        # Northeast (X+)
            'SW': {'x': -step, 'y': 0},       # Southwest (X-)
            'NW': {'x': 0, 'y': step},        # Northwest (Y+)
            'SE': {'x': 0, 'y': -step}        # Southeast (Y-)
        }
        
        if direction in direction_changes:
            changes = direction_changes[direction]
            self.x_spin.setValue(self.x_spin.value() + changes['x'])
            self.y_spin.setValue(self.y_spin.value() + changes['y'])
    
    def reset_offsets(self):
        """Reset to the default waypoint-matched coordinates."""
        if not all([self.source_file, self.target_file]):
            QMessageBox.warning(
                self,
                "Files Missing",
                "Please select both source and target hideout files first."
            )
            return
            
        try:
            source_lines = read_hideout_file(self.source_file)
            target_lines = read_hideout_file(self.target_file)
            
            source_x, source_y = find_waypoint_coords(source_lines)
            target_x, target_y = find_waypoint_coords(target_lines)
            
            x_offset = target_x - source_x
            y_offset = target_y - source_y
            
            self.x_spin.setValue(x_offset)
            self.y_spin.setValue(y_offset)
            
            QMessageBox.information(
                self,
                "Reset Complete",
                f"Reset to waypoint-based coordinates:\n"
                f"X offset: {x_offset}\n"
                f"Y offset: {y_offset}"
            )
            
        except Exception as e:
            QMessageBox.warning(
                self,
                "Reset Failed",
                f"Could not reset to waypoint coordinates: {str(e)}\n"
                "Please check that both hideouts have waypoints."
            )

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