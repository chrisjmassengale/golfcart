# FastAPI web interface — phone/tablet control
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "GolfCart online"}

# TODO: live camera stream
# TODO: mode switching (follow, navigate, stop)
# TODO: recording trigger
# TODO: telemetry websocket
