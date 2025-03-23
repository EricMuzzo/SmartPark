from fastapi import APIRouter, HTTPException, status, Depends, Response
from ..models.user import User, UserCreate, UserUpdate, UserFilterParams
from ..models.generic import ListResponse
from ..crud import users as user_crud


user_not_found_response = {
    404: {
        "description": "User with the given id not found",
        "content": {
            "application/json": {
                "example": {
                    "message": "User with id 67ccb6d6825b86fb6abcae70 not found"
                }
            }
        }
    }
}

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get(
    path="",
    summary="Get all users",
    description="Fetch a list of all users",
    response_model=ListResponse[User]
)
async def getUsers(filter_params: UserFilterParams = Depends()) -> ListResponse[User]:
    filter_dict = filter_params.model_dump(exclude_unset=True, exclude_none=True)
    users = await user_crud.fetch_all_users(filter_dict)
    return ListResponse(records=users)


@router.get("/{id}", summary="Get user", description="Fetch a user by their Mongo id", response_model=User, responses=user_not_found_response)
async def getUser(id: str):
    user = await user_crud.fetch_user(id)
    if user:
        return user
    raise HTTPException(status_code=404, detail=f"User with id {id} not found")


# @router.post("", summary="Create user", description="Manually create a user", response_model=User, status_code=status.HTTP_201_CREATED)
# async def createUser(user: UserCreate) -> User:
#     new_user = await user_crud.create_user(user.model_dump(by_alias=True, exclude=["id"]))
#     return new_user


@router.put("/{id}", summary="Update user", description="Update a user by ID", response_model=User, responses=user_not_found_response)
async def updateUser(id: str, user_data: UserUpdate):
    """Update a user by ID"""
    
    update_payload = user_data.model_dump(by_alias=True, exclude_none=True)
    
    updated_user = await user_crud.update_user(id, update_payload)
    if updated_user is not None:
        return updated_user
    raise HTTPException(status_code=404, detail=f"User with {id} not found")

@router.delete("/{id}", summary="Delete user", description="Delete a user by Mongo ID", status_code=status.HTTP_204_NO_CONTENT, responses=user_not_found_response)
async def deleteUser(id: str):
    result = await user_crud.remove_user(id)
    if result:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"User with id {id} not found")