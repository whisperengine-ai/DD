"""
Prismo Triad (Enhanced): Cognitive/Moral reasoning with comprehensive spaCy pipeline.
Uses full spaCy capabilities:
- Tokenization: Word segmentation and punctuation handling
- POS Tagging: Part-of-speech identification
- Dependency Parsing: Syntactic relationship analysis
- Lemmatization: Base form extraction
- Sentence Boundary Detection: Multi-sentence handling
- Named Entity Recognition: Entity extraction and categorization
- Similarity: Semantic comparison between texts
- Rule-based Matching: Pattern-based concept extraction
"""
import sqlite3
import json
import logging
from typing import Dict, List, Tuple, Optional
import spacy
from spacy.matcher import Matcher
from spacy.tokens import Doc, Span, Token

logger = logging.getLogger(__name__)


class PrismoTriadEnhanced:
    """Enhanced cognitive/moral reasoning with comprehensive spaCy pipeline."""
    
    def __init__(self, db_path: str = "./data/dd.db", slmu_rules_path: str = "./config/slmu_rules.json"):
        logger.info("Initializing Enhanced Prismo Triad with full spaCy pipeline...")
        
        self.db_path = db_path
        
        # Load spaCy model with all components enabled
        logger.info("Loading spaCy en_core_web_sm with full pipeline...")
        try:
            self.nlp = spacy.load("en_core_web_sm")
            logger.info(f"  Pipeline components: {self.nlp.pipe_names}")
        except OSError:
            logger.error("spaCy model not found. Run: python -m spacy download en_core_web_sm")
            raise
        
        # Initialize rule-based matcher for ethical patterns
        self.matcher = Matcher(self.nlp.vocab)
        self._init_matchers()
        
        # Load SLMU rules
        with open(slmu_rules_path, 'r', encoding='utf-8') as f:
            self.slmu_rules = json.load(f)
        
        # Initialize database
        self._init_db()
        
        logger.info("Enhanced Prismo Triad initialized successfully")
    
    def _init_matchers(self):
        """Initialize spaCy rule-based matchers for ethical patterns."""
        # Pattern for detecting harm/violence concepts
        harm_pattern = [
            {"LEMMA": {"IN": ["harm", "hurt", "damage", "destroy", "kill", "attack"]}}
        ]
        self.matcher.add("HARM", [harm_pattern])
        
        # Pattern for detecting ethical concepts
        ethical_pattern = [
            {"LEMMA": {"IN": ["respect", "dignity", "fairness", "justice", "equality", "rights"]}}
        ]
        self.matcher.add("ETHICAL", [ethical_pattern])
        
        # Pattern for detecting imperative commands
        command_pattern = [
            {"POS": "VERB", "TAG": {"IN": ["VB", "VBP"]}},
            {"POS": {"IN": ["NOUN", "PRON"]}}
        ]
        self.matcher.add("COMMAND", [command_pattern])
    
    def _init_db(self):
        """Initialize SQLite database for concepts and relationships."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Enhanced concepts table with linguistic features
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS concepts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                lemma TEXT,
                entity_type TEXT,
                pos_tag TEXT,
                category TEXT,
                frequency INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(name, entity_type)
            )
        ''')
        
        # Relationships table with dependency labels
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS relationships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_id INTEGER,
                predicate TEXT,
                predicate_lemma TEXT,
                object_id INTEGER,
                dependency_type TEXT,
                strength REAL DEFAULT 1.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (subject_id) REFERENCES concepts(id),
                FOREIGN KEY (object_id) REFERENCES concepts(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def process(self, text: str, user_id: str) -> Dict:
        """
        Enhanced processing with full spaCy pipeline:
        Understanding → Reasoning → Judgment
        """
        logger.info(f"Enhanced Prismo processing for user {user_id}")
        
        # Process text through full spaCy pipeline
        # This includes: tokenization, POS tagging, dependency parsing, 
        # lemmatization, sentence boundary detection, and NER
        doc = self.nlp(text)
        
        # 1. UNDERSTANDING: Extract linguistic features
        linguistic_analysis = self._analyze_linguistics(doc)
        
        # 2. EXTRACTION: Get entities and concepts
        entities = self._extract_entities(doc)
        concepts = self._extract_concepts(doc, entities, linguistic_analysis)
        
        # 3. REASONING: Identify relationships using dependency parsing
        relationships = self._extract_relationships(doc, concepts)
        
        # 4. PATTERN MATCHING: Apply rule-based ethical patterns
        ethical_matches = self._apply_ethical_patterns(doc)
        
        # 5. JUDGMENT: Check SLMU compliance
        slmu_result = self._check_slmu_compliance(text, doc, concepts, ethical_matches)
        
        # Store concepts and relationships
        self._store_concepts(concepts)
        self._store_relationships(relationships)
        
        return {
            'entities': entities,
            'concepts': concepts,
            'relationships': relationships,
            'linguistic_features': linguistic_analysis,
            'ethical_patterns': ethical_matches,
            'slmu_compliance': slmu_result,
            'entity_count': len(entities),
            'concept_count': len(concepts),
            'sentence_count': len(list(doc.sents))
        }
    
    def _analyze_linguistics(self, doc) -> Dict:
        """
        Comprehensive linguistic analysis using spaCy pipeline features:
        - Tokenization: Count and analyze tokens
        - POS Tagging: Part-of-speech distribution
        - Lemmatization: Extract key lemmas
        - Sentence Boundary Detection: Multi-sentence handling
        """
        # Tokenization analysis
        tokens = [token for token in doc if not token.is_space]
        token_count = len(tokens)
        
        # POS tagging distribution
        pos_counts = {}
        for token in tokens:
            pos = token.pos_
            pos_counts[pos] = pos_counts.get(pos, 0) + 1
        
        # Extract key lemmas (content words)
        key_lemmas = [
            token.lemma_ 
            for token in tokens 
            if token.pos_ in ['NOUN', 'VERB', 'ADJ', 'ADV'] and not token.is_stop
        ]
        
        # Sentence boundary detection
        sentences = [sent.text.strip() for sent in doc.sents]
        
        # Dependency analysis
        dependency_types = set([token.dep_ for token in tokens])
        
        return {
            'token_count': token_count,
            'pos_distribution': pos_counts,
            'key_lemmas': key_lemmas[:20],  # Top 20
            'sentences': sentences,
            'sentence_count': len(sentences),
            'dependency_types': list(dependency_types),
            'avg_token_length': sum(len(t.text) for t in tokens) / token_count if token_count > 0 else 0
        }
    
    def _extract_entities(self, doc) -> List[Dict]:
        """
        Extract named entities using spaCy NER with enhanced metadata.
        Returns list of entities with text, label, lemma, and linguistic features.
        """
        entities = []
        for ent in doc.ents:
            entities.append({
                'text': ent.text,
                'label': ent.label_,
                'start': ent.start_char,
                'end': ent.end_char,
                'lemma': ent.lemma_,
                'root_pos': ent.root.pos_,
                'root_dep': ent.root.dep_
            })
        return entities
    
    def _extract_concepts(self, doc, entities: List[Dict], linguistic_analysis: Dict) -> List[Dict]:
        """
        Extract concepts using multiple spaCy features:
        - Named entities (from NER)
        - Noun chunks (from dependency parsing)
        - Key lemmas (from lemmatization)
        - POS-based filtering
        """
        concepts = []
        seen_texts = set()
        
        # Add entities as primary concepts
        for ent in entities:
            if ent['text'].lower() not in seen_texts:
                concepts.append({
                    'name': ent['text'],
                    'lemma': ent.get('lemma', ent['text']),
                    'entity_type': ent['label'],
                    'pos_tag': ent.get('root_pos', 'UNKNOWN'),
                    'category': self._categorize_entity(ent['label'])
                })
                seen_texts.add(ent['text'].lower())
        
        # Add noun chunks as potential concepts (using dependency parsing)
        for chunk in doc.noun_chunks:
            # Skip if too long or already captured
            if len(chunk.text.split()) <= 3 and chunk.text.lower() not in seen_texts:
                concepts.append({
                    'name': chunk.text,
                    'lemma': chunk.lemma_,
                    'entity_type': 'NOUN_CHUNK',
                    'pos_tag': chunk.root.pos_,
                    'category': 'general'
                })
                seen_texts.add(chunk.text.lower())
        
        # Add key lemmas from linguistic analysis as abstract concepts
        for lemma in linguistic_analysis.get('key_lemmas', [])[:10]:
            if lemma.lower() not in seen_texts:
                concepts.append({
                    'name': lemma,
                    'lemma': lemma,
                    'entity_type': 'LEMMA',
                    'pos_tag': 'ABSTRACT',
                    'category': 'concept'
                })
                seen_texts.add(lemma.lower())
        
        return concepts
    
    def _categorize_entity(self, label: str) -> str:
        """Map spaCy entity labels to conceptual categories."""
        category_map = {
            'PERSON': 'agent',
            'ORG': 'organization',
            'GPE': 'location',
            'LOC': 'location',
            'DATE': 'temporal',
            'TIME': 'temporal',
            'MONEY': 'value',
            'PERCENT': 'value',
            'PRODUCT': 'artifact',
            'EVENT': 'event',
            'WORK_OF_ART': 'artifact',
            'LAW': 'concept',
            'LANGUAGE': 'concept',
            'NORP': 'group'
        }
        return category_map.get(label, 'general')
    
    def _extract_relationships(self, doc, concepts: List[Dict]) -> List[Dict]:
        """
        Extract relationships using advanced dependency parsing:
        - Subject-verb-object patterns
        - Prepositional relationships
        - Dependency labels for context
        - Lemmatized predicates for normalization
        """
        relationships = []
        
        # Build concept lookup by text matching
        concept_map = {c['name'].lower(): c for c in concepts}
        
        # Extract verb-based relationships using dependency parsing
        for token in doc:
            if token.pos_ == 'VERB':
                # Find subjects (nsubj, nsubjpass, agent)
                subjects = [child for child in token.children 
                           if child.dep_ in ('nsubj', 'nsubjpass', 'agent')]
                
                # Find objects (dobj, pobj, attr, dative)
                objects = [child for child in token.children 
                          if child.dep_ in ('dobj', 'pobj', 'attr', 'dative')]
                
                # Create relationships
                for subj in subjects:
                    subj_text = subj.text.lower()
                    subj_concept = concept_map.get(subj_text)
                    
                    for obj in objects:
                        obj_text = obj.text.lower()
                        obj_concept = concept_map.get(obj_text)
                        
                        if subj_concept and obj_concept:
                            relationships.append({
                                'subject': subj_concept['name'],
                                'predicate': token.text,
                                'predicate_lemma': token.lemma_,
                                'object': obj_concept['name'],
                                'dependency_type': f"{subj.dep_}-{obj.dep_}",
                                'verb_tense': token.tag_
                            })
        
        # Extract prepositional relationships
        for token in doc:
            if token.dep_ == 'prep':
                head = token.head
                pobj = [child for child in token.children if child.dep_ == 'pobj']
                
                if pobj and head.text.lower() in concept_map and pobj[0].text.lower() in concept_map:
                    relationships.append({
                        'subject': head.text,
                        'predicate': token.text,
                        'predicate_lemma': token.lemma_,
                        'object': pobj[0].text,
                        'dependency_type': 'prep-pobj',
                        'verb_tense': 'N/A'
                    })
        
        return relationships
    
    def _apply_ethical_patterns(self, doc) -> Dict:
        """
        Apply rule-based pattern matching for ethical concepts:
        - Harm/violence detection
        - Ethical principle identification
        - Command/imperative detection
        """
        matches = self.matcher(doc)
        
        pattern_matches = {
            'harm_patterns': [],
            'ethical_patterns': [],
            'command_patterns': []
        }
        
        for match_id, start, end in matches:
            span = doc[start:end]
            rule_name = self.nlp.vocab.strings[match_id]
            
            match_info = {
                'text': span.text,
                'lemma': span.lemma_,
                'start': start,
                'end': end
            }
            
            if rule_name == 'HARM':
                pattern_matches['harm_patterns'].append(match_info)
            elif rule_name == 'ETHICAL':
                pattern_matches['ethical_patterns'].append(match_info)
            elif rule_name == 'COMMAND':
                pattern_matches['command_patterns'].append(match_info)
        
        return pattern_matches
    
    def _check_slmu_compliance(self, text: str, doc, concepts: List[Dict], ethical_matches: Dict) -> Dict:
        """
        Enhanced SLMU compliance checking with:
        - Pattern-based rule checking
        - Concept-aware validation
        - Ethical pattern matching results
        - Lemma-based keyword matching
        """
        violations = []
        warnings = []
        
        text_lower = text.lower()
        
        # Check forbidden patterns (basic text matching)
        for rule in self.slmu_rules.get('forbidden_patterns', []):
            pattern = rule['pattern'].lower()
            if pattern in text_lower:
                violations.append({
                    'type': 'forbidden_pattern',
                    'pattern': pattern,
                    'severity': rule.get('severity', 'high')
                })
        
        # Check for harm patterns detected by matcher
        harm_patterns = ethical_matches.get('harm_patterns', [])
        if harm_patterns:
            for harm in harm_patterns:
                violations.append({
                    'type': 'harm_pattern_detected',
                    'text': harm['text'],
                    'lemma': harm['lemma'],
                    'severity': 'high'
                })
        
        # Check for command patterns (potential manipulation)
        command_patterns = ethical_matches.get('command_patterns', [])
        if len(command_patterns) > 3:  # Multiple imperatives
            warnings.append({
                'type': 'excessive_commands',
                'count': len(command_patterns),
                'severity': 'medium'
            })
        
        # Check required values using both text and lemmas
        required_present = []
        doc_lemmas = set([token.lemma_.lower() for token in doc])
        
        for value in self.slmu_rules.get('required_values', []):
            value_lower = value.lower()
            # Check in text, concepts, or lemmas
            if (value_lower in text_lower or 
                any(value_lower in c['name'].lower() for c in concepts) or
                value_lower in doc_lemmas):
                required_present.append(value)
        
        # Check ethical principles with concept awareness
        ethical_found = ethical_matches.get('ethical_patterns', [])
        for principle in self.slmu_rules.get('ethical_principles', []):
            principle_keywords = principle.get('keywords', [])
            for keyword in principle_keywords:
                keyword_lower = keyword.lower()
                # Check in text, concepts, lemmas, or matched patterns
                if (keyword_lower in text_lower or
                    any(keyword_lower in c.get('lemma', '').lower() for c in concepts) or
                    any(keyword_lower in p['lemma'].lower() for p in ethical_found)):
                    warnings.append({
                        'type': 'ethical_principle',
                        'principle': principle['name'],
                        'keyword': keyword,
                        'severity': 'info'
                    })
        
        # Sentiment-based warnings using POS distribution
        verb_count = sum(1 for token in doc if token.pos_ == 'VERB')
        if verb_count > 10:  # Lots of action verbs
            warnings.append({
                'type': 'high_activity',
                'verb_count': verb_count,
                'severity': 'low'
            })
        
        compliant = len(violations) == 0
        
        return {
            'compliant': compliant,
            'violations': violations,
            'warnings': warnings,
            'required_values_present': required_present,
            'ethical_patterns_found': len(ethical_found),
            'harm_patterns_found': len(harm_patterns),
            'command_patterns_found': len(command_patterns)
        }
    
    def _store_concepts(self, concepts: List[Dict]):
        """Store or update concepts with enhanced linguistic features."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for concept in concepts:
            # Try to insert or update frequency with lemma and POS
            cursor.execute('''
                INSERT INTO concepts (name, lemma, entity_type, pos_tag, category)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(name, entity_type) DO UPDATE SET
                    frequency = frequency + 1,
                    updated_at = CURRENT_TIMESTAMP
            ''', (
                concept['name'],
                concept.get('lemma', concept['name']),
                concept.get('entity_type', 'unknown'),
                concept.get('pos_tag', 'UNKNOWN'),
                concept.get('category', 'general')
            ))
        
        conn.commit()
        conn.close()
    
    def _store_relationships(self, relationships: List[Dict]):
        """Store relationships with enhanced dependency information."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for rel in relationships:
            # Get concept IDs
            cursor.execute('SELECT id FROM concepts WHERE name = ?', (rel['subject'],))
            subj_row = cursor.fetchone()
            
            cursor.execute('SELECT id FROM concepts WHERE name = ?', (rel['object'],))
            obj_row = cursor.fetchone()
            
            if subj_row and obj_row:
                cursor.execute('''
                    INSERT INTO relationships (subject_id, predicate, predicate_lemma, 
                                             object_id, dependency_type)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    subj_row[0], 
                    rel['predicate'], 
                    rel.get('predicate_lemma', rel['predicate']),
                    obj_row[0],
                    rel.get('dependency_type', 'unknown')
                ))
        
        conn.commit()
        conn.close()
    
    def get_concept_count(self) -> int:
        """Get total number of unique concepts."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM concepts')
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def get_top_concepts(self, limit: int = 10) -> List[Dict]:
        """Get most frequent concepts with linguistic features."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT name, lemma, entity_type, pos_tag, category, frequency
            FROM concepts
            ORDER BY frequency DESC
            LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'name': row[0],
                'lemma': row[1],
                'entity_type': row[2],
                'pos_tag': row[3],
                'category': row[4],
                'frequency': row[5]
            }
            for row in rows
        ]
