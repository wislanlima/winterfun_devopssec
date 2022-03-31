from fastapi import FastAPI

from app.auth.auth_routes import auth
from app.users.users_routes import users, create_users_table

from fastapi.middleware.cors import CORSMiddleware

import os

description = """
NCIRL_PGDCLOUD_DEVSECOPS. 🚀

## Part of the tutorial on Monitoring

You will be able to:
* **Create a user table**.
* **Create users**.
* **Login**.
* **etc.**.
"""

app = FastAPI(title="NCIRL_PGDCLOUD_DEVSECOPS_2022",description=description,version="SEMESTER2.2022",)

create_users_table()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth)
app.include_router(users)


@app.get("/")
async def root():
    return {"message": "This is a test for the load balancing using the new Amazon account  - Server is Up. Go to <ip_address>/docs to explore the API**"}
