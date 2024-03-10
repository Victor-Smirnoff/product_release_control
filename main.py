import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from exception import ShiftTaskException
from view import shift_task_router


app = FastAPI()
app.include_router(shift_task_router)


@app.exception_handler(ShiftTaskException)
async def currency_exception_handler(request: Request, exc: ShiftTaskException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
