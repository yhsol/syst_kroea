from fastapi import APIRouter, Depends, HTTPException
from app.services.position_service import PositionService
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/reduce-all")
async def reduce_all_positions(
    position_service: PositionService = Depends(PositionService)
):
    """모든 해외 주식 포지션을 절반으로 줄입니다."""
    try:
        result = position_service.reduce_all_positions_by_half()
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["message"])
        return result
    except Exception as e:
        logger.error(f"Error in reduce_all_positions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 