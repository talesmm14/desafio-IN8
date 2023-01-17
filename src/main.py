import uvicorn
import asyncio
from operator import itemgetter
from fastapi import FastAPI, Query, APIRouter
from scraping import get_products, URLS_PRODUCTS

menu = dict(URLS_PRODUCTS)


class BasicAPI:
    def __init__(self, name: str):
        self.name = name
        self.router = APIRouter()
        self.url = dict(URLS_PRODUCTS)[self.name]
        self.router.add_api_route(f"/products/{self.name}", self.basic_return, methods=["GET"])
        
    async def basic_return(
        self, 
        search: str | None = Query(
            default=None,
            description="Search by product name"
            ), 
        sort_by_price: bool = Query(
            default=True,
            description="Sort by price"
            )
        ):
        products = await get_products(self.url)
        if search:
            products = [product for product in products if product['name'].find(search) == 0]
        if not sort_by_price:
            products = sorted(products, key=itemgetter('price'))
        return products


app = FastAPI()
        
        

@app.get("/")
async def root():
    return {"message": "API desafio IN8, by Tales Monteiro Melquiades."}


@app.get("/products/")
async def products(
    search: str | None = Query(
        default=None,
        description="Search by product name"
        ), 
    sort_by_price: bool = Query(
        default=True,
        description="Sort by price"
        )
    ):
    products = await get_products(menu['phones'])
    if search:
        products = [product for product in products if product['name'].find(search) == 0]
    if not sort_by_price:
        products = sorted(products, key=itemgetter('price'))
    return products

app.include_router(BasicAPI("computers").router)
app.include_router(BasicAPI("laptops").router)
app.include_router(BasicAPI("tablets").router)
app.include_router(BasicAPI("phones").router)
app.include_router(BasicAPI("touch").router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
        port=8000
    )
    