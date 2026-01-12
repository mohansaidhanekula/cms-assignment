import asyncio
import logging
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Lesson, PublishingLog
from app.config import settings
from app.database import SessionLocal

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Database setup
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def publish_scheduled_lessons():
    """Scheduled task that runs every 60 seconds to publish scheduled lessons"""
    db = SessionLocal()
    try:
        now = datetime.utcnow()
        
        # Find lessons that should be published
        lessons_to_publish = db.query(Lesson).filter(
            Lesson.status == "scheduled",
            Lesson.scheduled_publish_time <= now
        ).all()
        
        for lesson in lessons_to_publish:
            try:
                lesson.status = "published"
                lesson.published_at = now
                
                # Log the publishing action
                log_entry = PublishingLog(
                    lesson_id=lesson.id,
                    action="published",
                    timestamp=now,
                    status="success",
                    details=f"Lesson auto-published at {now}"
                )
                db.add(log_entry)
                db.commit()
                logger.info(f"Published lesson {lesson.id}")
            except Exception as e:
                db.rollback()
                logger.error(f"Failed to publish lesson {lesson.id}: {str(e)}")
                log_entry = PublishingLog(
                    lesson_id=lesson.id,
                    action="publish",
                    timestamp=now,
                    status="failed",
                    details=f"Error: {str(e)}"
                )
                db.add(log_entry)
                db.commit()
    except Exception as e:
        logger.error(f"Worker error: {str(e)}")
    finally:
        db.close()

async def worker_loop():
    """Main worker loop that runs every 60 seconds"""
    logger.info("Worker started")
    while True:
        try:
            await publish_scheduled_lessons()
            logger.debug(f"Worker iteration at {datetime.utcnow()}")
        except Exception as e:
            logger.error(f"Worker exception: {str(e)}")
        
        # Wait 60 seconds before next iteration
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(worker_loop())
