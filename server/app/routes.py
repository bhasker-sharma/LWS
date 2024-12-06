from fastapi import APIRouter, WebSocket, Request
from fastapi.responses import HTMLResponse
from app.data import serial_handler
from app.sta_lta import StaLtaDetector
import asyncio

router = APIRouter()

sta_lta_detector = None


# Serve the real-time data page
@router.get("/data", response_class=HTMLResponse)
async def data_page():
    with open("templates/data.html", "r") as file:
        return file.read()

# STA/LTA Algorithm Execution Endpoint
@router.post("/start_detection")
async def start_detection(request: Request):
    global sta_lta_detector
    form_data = await request.form()
    sta_window = int(form_data["sta_window"])
    lta_window = int(form_data["lta_window"])
    threshold = float(form_data["threshold"])

    sta_lta_detector = StaLtaDetector(sta_window, lta_window, threshold, serial_handler)
    
    # Start the detection process in the background
    asyncio.create_task(sta_lta_detector.start_detection())
    
    return {"message": "Seismic detection started with the provided parameters."}

# WebSocket endpoint for real-time sensor data
@router.websocket("/ws/data")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    if not serial_handler.connection:
        await websocket.send_json({"error": "Serial connection not initialized."})
        await websocket.close()
        return

    try:
        while True:
            data_point = serial_handler.read_data()
            if data_point:
                await websocket.send_json(data_point)
            await asyncio.sleep(0.01)  # ~100 fps
    except Exception as e:
        print(f"WebSocket connection error: {e}")
    finally:
        try:
            await websocket.close()
        except Exception as close_error:
            print(f"erors closing websocket: {close_error}")
