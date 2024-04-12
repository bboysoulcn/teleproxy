from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx
import uvicorn

app = FastAPI()


@app.post("/{path:path}")
async def forward_request(request: Request, path: str):
    # 获取原始请求的方法、头部和数据
    headers = dict(request.headers)
    headers['content-type'] = 'application/json'
    headers['host'] = 'api.telegram.org'
    headers.pop('content-length', None)
    body = await request.body()
    data = body.decode('utf-8')

    # 创建新的请求URL
    new_url = 'https://api.telegram.org/' + path

    # 使用httpx发送新的请求
    if data:
        response = httpx.post(new_url, headers=headers, params=data, timeout=1000)
    else:
        response = httpx.post(new_url, headers=headers, timeout=1000)
    return JSONResponse(response.json())

@app.get("/")
async def hello_world():
    return "Hello World"

if __name__ == '__main__':
    uvicorn.run(app='main:app', port=8000, host="0.0.0.0", workers=5)
