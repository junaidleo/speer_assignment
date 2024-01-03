from fastapi import APIRouter

from routes import notes, auth, share

api_router = APIRouter()

api_router.include_router(notes.router, prefix="/notes", tags=["notes"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(share.router, prefix="/search", tags=["search"])
