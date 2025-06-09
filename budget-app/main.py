from fastapi import FastAPI


from routers import categories_router, auth, expenses_router, user_router

app = FastAPI()


app.include_router(auth.router)
app.include_router(categories_router.router)
app.include_router(expenses_router.router)
app.include_router(user_router.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}