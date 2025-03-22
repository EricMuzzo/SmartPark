from fastapi import Query, HTTPException
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

operator_map = {
    "eq": "$eq",
    "ne": "$ne",
    "gt": "$gt",
    "gte": "$gte",
    "lt": "$lt",
    "lte": "$lte"
}

def parse_reservations_filter(
    filter: Optional[List[str]] = Query(None, description="Filter expressions of the form {field}:{operator}:{value}")
) -> dict:
    """
    Dependency function that converts the given filter query param(s)
    into a MongoDB filter dictionary.

    Example usage:
        GET /reservations?filter=spot_id:eq:641a840ef5c746b227c0cb63
                          &filter=start_time:gt:2025-03-08T16:30:00
    Returns:
        dict suitable for passing to reservations_collection.find(mongo_filter).
    """

    mongo_filter = {}

    if filter:
        for expr in filter:
            parts = expr.split(":", 2)  # split on first two colons
            if len(parts) != 3:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid filter format: '{expr}' (expected 'field:operator:value')"
                )

            field_name, operator, raw_value = parts

            # Validate operator
            if operator not in operator_map:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported operator '{operator}' in filter '{expr}'"
                )

            # Convert value based on the field_name
            if field_name in ["spot_id", "user_id"]:
                try:
                    value = ObjectId(raw_value)
                except:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid ObjectId for '{field_name}' in filter '{expr}'"
                    )
            elif field_name in ["start_time", "end_time"]:
                try:
                    value = datetime.fromisoformat(raw_value)
                except ValueError:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid datetime string for '{field_name}' in filter '{expr}'"
                    )
            elif field_name == "final_price":
                try:
                    value = float(raw_value)
                except ValueError:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid float string for '{field_name}' in filter '{expr}'"
                    )
            else:
                # By default treat as string
                value = raw_value

            # Build partial filter for this expression
            field_filter = {operator_map[operator]: value}

            # Merge into the mongo_filter.  Basic approach is to AND them:
            # mongo_filter[field_name] = { "$gt": value, ... } etc.
            if field_name not in mongo_filter:
                mongo_filter[field_name] = field_filter
            else:
                # If the same field was repeated, you need to decide how to handle that
                # (e.g. combine with $and or $or, or just override, etc.)
                # For simplicity, we'll just merge them:
                mongo_filter[field_name].update(field_filter)

    return mongo_filter



def parse_spots_filter(
    filter: Optional[List[str]] = Query(None, description="Filter expressions of the form {field}:{operator}:{value}")
) -> dict:
    """
    Dependency function that converts the given filter query param(s)
    into a MongoDB filter dictionary.

    Example usage:
        GET /spots?filter=floor_level:eq:3
                          &filter=status:eq:vacant
    Returns:
        dict suitable for passing to spots_collection.find(mongo_filter).
    """
    mongo_filter = {}

    if filter:
        for expr in filter:
            parts = expr.split(":", 2)  # split on first two colons
            if len(parts) != 3:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid filter format: '{expr}' (expected 'field:operator:value')"
                )

            field_name, operator, raw_value = parts

            # Validate operator
            if operator not in operator_map:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported operator '{operator}' in filter '{expr}'"
                )

            #Validate the filter field names
            if field_name == "status":
                if raw_value not in ["vacant", "occupied", "reserved"]:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid filter value for '{field_name}' in filter '{expr}'. Values accepted are 'vacant', 'occupied', 'reserved'"
                    )
                value = raw_value
            
            elif field_name in ["floor_level", "spot_number"]:
                try:
                    value = int(raw_value)
                except ValueError:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid integer string for '{field_name}' in filter '{expr}'"
                    )
            else:
                # By default treat as string
                value = raw_value

            # Build partial filter for this expression
            field_filter = {operator_map[operator]: value}

            # Merge into the mongo_filter.  Basic approach is to AND them:
            # mongo_filter[field_name] = { "$gt": value, ... } etc.
            if field_name not in mongo_filter:
                mongo_filter[field_name] = field_filter
            else:
                # If the same field was repeated, you need to decide how to handle that
                # (e.g. combine with $and or $or, or just override, etc.)
                # For simplicity, we'll just merge them:
                mongo_filter[field_name].update(field_filter)

    return mongo_filter