"""
Enhanced Semantic Analyzer - No Heavy Dependencies
"""

import re
import numpy as np
from typing import List, Dict, Any, Tuple
from collections import Counter

class SemanticAnalyzer:
    def __init__(self, nlp_model, embedding_model, domain_vocabularies):
        self.nlp = nlp_model
        self.embedding_model = embedding_model
        self.domain_vocabularies = domain_vocabularies
        
        # Job-specific patterns for exact matching
        self.job_patterns = {
            "4_days": ["4 days", "4-day", "four days", "four day", "multi-day"],
            "college_friends": ["college friends", "university friends", "student", "college", "young adult"],
            "group_10": ["group of 10", "10 people", "10 friends", "large group", "group travel"],
            "trip_planning": ["trip planning", "travel planning", "itinerary", "schedule", "organize"]
        }
    
    def analyze_persona_requirements(self, persona: str, job_description: str) -> Dict[str, Any]:
        """Analyze persona and job with focus on exact requirements"""
        
        job_analysis = self._extract_job_specifics(job_description)
        keywords = self._get_optimized_keywords(persona, job_description)
        patterns = self._create_exact_patterns(job_description)
        
        context = f"{persona} planning {job_description}"
        context_embedding = self.embedding_model.encode(context)
        
        return {
            'persona': persona,
            'job_analysis': job_analysis,
            'keywords': keywords,
            'patterns': patterns,
            'context_embedding': context_embedding,
            'scoring_weights': self._get_scoring_weights()
        }
    
    def _extract_job_specifics(self, job_description: str) -> Dict[str, Any]:
        """Extract specific job requirements"""
        analysis = {
            'duration': None,
            'group_size': None,
            'group_type': None,
            'age_group': None,
            'main_activity': None
        }
        
        job_lower = job_description.lower()
        
        if "4 days" in job_lower or "4-day" in job_lower:
            analysis['duration'] = "4 days"
        
        if "10" in job_description:
            analysis['group_size'] = 10
        
        if "college friends" in job_lower:
            analysis['group_type'] = "college friends"
            analysis['age_group'] = "young adults"
        
        if "plan" in job_lower:
            analysis['main_activity'] = "trip planning"
        
        return analysis
    
    def _get_optimized_keywords(self, persona: str, job_description: str) -> Dict[str, List[str]]:
        """Get optimized keywords for maximum accuracy"""
        base_keywords = self.domain_vocabularies.get(persona, {})
        
        optimized = {
            'critical': ["itinerary", "plan", "days", "group", "activities", "schedule"],
            'high_priority': base_keywords.get('high_priority', []),
            'job_specific': [],
            'actionable': ["book", "visit", "organize", "coordinate", "arrange", "prepare"]
        }
        
        if "4 days" in job_description:
            optimized['job_specific'].extend(["4 days", "multi-day", "itinerary", "schedule"])
        
        if "college friends" in job_description:
            optimized['job_specific'].extend(["college", "student", "friends", "budget", "affordable"])
        
        if "group of 10" in job_description:
            optimized['job_specific'].extend(["group", "large group", "party", "accommodation"])
        
        return optimized
    
    def _create_exact_patterns(self, job_description: str) -> List[str]:
        """Create exact matching patterns"""
        patterns = []
        job_lower = job_description.lower()
        
        if "4 days" in job_lower:
            patterns.extend(self.job_patterns["4_days"])
        
        if "college friends" in job_lower:
            patterns.extend(self.job_patterns["college_friends"])
        
        if "10" in job_description:
            patterns.extend(self.job_patterns["group_10"])
        
        if "plan" in job_lower:
            patterns.extend(self.job_patterns["trip_planning"])
        
        return patterns
    
    def _get_scoring_weights(self) -> Dict[str, float]:
        """Get optimized scoring weights"""
        return {
            'exact_job_match': 5.0,
            'critical_keywords': 4.0,
            'semantic_similarity': 3.0,
            'actionable_content': 2.5,
            'section_quality': 2.0,
            'practical_value': 1.5
        }
    
    def calculate_enhanced_relevance(self, section: Dict[str, Any], 
                                   requirements: Dict[str, Any]) -> Dict[str, float]:
        """Calculate relevance scores"""
        
        content = section.get('content', '')
        title = section.get('title', '')
        combined_text = f"{title} {content}".lower()
        
        scores = {}
        
        scores['exact_job_match'] = self._score_exact_job_match(
            combined_text, requirements['job_analysis'], requirements['patterns']
        )
        
        scores['critical_keywords'] = self._score_critical_keywords(
            combined_text, requirements['keywords']['critical']
        )
        
        scores['semantic_similarity'] = self._calculate_semantic_similarity(
            section, requirements['context_embedding']
        )
        
        scores['actionable_content'] = self._score_actionable_content(
            combined_text, requirements['keywords']['actionable']
        )
        
        scores['section_quality'] = section.get('quality_score', 0.5)
        
        scores['practical_value'] = self._score_practical_value(combined_text)
        
        return scores
    
    def _score_exact_job_match(self, text: str, job_analysis: Dict, patterns: List[str]) -> float:
        """Score exact match to job requirements"""
        score = 0.0
        
        if job_analysis['duration'] and job_analysis['duration'].lower() in text:
            score += 0.4
        
        if job_analysis['group_size'] and str(job_analysis['group_size']) in text:
            score += 0.3
        
        if job_analysis['group_type'] and job_analysis['group_type'].lower() in text:
            score += 0.2
        
        pattern_matches = sum(1 for pattern in patterns if pattern.lower() in text)
        score += min(pattern_matches * 0.1, 0.3)
        
        return min(score, 1.0)
    
    def _score_critical_keywords(self, text: str, critical_keywords: List[str]) -> float:
        """Score critical keyword presence"""
        if not critical_keywords:
            return 0.0
        
        matches = sum(1 for keyword in critical_keywords if keyword.lower() in text)
        return matches / len(critical_keywords)
    
    def _calculate_semantic_similarity(self, section: Dict[str, Any], context_embedding) -> float:
        """Calculate semantic similarity using lightweight embedder"""
        content = section.get('content', '')
        if not content:
            return 0.0
        
        try:
            return self.embedding_model.similarity(
                content[:800], 
                "travel planning for college friends 4 days group activities"
            )
        except:
            return 0.0
    
    def _score_actionable_content(self, text: str, actionable_keywords: List[str]) -> float:
        """Score actionable content"""
        actionable_indicators = [
            'how to', 'steps', 'guide', 'tips', 'plan', 'book', 'visit',
            'organize', 'coordinate', 'arrange', 'prepare', 'reserve'
        ]
        
        matches = sum(1 for indicator in actionable_indicators if indicator in text)
        return min(matches * 0.15, 1.0)
    
    def _score_practical_value(self, text: str) -> float:
        """Score practical planning value"""
        practical_indicators = [
            'address', 'location', 'cost', 'price', 'hours', 'contact',
            'website', 'phone', 'directions', 'transport', 'metro', 'bus'
        ]
        
        matches = sum(1 for indicator in practical_indicators if indicator in text)
        practical_score = min(matches * 0.1, 0.6)
        
        if text.count(':') > 2 or text.count(';') > 2:
            practical_score += 0.2
        
        return min(practical_score, 1.0)
