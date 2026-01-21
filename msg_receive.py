import fastapi
import uvicorn
import json

app = fastapi.FastAPI()

@app.post("/aiq")
async def index(request: fastapi.Request):
    try:
        tmp = await request.body()
        tmp = json.loads(tmp.decode('utf-8'))
        msg_queue.put(tmp)
    except:
        pass
    return ''

def main(port, que):
    global msg_queue
    msg_queue = que
    uvicorn.run(app, host="0.0.0.0", port=port)