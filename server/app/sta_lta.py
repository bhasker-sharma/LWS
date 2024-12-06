import logging
from .data import serial_handler
import asyncio

class StaLtaDetector:
    def __init__(self, sta_window, lta_window, threshold,serial_handler):
        self.sta_window = sta_window
        self.lta_window = lta_window
        self.threshold = threshold
        self.z_data_buffer = []
        self.serial_handler = serial_handler
        self.logger = logging.getLogger("StaLtaDetector")
        logging.basicConfig(level=logging.INFO)
        self.listeners = []
        
    def calculate_sta_lta(self, z_data):
        self.z_data_buffer.append(z_data)

        # Ensure sufficient data in the buffer
        if len(self.z_data_buffer) < self.lta_window * 2:
            return None

        if len(self.z_data_buffer) > self.lta_window:
            self.z_data_buffer.pop(0)

        sta = sum(self.z_data_buffer[-self.sta_window:]) / self.sta_window
        lta = sum(self.z_data_buffer) / len(self.z_data_buffer)

        self.logger.debug(f"STA: {sta}, LTA: {lta}, Ratio: {sta / lta if lta else 'N/A'}")
        return sta, lta
        
    async def start_detection(self):
        """
        Continuously read data and check for seismic events.
        """
        while True:
            data_point = self.serial_handler.read_data()
            if data_point:
                z_data = float(data_point["Zdata"])
                result = self.calculate_sta_lta(z_data)
                if result:
                    sta, lta = result
                    if self.detect_seismic_activity(sta, lta):
                        self.logger.info("Seismic event detected!")
                        print("Seismic event detected!")
            await asyncio.sleep(0.01)  # Adjust the frequency as needed
            
    def detect_seismic_activity(self, sta, lta):
        return sta / lta > self.threshold if lta else False
    
