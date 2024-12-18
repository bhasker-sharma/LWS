from fastapi import FastAPI
from core.routes import router
import uvicorn 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
        
