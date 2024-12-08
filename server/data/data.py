import serial
import threading
import time
import csv
from datetime import datetime
import logging

# Logging configuration
def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(logging.ERROR)  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        console_handler = logging.StreamHandler()  # Log to the console
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    return logger

logger = get_logger(__name__)

class listNode:
    def __init__(self, val, nxt, prev):
        self.val = val
        self.next = nxt  # it is the starting pointer of circular queue 
        self.prev = prev # it is the end pointer of the circular queue

class MyCircularQueue:
    def __init__(self, k: int):
        self.space = k
        self.left = listNode(0, None, None)
        self.right = listNode(0, None, self.left)
        self.left.next = self.right

    def enQueue(self, value: int) -> bool:
        if self.space == 0:
            logger.warning("Queue is full. Cannot enqueue.")
            return False
        cur = listNode(value, self.right, self.right.prev)
        self.right.prev.next = cur 
        self.right.prev = cur
        self.space -= 1
        logger.info(f"Enqueued value: {value}. Space remaining: {self.space}.")
        return True
    
    def deQueue(self) -> bool:
        if self.isEmpty():
            logger.warning("Queue is empty. Cannot dequeue.")
            return False
        removed_value = self.left.next.val
        self.left.next = self.left.next.next
        self.left.next.prev = self.left
        self.space += 1
        logger.info(f"Dequeued value: {removed_value}. Space available: {self.space}.")
        return True
    
    def Front(self) -> int:
        if self.isEmpty():
            logger.warning("Queue is empty. Cannot access front value.")
            return -1
        return self.left.next.val

    def Rear(self) -> int:
        if self.isEmpty():
            logger.warning("Queue is empty. Cannot access rear value.")
            return -1
        return self.right.prev.val

    def isEmpty(self) -> bool:
        return self.left.next == self.right
    
    def isFull(self) -> bool:
        return self.space == 0

    
class SensorDataReader:
    def __init__(self, port, baud_rate, queue_size):
        self.port = port
        self.baud_rate = baud_rate
        self.serial_connection = serial.Serial(self.port, self.baud_rate)
        self.data_queue = MyCircularQueue(queue_size)
        self.lock = threading.Lock()
        
        self.read_thread = threading.Thread(target=self.read_data)
        self.read_thread.start()
        logger.info(f"Started data reading thread on port: {self.port} with baud rate: {self.baud_rate}")

    def read_data(self):
        while True:
            if self.serial_connection.in_waiting > 0:
                data_line = self.serial_connection.readline().decode('utf-8', errors='replace').strip()
                part = data_line.split(',')
                if len(part) == 4:
                    data_point = {
                        "SNO": part[0],
                        "Xdata": part[1],
                        "Ydata": part[2],
                        "Zdata": part[3]
                    }
                    logger.debug(f"Read data: {data_point}")
                    with self.lock:
                        if self.data_queue.isFull():
                            self.data_queue.deQueue()
                        self.data_queue.enQueue(data_point)

            
            time.sleep(0.005)

    def get_data(self):
        with self.lock:
            data_list = []
            current = self.data_queue.left.next
            while current != self.data_queue.right:
                data_list.append(current.val)
                current = current.next
            return data_list
    
    def stop(self):
        self.csv_writer.close()
        self.read_thread.join()
