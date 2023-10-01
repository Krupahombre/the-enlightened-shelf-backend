from fastapi import APIRouter, Query
from starlette import status

router = APIRouter(
    prefix="/test",
    tags=["Test"]
)


@router.get("/", status_code=status.HTTP_200_OK)
async def test_function(name: str, age: int = Query(gt=0)):
    user_name = name
    user_age = age

    return {"Name": user_name, "Age": user_age}
