"""
Enhanced Subsection Extractor - Optimized for Target Output Quality
"""

import re
import numpy as np
from typing import List, Dict, Any, Tuple

class SubsectionExtractor:
    def __init__(self, semantic_analyzer):
        self.semantic_analyzer = semantic_analyzer
        
        # Job-specific correlation terms
        self.job_correlation_terms = [
            "4 days", "college", "friends", "group", "student", "plan", "planning",
            "itinerary", "schedule", "organize", "budget", "activities", "visit"
        ]
        
        # Avoid these generic terms
        self.avoid_terms = [
            "introduction", "overview", "welcome", "about this", "general",
            "in general", "typically", "usually", "known for"
        ]
    
    def extract_refined_subsections(self, top_sections: List[Dict[str, Any]], 
                                   persona: str, job_description: str) -> List[Dict[str, Any]]:
        """Extract refined subsections optimized for target output"""
        
        print(f"📝 Extracting refined subsections for target accuracy...")
        
        requirements = self.semantic_analyzer.analyze_persona_requirements(
            persona, job_description
        )
        
        refined_subsections = []
        
        for i, section in enumerate(top_sections):
            refined_content = self._extract_target_quality_content(
                section, requirements
            )
            
            if refined_content and len(refined_content.strip()) > 80:
                refined_subsections.append({
                    'document': section['document'],
                    'refined_text': refined_content,
                    'page_number': section['page_number']
                })
                
                print(f"  ✅ Subsection {i+1}: {len(refined_content.split())} words extracted")
            else:
                print(f"  ⚠️ Subsection {i+1}: Low quality content, using fallback")
                # Use fallback extraction
                fallback_content = self._fallback_content_extraction(section, requirements)
                if fallback_content:
                    refined_subsections.append({
                        'document': section['document'],
                        'refined_text': fallback_content,
                        'page_number': section['page_number']
                    })
        
        print(f"✅ Generated {len(refined_subsections)} refined subsections")
        return refined_subsections
    
    def _extract_target_quality_content(self, section: Dict[str, Any], 
                                      requirements: Dict[str, Any]) -> str:
        """Extract high-quality content matching target output requirements"""
        
        content = section.get('content', '')
        if not content:
            return ""
        
        # Split into sentences for precise extraction
        sentences = self._split_into_quality_sentences(content)
        
        # Score sentences for job relevance
        sentence_scores = []
        for sentence in sentences:
            if self._should_avoid_sentence(sentence):
                continue
            
            score = self._score_sentence_for_target(sentence, requirements)
            if score > 0.4:  # Higher threshold for quality
                sentence_scores.append((sentence, score))
        
        # If we have good sentences, combine them
        if sentence_scores:
            return self._combine_high_quality_sentences(sentence_scores)
        else:
            return ""
    
    def _split_into_quality_sentences(self, content: str) -> List[str]:
        """Split content into quality sentences using spaCy"""
        try:
            doc = self.semantic_analyzer.nlp(content)
            sentences = []
            
            for sent in doc.sents:
                sentence_text = sent.text.strip()
                # Keep substantial sentences
                if len(sentence_text) > 25 and len(sentence_text.split()) > 5:
                    sentences.append(sentence_text)
            
            return sentences
        except:
            # Fallback to simple splitting
            return [s.strip() + '.' for s in content.split('.') if len(s.strip()) > 25]
    
    def _should_avoid_sentence(self, sentence: str) -> bool:
        """Check if sentence should be avoided"""
        sentence_lower = sentence.lower()
        
        # Avoid generic content
        for term in self.avoid_terms:
            if term in sentence_lower:
                return True
        
        # Avoid very short or very long sentences
        if len(sentence.split()) < 8 or len(sentence.split()) > 50:
            return True
        
        # Avoid sentences that are mostly proper names or locations without context
        if sentence.count(':') == 0 and sentence.count(',') > 3:
            return True
        
        return False
    
    def _score_sentence_for_target(self, sentence: str, requirements: Dict[str, Any]) -> float:
        """Score sentence for target output quality"""
        
        sentence_lower = sentence.lower()
        score = 0.0
        
        # Job correlation (highest weight)
        job_analysis = requirements['job_analysis']
        
        if job_analysis['duration'] and job_analysis['duration'].lower() in sentence_lower:
            score += 0.6
        
        if job_analysis['group_size'] and str(job_analysis['group_size']) in sentence_lower:
            score += 0.5
        
        if job_analysis['group_type'] and job_analysis['group_type'].lower() in sentence_lower:
            score += 0.4
        
        # Keyword correlation
        keyword_matches = sum(1 for term in self.job_correlation_terms 
                            if term.lower() in sentence_lower)
        score += min(keyword_matches * 0.15, 0.6)
        
        # Actionable content bonus
        actionable_terms = ['plan', 'visit', 'book', 'organize', 'coordinate', 'arrange']
        actionable_matches = sum(1 for term in actionable_terms if term in sentence_lower)
        score += min(actionable_matches * 0.1, 0.3)
        
        # Practical information bonus
        practical_terms = ['cost', 'price', 'address', 'hours', 'phone', 'website']
        practical_matches = sum(1 for term in practical_terms if term in sentence_lower)
        score += min(practical_matches * 0.1, 0.2)
        
        # Specific details bonus (numbers, times, names)
        if re.search(r'\b\d+\b', sentence):
            score += 0.1
        
        return min(score, 1.0)
    
    def _combine_high_quality_sentences(self, sentence_scores: List[Tuple[str, float]], 
                                      max_words: int = 250) -> str:
        """Combine high-quality sentences into coherent text"""
        
        # Sort by score
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        
        combined_text = ""
        word_count = 0
        
        for sentence, score in sentence_scores:
            sentence_words = len(sentence.split())
            
            if word_count + sentence_words <= max_words:
                if combined_text:
                    combined_text += " "
                combined_text += sentence
                word_count += sentence_words
            elif word_count < max_words * 0.7:  # If we don't have enough content
                if combined_text:
                    combined_text += " "
                combined_text += sentence
                word_count += sentence_words
            else:
                break
        
        return self._clean_final_text(combined_text)
    
    def _fallback_content_extraction(self, section: Dict[str, Any], 
                                   requirements: Dict[str, Any]) -> str:
        """Fallback extraction when no high-quality sentences found"""
        
        content = section.get('content', '')
        if not content:
            return ""
        
        # Extract first meaningful paragraph that's not generic
        paragraphs = content.split('\n\n')
        
        for paragraph in paragraphs[:3]:
            paragraph = paragraph.strip()
            if (len(paragraph.split()) > 20 and 
                not any(term in paragraph.lower() for term in self.avoid_terms)):
                
                # Truncate to reasonable length
                words = paragraph.split()
                if len(words) > 200:
                    paragraph = ' '.join(words[:200]) + "..."
                
                return self._clean_final_text(paragraph)
        
        # Last resort: use beginning of content
        words = content.split()[:150]  # First 150 words
        return self._clean_final_text(' '.join(words))
    
    def _clean_final_text(self, text: str) -> str:
        """Clean and format final text"""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Ensure proper sentence endings
        if text and not text.endswith('.'):
            text += '.'
        
        # Fix sentence boundaries
        text = re.sub(r'([a-z])([A-Z])', r'\1. \2', text)
        
        # Remove very short trailing fragments
        sentences = text.split('.')
        if len(sentences) > 1 and len(sentences[-1].strip()) < 8:
            text = '.'.join(sentences[:-1]) + '.'
        
        return text
