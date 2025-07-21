import uvicorn
from fastapi import FastAPI

app: FastAPI = FastAPI()


@app.get("/")
async def root() -> dict[str, str]:
	return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str) -> dict[str, str]:
	return {"message": f"Hello {name}"}


if __name__ == "__main__":
	uvicorn.run(
		"main:app",
		host="",
		port=8080,
		reload=True,
	)
