import serial
import time
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
from scipy.signal import find_peaks

class ArduinoSensorReader:
    def __init__(self, port, baud_rate=9600, buffer_size=200):
        """
        Initialize the sensor reader with Arduino serial connection
        
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
        self.temp_buffer = deque(maxlen=buffer_size)  # New buffer for temperature
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
        Read PPG and temperature data from Arduino for a specified duration
        
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
            
            print("Reading sensor data... Press Ctrl+C to stop")
            while True:
                if end_time and time.time() > end_time:
                    break
                    
                # Read a line from the serial port
                if self.serial_connection.in_waiting > 0:
                    line = self.serial_connection.readline().decode('utf-8').strip()
                    try:
                        # Convert the received string to ppg and temperature values (CSV format)
                        values = line.split(',')
                        if len(values) == 2:
                            ppg_value = float(values[0])
                            temp_value = float(values[1])
                            current_time = time.time() - self.start_time
                            
                            # Add to buffers
                            self.ppg_buffer.append(ppg_value)
                            self.temp_buffer.append(temp_value)
                            self.time_buffer.append(current_time)
                            
                            print(f"Time: {current_time:.2f}s, PPG: {ppg_value}, Temp: {temp_value:.2f}°C")
                        else:
                            print(f"Invalid data format: {line}")
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
        Save collected sensor data to a CSV file
        
        Args:
            filename (str): Name of the file to save data to
        """
        if not self.ppg_buffer:
            print("No data to save")
            return
            
        try:
            with open(filename, 'w') as f:
                f.write("Time,PPG,Temperature\n")
                for time_val, ppg_val, temp_val in zip(self.time_buffer, self.ppg_buffer, self.temp_buffer):
                    f.write(f"{time_val:.3f},{ppg_val},{temp_val:.2f}\n")
            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving data: {e}")
            
    def plot_data(self):
        """Plot the collected sensor data"""
        if not self.ppg_buffer:
            print("No data to plot")
            return
            
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
        
        # Plot PPG signal
        ax1.plot(list(self.time_buffer), list(self.ppg_buffer), 'b-')
        ax1.set_title("PPG Signal")
        ax1.set_ylabel("PPG Value")
        ax1.grid(True)
        
        # Plot temperature signal
        ax2.plot(list(self.time_buffer), list(self.temp_buffer), 'r-')
        ax2.set_title("Temperature")
        ax2.set_xlabel("Time (seconds)")
        ax2.set_ylabel("Temperature (°C)")
        ax2.grid(True)
        
        plt.tight_layout()
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
    
    def get_average_temperature(self):
        """Calculate the average temperature from collected data"""
        if not self.temp_buffer:
            print("No temperature data available")
            return None
        
        avg_temp = np.mean(list(self.temp_buffer))
        print(f"Average temperature: {avg_temp:.2f}°C")
        return avg_temp
    

# Example usage
if __name__ == "__main__":
    # To check port run on terminal: ls /dev/tty.*
    
    port = '/dev/tty.usbserial-AQ01PO2L'
    sensor_reader = ArduinoSensorReader(port=port)
    
    if sensor_reader.connect():
        try:
            # Read data for 30 seconds
            sensor_reader.read_data(duration=10)
            
            # Analyze heart rate
            sensor_reader.analyze_heart_rate()
            
            # Get average temperature
            sensor_reader.get_average_temperature()
            
            # Plot the data
            sensor_reader.plot_data()
            
            # Calculate HRV
            hrv_metrics = sensor_reader.calculate_hrv()
            
            # Save the data
            sensor_reader.save_data('sensor_data.csv')
            
        finally:
            sensor_reader.disconnect()