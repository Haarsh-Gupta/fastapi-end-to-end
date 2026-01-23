from fastapi import Request
import time 


async def timing_middleware(request: Request , call_next):
    start = time.time()
    response = await call_next(request)
    response.headers["X-Time"] = f"{time.time() - start:.4f}s"
    print(f"Url : {request.url} Time :{response.headers["x-time"]}")
    return response

