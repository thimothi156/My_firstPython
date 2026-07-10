from fastapi import FastAPI
from routers import user, user_profile, product, category,authenticate


app = FastAPI()

app.include_router(user.router)
app.include_router(authenticate.router)
app.include_router(user_profile.router)
app.include_router(product.router)
app.include_router(category.router)