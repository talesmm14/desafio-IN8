import uvicorn
import asyncio
from fastapi import FastAPI
from scraping import get_products, URLS_PRODUCTS

menu = dict(URLS_PRODUCTS)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get("/products/")
async def products():
    return await get_products()


@app.get(f"/products/{menu['computers']}")
async def computers():
    return await get_products(menu['computers'])


@app.get(f"/products/{menu['laptops']}")
async def laptops():
    return await get_products(menu['laptops'])


@app.get(f"/products/{menu['phones']}")
async def phones():
    return await get_products(menu['phones'])


@app.get(f"/products/{menu['tablets']}")
async def tablets():
    return await get_products(menu['tablets'])


@app.get(f"/products/{menu['tablets']}")
async def tablets():
    return await get_products(menu['tablets'])


@app.get(f"/products/{menu['touch']}")
async def touch():
    return await get_products(menu['touch'])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
        port=8000
    )
    