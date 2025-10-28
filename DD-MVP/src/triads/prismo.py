"""
Prismo Triad: Cognitive/Moral reasoning.
Simplified version with concept extraction and SLMU compliance checking.
"""
from typing import Dict, List
import sqlite3
import logging
import re

logger = logging.getLogger(__name__)


class PrismoTriad:
    """Simplified cognitive/moral reasoning."""
    
    def __init__(self, db_path: str, slmu_rules: Dict):
        self.db = sqlite3.connect(db_path, check_same_thread=False)
        self.slmu_rules = slmu_rules
        self._init_db()
        logger.info(f"Prismo initialized with database: {db_path}")
    
    def _init_db(self):
        """Create simple concept table."""
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS concepts (
                id TEXT PRIMARY KEY,
                name TEXT,
                category TEXT,
                slmu_compliant INTEGER,
                user_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS concept_relations (
                from_concept TEXT,
                to_concept TEXT,
                relation_type TEXT,
                weight REAL,
                FOREIGN KEY(from_concept) REFERENCES concepts(id),
                FOREIGN KEY(to_concept) REFERENCES concepts(id)
            )
        """)
        self.db.commit()
    
    def process(self, text: str, user_id: str) -> Dict:
        """
        Simplified: Interpretation → Judgment → Synthesis.
        """
        logger.info(f"Prismo processing for user {user_id}")
        
        # 1. Interpretation: Extract key concepts
        concepts = self._extract_concepts(text)
        
        # 2. Judgment: Check SLMU compliance
        compliant_concepts = []
        non_compliant = []
        
        for concept in concepts:
            is_compliant, reason = self._check_slmu_compliance(concept)
            if is_compliant:
                compliant_concepts.append(concept)
                self._store_concept(concept, user_id)
            else:
                non_compliant.append((concept, reason))
        
        # 3. Synthesis: Generate simple response
        if len(compliant_concepts) == 0:
            return {
                'compliant': False,
                'reason': 'No compliant concepts found',
                'non_compliant': non_compliant,
                'concepts': []
            }
        
        # Find related concepts
        related = []
        if compliant_concepts:
            related = self._find_related(compliant_concepts[0])
        
        return {
            'compliant': True,
            'concepts': compliant_concepts,
            'related': related,
            'concept_count': len(compliant_concepts)
        }
    
    def _extract_concepts(self, text: str) -> List[str]:
        """
        Simple concept extraction.
        For MVP: Capitalized words + important words.
        """
        # Extract capitalized words (potential proper nouns/concepts)
        words = re.findall(r'\b[A-Z][a-z]+\b', text)
        
        # Also extract important lowercase concepts
        important_words = [
            'wisdom', 'knowledge', 'love', 'compassion', 'justice',
            'truth', 'virtue', 'faith', 'hope', 'charity', 'temperance',
            'prudence', 'fortitude', 'courage', 'patience', 'kindness'
        ]
        
        for word in important_words:
            if word in text.lower():
                words.append(word.capitalize())
        
        # Remove duplicates and limit
        unique_concepts = list(set(words))
        return unique_concepts[:10]  # Limit to 10 concepts
    
    def _check_slmu_compliance(self, concept: str) -> tuple[bool, str]:
        """Check against SLMU rule set."""
        prohibited = self.slmu_rules.get('prohibited_concepts', [])
        concept_lower = concept.lower()
        
        for prohibited_concept in prohibited:
            if prohibited_concept.lower() in concept_lower:
                return False, f"Contains prohibited concept: {prohibited_concept}"
        
        return True, "Compliant"
    
    def _store_concept(self, concept: str, user_id: str):
        """Store concept in SQLite."""
        try:
            concept_id = f"{user_id}_{concept.lower()}"
            self.db.execute(
                """INSERT OR REPLACE INTO concepts 
                   (id, name, category, slmu_compliant, user_id) 
                   VALUES (?, ?, ?, ?, ?)""",
                (concept_id, concept, "general", 1, user_id)
            )
            self.db.commit()
        except Exception as e:
            logger.error(f"Error storing concept: {e}")
    
    def _find_related(self, concept: str) -> List[str]:
        """Find related concepts in DB."""
        try:
            cursor = self.db.execute(
                "SELECT name FROM concepts WHERE name LIKE ? LIMIT 5",
                (f"%{concept[:3]}%",)
            )
            return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error finding related concepts: {e}")
            return []
    
    def get_concept_count(self) -> int:
        """Get total number of concepts."""
        cursor = self.db.execute("SELECT COUNT(*) FROM concepts")
        return cursor.fetchone()[0]
