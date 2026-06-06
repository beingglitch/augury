
from fastapi import FastAPI
import uvicorn
from pprint import pprint

from app.parser import parse_log

app = FastAPI(title="Augury", version="0.1.0")


@app.get("/", tags=["root"])
async def read_root():
	return {"message": "Welcome to Augury API"}


if __name__ == "__main__":
	# uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
	result  = parse_log("../../logs/test.bin")
	from app.detectors import attitude
	attitude_changes = attitude.detect_attitude_changes(result)
	pprint(attitude_changes)