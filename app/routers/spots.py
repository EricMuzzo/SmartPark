from fastapi import APIRouter, HTTPException, Depends, status, Response
from ..models.spot import ParkingSpot, ParkingSpotBase, ParkingSpotCollection, ParkingSpotUpdate
from ..models.generic import ListResponse
from ..crud import spots as spots_crud
from ..utils.filtering import parse_spots_filter


spot_not_found_response = {
    404: {
        "description": "Parking spot with the given id not found",
        "content": {
            "application/json": {
                "example": {
                    "message": "Parking spot with id 67ccb6d6825b86fb6abcae70 not found"
                }
            }
        }
    }
}


router = APIRouter(
    prefix="/spots",
    tags=["Spots"]
)


@router.get(
    path="",
    summary="Get all parking spots",
    description="Fetch a list of all parking spots",
    response_model=ListResponse[ParkingSpot]
)
async def getSpots(filters: dict = Depends(parse_spots_filter)) -> ListResponse[ParkingSpot]:
    spots = await spots_crud.fetch_all_spots(filters)
    return ListResponse(records=spots)


@router.get(
    path="/{id}",
    summary="Get parking spot",
    description="Fetch a parking spot by its Mongo id",
    response_model=ParkingSpot,
    responses=spot_not_found_response
)
async def getSpot(id: str) -> ParkingSpot:
    spot = await spots_crud.fetch_spot(id)
    if spot:
        return spot
    raise HTTPException(status_code=404, detail=f"Parking spot with id {id} not found")


@router.post(
    path="",
    summary="Create parking spot",
    description="Create a parking spot record in the database",
    response_model=ParkingSpot,
    responses={404: {"detail": "Conflict with existing parking spot"}}
)
async def createSpot(reservation: ParkingSpotBase) -> ParkingSpot:
    created_spot = await spots_crud.create_spot(reservation.model_dump(by_alias=True, exclude=["id"]))
    return created_spot


@router.put(
    path="/{id}",
    summary="Update parking spot",
    description="Update a parking spot by ID",
    response_model=ParkingSpot,
    responses=spot_not_found_response
)
async def updateSpot(id: str, spot_data: ParkingSpotUpdate) -> ParkingSpot:
    
    update_payload = spot_data.model_dump(by_alias=True, exclude_none=True)
    updated_spot = await spots_crud.update_spot(id, update_payload)
    if updated_spot is not None:
        return updated_spot
    raise HTTPException(status_code=404, detail=f"Parking spot with {id} not found")


@router.delete(
    path="/{id}",
    summary="Delete parking spot",
    description="Delete a parking spot by its mongo id",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=spot_not_found_response
)
async def deleteSpot(id: str):
    result = await spots_crud.remove_spot(id)
    if result:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Parking spot with id {id} not found")