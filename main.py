from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from works.dynamic_conf import main as dynamic_conf_main
from works.dynamic_opt import opt

app = FastAPI()

origins = [ 
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root(
    first: int, second: int, third: int, fourth: int, fifth: int, sixth: int
):
    if (
        (first != None)
        and (second != None)
        and (third != None)
        and (fourth != None)
        and (fifth != None)
        and (sixth != None)
    ):
        array = [first, second, third, fourth, fifth, sixth]
        data = opt(array)
        return {"message": data}
