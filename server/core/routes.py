from fastapi import APIRouter, WebSocket, Request, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from data.data import SensorDataReader
from threading import Lock
from algorithm.sta_lta import StaLtaDetector
import asyncio

router = APIRouter()

sensor_data_reader = SensorDataReader(
    port="/dev/ttyAMA2", 
    baud_rate=115200, 
    queue_size=1000, 
)
data_lock = Lock()


@router.websocket("/ws/graph")
async def websocket_graph(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            with data_lock:
                data_batch = sensor_data_reader.get_data()
            if data_batch:
                await websocket.send_json(data_batch)
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(f"Error in WEbSocket: {e}")
    finally:
        try:
            await websocket.close()
        except Exception as close_error:
            print(f"Error while closing websocket : {close_error}")
