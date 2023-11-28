from fastapi import APIRouter, Response
from models.model1 import Model

router = APIRouter()

@router.post("/add")
async def login(response: Response, model: Model):
    pass