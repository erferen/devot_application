from fastapi import FastAPI


from routers import folders_router, files_router

app = FastAPI()

app.include_router(folders_router.router)
app.include_router(files_router.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}