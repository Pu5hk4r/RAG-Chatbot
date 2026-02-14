from fastapi import APIRouter
from app.db import collections_db
from app.schema import CollectionInfo

router = APIRouter(prefix="/api", tags=["users"])


@router.get("/collections")
async def list_collections():
    collections = []

    for cid, data in collections_db.items():
        collections.append(
            CollectionInfo(
                id=cid,
                name=data["name"],
                document_count=len(data["files"]),
                indexed=data["indexed"]
            )
        )

    return {"collections": collections}
