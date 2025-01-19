from fastapi import FastAPI

app = fastAPI()

@app.get("/")
async def root():
	return {"message": "Hello world"}