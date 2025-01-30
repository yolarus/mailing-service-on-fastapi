from fastapi import FastAPI

from mailings.mailings.routes import router as router_mailings

app = FastAPI()


@app.get("/")
def home_page():
    """
    Маршрут для домашней страницы
    """
    return {"message": "Домашняя страница"}


app.include_router(router_mailings)
