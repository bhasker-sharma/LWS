import serial

class SerialHandler:
	def __init__(self,baud_rate: int, port: str):
		self.port = port
		self.baud_rate = baud_rate
		self.connection = None
		
	def initialize_connection(self):
		try:
			self.connection = serial.Serial(self.port , self.baud_rate)
			print(f"Serial connection established on {self.port} at {self.baud_rate}")
		except serial.SerialException as e:
			print(f"Error initializing serial communication: {e}")
			self.connection = None 
		
	def read_data(self):
		if self.connection and self.connection.in_waiting > 0:
			data_line =  self.connection.readline().decode('utf-8', errors ='replace').strip()
			if data_line:
				parts = data_line.split(',')
				if len(parts) == 4:
					return{
						"SNO":parts[0],
						"Xdata": parts[1],
						"Ydata": parts[2],
						"Zdata":parts[3]
						}
				else:
					print(f"Invalid data point: {data_line}")
			return None
			
serial_handler =  SerialHandler(port='/dev/ttyAMA2',baud_rate=115200)
serial_handler.initialize_connection()
						
