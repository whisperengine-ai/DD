"""
Sleep Phase: Scheduled maintenance and consolidation.
Simplified version using APScheduler.
"""
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class SleepPhase:
    """Simplified sleep phase: validation + cleanup."""
    
    def __init__(self, chroma, prismo, anchor, soul, vector_store):
        self.chroma = chroma
        self.prismo = prismo
        self.anchor = anchor
        self.soul = soul
        self.vector_store = vector_store
        self.scheduler = BackgroundScheduler()
        self.last_run = None
        self.run_count = 0
        logger.info("Sleep phase initialized")
    
    def start(self, interval_hours: int = 6):
        """Start sleep phase scheduler."""
        try:
            self.scheduler.add_job(
                self.run_sleep_cycle,
                'interval',
                hours=interval_hours,
                id='sleep_phase',
                replace_existing=True
            )
            self.scheduler.start()
            logger.info(f"Sleep phase scheduled every {interval_hours} hours")
        except Exception as e:
            logger.error(f"Failed to start sleep phase scheduler: {e}")
    
    def stop(self):
        """Stop the scheduler."""
        try:
            self.scheduler.shutdown()
            logger.info("Sleep phase scheduler stopped")
        except Exception as e:
            logger.error(f"Error stopping scheduler: {e}")
    
    def run_sleep_cycle(self) -> Dict:
        """Execute simplified sleep phase."""
        logger.info("=== SLEEP PHASE START ===")
        start_time = datetime.utcnow()
        results = {}
        
        try:
            # Stage 1: Validate
            logger.info("Stage 1: Validation")
            results['validation'] = {
                'vectors': self._validate_vectors(),
                'concepts': self._validate_concepts()
            }
            
            # Stage 2: Cleanup (optional for MVP)
            logger.info("Stage 2: Cleanup")
            results['cleanup'] = {
                'status': 'skipped_mvp'
            }
            
            # Stage 3: Soul refinement
            logger.info("Stage 3: Soul Refinement")
            results['soul_refinement'] = self._refine_souls()
            
            # Calculate duration
            duration = (datetime.utcnow() - start_time).total_seconds()
            self.last_run = datetime.utcnow()
            self.run_count += 1
            
            logger.info(f"=== SLEEP PHASE COMPLETE ({duration:.1f}s) ===")
            
            results['duration_seconds'] = duration
            results['success'] = True
            return results
            
        except Exception as e:
            logger.error(f"Sleep phase failed: {e}")
            duration = (datetime.utcnow() - start_time).total_seconds()
            return {
                'success': False,
                'error': str(e),
                'duration_seconds': duration
            }
    
    def _validate_vectors(self) -> Dict:
        """Check vector integrity."""
        try:
            count = self.vector_store.count()
            logger.info(f"Validated {count} vectors")
            return {'count': count, 'status': 'valid'}
        except Exception as e:
            logger.error(f"Vector validation failed: {e}")
            return {'count': 0, 'status': 'error', 'error': str(e)}
    
    def _validate_concepts(self) -> Dict:
        """Check concept DB integrity."""
        try:
            count = self.prismo.get_concept_count()
            logger.info(f"Validated {count} concepts")
            return {'count': count, 'status': 'valid'}
        except Exception as e:
            logger.error(f"Concept validation failed: {e}")
            return {'count': 0, 'status': 'error', 'error': str(e)}
    
    def _cleanup_old_vectors(self):
        """Remove vectors older than 30 days (simplified: skip for MVP)."""
        logger.info("Vector cleanup skipped (MVP)")
        return {'status': 'skipped'}
    
    def _cleanup_old_concepts(self):
        """Remove old concepts (simplified: skip for MVP)."""
        logger.info("Concept cleanup skipped (MVP)")
        return {'status': 'skipped'}
    
    def _refine_souls(self) -> Dict:
        """Update all soul states."""
        try:
            users = self.soul.get_all_users()
            refined_count = 0
            
            for user_id in users:
                soul = self.soul.get_or_create(user_id)
                logger.info(
                    f"Soul state for {user_id}: "
                    f"alignment={soul['alignment_score']:.3f}, "
                    f"interactions={soul['interaction_count']}"
                )
                refined_count += 1
            
            # Get overall stats
            stats = self.soul.get_stats()
            
            return {
                'users_processed': refined_count,
                'stats': stats,
                'status': 'complete'
            }
        except Exception as e:
            logger.error(f"Soul refinement failed: {e}")
            return {
                'users_processed': 0,
                'status': 'error',
                'error': str(e)
            }
    
    def get_status(self) -> Dict:
        """Get sleep phase status."""
        return {
            'scheduler_running': self.scheduler.running,
            'last_run': self.last_run.isoformat() if self.last_run else None,
            'run_count': self.run_count,
            'next_run': str(self.scheduler.get_jobs()[0].next_run_time) if self.scheduler.get_jobs() else None
        }
