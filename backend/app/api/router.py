from fastapi import APIRouter

from app.api.routes import attempts, health, hierarchy, practice_tests, recommendations

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(hierarchy.router, tags=["hierarchy"])
api_router.include_router(practice_tests.router, prefix="/practice-tests", tags=["practice-tests"])
api_router.include_router(attempts.router, prefix="/test-attempts", tags=["test-attempts"])
api_router.include_router(recommendations.router, prefix="/users", tags=["recommendations"])
