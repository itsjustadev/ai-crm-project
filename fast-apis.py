import uvicorn
from fastapi import FastAPI, HTTPException, Request

app = FastAPI()

@app.post("/take_clients")
async def process_data(request: Request):
    content_type = request.headers.get("content-type")

    if content_type != "application/x-www-form-urlencoded":
        raise HTTPException(status_code=400, detail="Invalid content type")

    data = await request.form()
    account_id = data.get("account[id]")
    subdomain = data.get("account[subdomain]")
    leads_id = data.get("leads[add][0][id]")

    # Обрабатываем полученные данные
    return {"account_id": account_id, "subdomain": subdomain, "leads_id": leads_id}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)