"""
Pre-download ML models for Docker container build.
This ensures models are cached in the container image.
"""
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_models():
    """Download all required ML models."""
    
    # 1. Download Cardiff Twitter RoBERTa emotion model (28 emotions)
    logger.info("Downloading Cardiff Twitter RoBERTa emotion model (28 emotions)...")
    try:
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        
        model_name = "cardiffnlp/twitter-roberta-base-emotion-multilabel-latest"
        logger.info(f"  - Tokenizer: {model_name}")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        logger.info(f"  - Model: {model_name}")
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        
        logger.info("  ✓ Cardiff RoBERTa emotion model downloaded successfully")
    except Exception as e:
        logger.error(f"  ✗ Failed to download RoBERTa: {e}")
        return False
    
    # 2. Download sentence-transformers model
    logger.info("Downloading sentence-transformers model...")
    try:
        from sentence_transformers import SentenceTransformer
        
        model_name = "all-MiniLM-L6-v2"
        logger.info(f"  - Model: {model_name}")
        embedder = SentenceTransformer(model_name)
        
        logger.info("  ✓ sentence-transformers downloaded successfully")
    except Exception as e:
        logger.error(f"  ✗ Failed to download sentence-transformers: {e}")
        return False
    
    # 3. Verify spaCy model (should be downloaded separately via `python -m spacy download`)
    logger.info("Verifying spaCy model...")
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        logger.info("  ✓ spaCy model verified")
    except OSError:
        logger.error("  ✗ spaCy model not found - run: python -m spacy download en_core_web_sm")
        return False
    except Exception as e:
        logger.error(f"  ✗ Failed to verify spaCy: {e}")
        return False
    
    logger.info("="*60)
    logger.info("All models downloaded and verified successfully!")
    logger.info("="*60)
    return True

if __name__ == "__main__":
    success = download_models()
    sys.exit(0 if success else 1)
