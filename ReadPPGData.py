import serial
import time
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
from scipy.signal import find_peaks

class ArduinoPPGReader:
    def __init__(self, port, baud_rate=19200, buffer_size=100):
        """
        Initialize the PPG reader with Arduino serial connection
        
        Args:
            port (str): Serial port the Arduino is connected to (e.g., 'COM3', '/dev/ttyACM0')
            baud_rate (int): Baud rate for serial communication
            buffer_size (int): Size of the data buffer for visualization
        """
        self.port = port
        self.baud_rate = baud_rate
        self.buffer_size = buffer_size
        self.serial_connection = None
        self.ppg_buffer = deque(maxlen=buffer_size)
        self.time_buffer = deque(maxlen=buffer_size)
        self.start_time = None
        
    def connect(self):
        """Establish serial connection with Arduino"""
        try:
            self.serial_connection = serial.Serial(self.port, self.baud_rate)
            print(f"Connected to Arduino on {self.port}")
            # Allow some time for the Arduino to reset
            time.sleep(2)
            self.start_time = time.time()
            return True
        except serial.SerialException as e:
            print(f"Failed to connect to Arduino: {e}")
            return False
            
    def disconnect(self):
        """Close the serial connection"""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print("Disconnected from Arduino")
            
    def read_data(self, duration=None):
        """
        Read PPG data from Arduino for a specified duration
        
        Args:
            duration (float): Duration in seconds to read data (None for continuous)
        """
        if not self.serial_connection or not self.serial_connection.is_open:
            print("Serial connection not established")
            return
            
        try:
            end_time = None
            if duration:
                end_time = time.time() + duration
                
            # Clear any existing data in the buffer
            self.serial_connection.reset_input_buffer()
            
            print("Reading PPG data... Press Ctrl+C to stop")
            while True:
                if end_time and time.time() > end_time:
                    break
                    
                # Read a line from the serial port
                if self.serial_connection.in_waiting > 0:
                    line = self.serial_connection.readline().decode('utf-8').strip()
                    try:
                        # Convert the received string to float (assumes Arduino sends just the PPG value)
                        ppg_value = float(line)
                        current_time = time.time() - self.start_time
                        
                        # Add to buffers
                        self.ppg_buffer.append(ppg_value)
                        self.time_buffer.append(current_time)
                        
                        print(f"Time: {current_time:.2f}s, PPG: {ppg_value}")
                    except ValueError:
                        print(f"Invalid data received: {line}")
                
                # Small delay to prevent CPU overload
                time.sleep(0.01)
                
        except KeyboardInterrupt:
            print("\nStopped reading data")
        except Exception as e:
            print(f"Error reading data: {e}")
            
    def save_data(self, filename):
        """
        Save collected PPG data to a CSV file
        
        Args:
            filename (str): Name of the file to save data to
        """
        if not self.ppg_buffer:
            print("No data to save")
            return
            
        try:
            with open(filename, 'w') as f:
                f.write("Time,PPG\n")
                for time_val, ppg_val in zip(self.time_buffer, self.ppg_buffer):
                    f.write(f"{time_val:.3f},{ppg_val}\n")
            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving data: {e}")
            
    def plot_data(self):
        """Plot the collected PPG data"""
        if not self.ppg_buffer:
            print("No data to plot")
            return
            
        plt.figure(figsize=(10, 6))
        plt.plot(list(self.time_buffer), list(self.ppg_buffer))
        plt.title("PPG Signal from Arduino")
        plt.xlabel("Time (seconds)")
        plt.ylabel("PPG Value")
        plt.grid(True)
        plt.show()
        
    def analyze_heart_rate(self):
        """Simple heart rate analysis from PPG data"""
        if len(self.ppg_buffer) < 10:
            print("Not enough data for heart rate analysis")
            return None
            
        # Convert to numpy array for analysis
        ppg_data = np.array(list(self.ppg_buffer))
        time_data = np.array(list(self.time_buffer))
        
        # Simple peak detection (this is a basic approach)
        # Find peaks with a minimum height and distance
        peaks, _ = find_peaks(ppg_data, height=np.mean(ppg_data), distance=20)
        
        if len(peaks) < 2:
            print("Not enough peaks detected for heart rate calculation")
            return None
            
        # Calculate time between peaks
        peak_times = time_data[peaks]
        intervals = np.diff(peak_times)
        
        # Calculate heart rate (beats per minute)
        heart_rate = 60 / np.mean(intervals)
        
        print(f"Estimated heart rate: {heart_rate:.1f} BPM")
        return heart_rate

    def calculate_hrv(self):
        """Calculate heart rate variability (HRV) from PPG data"""
        if len(self.ppg_buffer) < 10:
            print("Not enough data for HRV analysis")
            return None
        
        ppg_data = np.array(list(self.ppg_buffer))
        time_data = np.array(list(self.time_buffer))
        
        peaks, _ = find_peaks(ppg_data, height=np.mean(ppg_data), distance=20)
        
        if len(peaks) < 2:
            print("Not enough peaks detected for HRV calculation")
            return None
        
        peak_times = time_data[peaks]
        rr_intervals = np.diff(peak_times) * 1000  # Convert to milliseconds
        
        sdnn = np.std(rr_intervals)
        rmssd = np.sqrt(np.mean(np.diff(rr_intervals) ** 2))
        
        print(f"SDNN: {sdnn:.2f} ms, RMSSD: {rmssd:.2f} ms")
        return {"SDNN": sdnn, "RMSSD": rmssd}

# Example usage
if __name__ == "__main__":
    # To check port run on terminal: ls /dev/tty.*
    
    port = '/dev/tty.usbserial-AQ01PO2L'
    ppg_reader = ArduinoPPGReader(port=port)
    
    if ppg_reader.connect():
        try:
            # Read data for 30 seconds
            ppg_reader.read_data(duration=30)
            
            # Analyze heart rate
            ppg_reader.analyze_heart_rate()
            
            # Plot the data
            ppg_reader.plot_data()
            
            # Calculate HRV
            hrv_metrics = ppg_reader.calculate_hrv()
            if hrv_metrics:
                print(f"SDNN: {hrv_metrics['SDNN']:.2f} ms, RMSSD: {hrv_metrics['RMSSD']:.2f} ms")
            
            # Save the data
            ppg_reader.save_data('ppg_data.csv')
            
        finally:
            ppg_reader.disconnect()
            