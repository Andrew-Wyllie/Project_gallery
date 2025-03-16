import sys
import datetime
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QMainWindow)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont

class EarningsTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
        # Tracking variables
        self.start_time = None
        self.total_time = datetime.timedelta()
        self.total_earnings = 0
        self.is_tracking = False
        self.hourly_rate = 11.44
        
        # Timer for updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_tracking)

    def initUI(self):
        self.setWindowTitle('Earnings Tracker')
        self.setGeometry(100, 100, 400, 300)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Hourly Rate Display
        self.rate_label = QLabel(f"Hourly Rate: £11.44")
        self.rate_label.setStyleSheet("color: #00FF00; background-color: black;")
        self.rate_label.setFont(QFont('Courier', 14))
        layout.addWidget(self.rate_label)
        
        # Time Worked Display
        self.time_label = QLabel("Time Worked: 00:00:00")
        self.time_label.setStyleSheet("color: #00FF00; background-color: black;")
        self.time_label.setFont(QFont('Courier', 16, QFont.Bold))
        layout.addWidget(self.time_label)
        
        # Earnings Display
        self.earnings_label = QLabel("Current Earnings: £0.00")
        self.earnings_label.setStyleSheet("color: #00FF00; background-color: black;")
        self.earnings_label.setFont(QFont('Courier', 16, QFont.Bold))
        layout.addWidget(self.earnings_label)
        
        # Buttons Layout
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        
        # Start Button
        self.start_button = QPushButton("Start Tracking")
        self.start_button.setStyleSheet("""
            background-color: #003300; 
            color: #00FF00; 
            border: 1px solid #00FF00;
            padding: 10px;
        """)
        self.start_button.clicked.connect(self.start_tracking)
        button_layout.addWidget(self.start_button)
        
        # Stop Button
        self.stop_button = QPushButton("Stop Tracking")
        self.stop_button.setStyleSheet("""
            background-color: #330000; 
            color: #00FF00; 
            border: 1px solid #00FF00;
            padding: 10px;
        """)
        self.stop_button.clicked.connect(self.stop_tracking)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.stop_button)
        
        # Set overall style
        self.setStyleSheet("""
            QMainWindow {
                background-color: black;
            }
            QWidget {
                background-color: black;
                color: #00FF00;
            }
        """)

    def start_tracking(self):
        if not self.is_tracking:
            self.start_time = datetime.datetime.now()
            self.is_tracking = True
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            
            # Start the timer to update every 100 ms
            self.timer.start(100)

    def stop_tracking(self):
        if self.is_tracking:
            current_time = datetime.datetime.now()
            current_session = current_time - self.start_time
            self.total_time += current_session
            
            total_seconds = self.total_time.total_seconds()
            self.total_earnings = (total_seconds / 3600) * self.hourly_rate
            
            self.is_tracking = False
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            
            # Stop the timer
            self.timer.stop()
            
            # Update labels to show total time and earnings
            self.time_label.setText(f"Total Time: {str(self.total_time).split('.')[0]}")
            self.earnings_label.setText(f"Total Earnings: £{self.total_earnings:.2f}")

    def update_tracking(self):
        if self.is_tracking:
            current_time = datetime.datetime.now()
            current_session = current_time - self.start_time
            total_time = self.total_time + current_session
            
            total_seconds = total_time.total_seconds()
            total_earnings = (total_seconds / 3600) * self.hourly_rate
            
            # Update labels
            self.time_label.setText(f"Time Worked: {str(total_time).split('.')[0]}")
            self.earnings_label.setText(f"Current Earnings: £{total_earnings:.2f}")

def main():
    app = QApplication(sys.argv)
    tracker = EarningsTracker()
    tracker.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()