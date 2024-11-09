from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.services.position_service import PositionService
import logging

logger = logging.getLogger(__name__)

def setup_scheduler():
    scheduler = BackgroundScheduler()
    position_service = PositionService()

    def reduce_positions_job():
        try:
            logger.info("Starting daily position reduction job")
            result = position_service.reduce_all_positions_by_half()
            logger.info(f"Position reduction job completed: {result}")
        except Exception as e:
            logger.error(f"Error in position reduction job: {str(e)}")

    # 매일 새벽 4시에 실행
    scheduler.add_job(
        reduce_positions_job,
        trigger=CronTrigger(hour=4, minute=0),
        id='reduce_positions',
        name='Reduce all positions by half',
        replace_existing=True
    )

    scheduler.start()
    return scheduler 