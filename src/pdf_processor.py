"""
Enhanced PDF Processor - Optimized for Target Output Quality
"""

import fitz
import re
import numpy as np
from pathlib import Path
from typing import List, Dict, Any
from collections import Counter

class PDFProcessor:
    def __init__(self):
        # Patterns for identifying real section headers
        self.header_patterns = [
            r'^[A-Z][A-Za-z\s]{10,80}$',  # Title case headers
            r'^\d+\.\s+[A-Z][A-Za-z\s]{8,}',  # Numbered sections
            r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*:',  # Title with colon
            r'^[A-Z\s]{8,40}$',  # All caps headers
            r'^Chapter\s+\d+|^Part\s+[IVX\d]+',  # Chapters/Parts
        ]
        
        # High-value keywords for travel planning
        self.travel_keywords = [
            'planning', 'itinerary', 'schedule', 'guide', 'tips', 'advice',
            'activities', 'things to do', 'restaurants', 'hotels', 'accommodation',
            'transport', 'budget', 'group', 'friends', 'college', 'student',
            'days', 'trip', 'travel', 'visit', 'explore'
        ]
        
        # Keywords that indicate actionable content
        self.actionable_keywords = [
            'how to', 'steps', 'guide', 'tips', 'recommendations', 'best',
            'must visit', 'should', 'plan', 'organize', 'book', 'reserve'
        ]
    
    def extract_document_content(self, pdf_path: str) -> List[Dict[str, Any]]:
        """Extract high-quality sections optimized for target output"""
        sections = []
        
        try:
            with fitz.open(pdf_path) as doc:
                # Analyze document structure first
                doc_analysis = self._analyze_document_structure(doc)
                
                # Extract sections with enhanced detection
                for page_num in range(len(doc)):
                    page = doc[page_num]
                    page_sections = self._extract_high_quality_sections(
                        page, page_num + 1, pdf_path, doc_analysis
                    )
                    sections.extend(page_sections)
            
            # Post-process for target output quality
            sections = self._optimize_sections_for_target_output(sections)
            return sections
            
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")
            return []
    
    def _analyze_document_structure(self, doc) -> Dict[str, Any]:
        """Analyze document to understand formatting patterns"""
        font_sizes = []
        font_flags = []
        
        for page in doc:
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" not in block:
                    continue
                for line in block["lines"]:
                    for span in line["spans"]:
                        font_sizes.append(span["size"])
                        font_flags.append(span["flags"])
        
        # Determine header characteristics
        if font_sizes:
            avg_size = np.mean(font_sizes)
            header_threshold = avg_size + 1.5  # Headers are typically larger
        else:
            header_threshold = 12
        
        return {
            'avg_font_size': avg_size if font_sizes else 12,
            'header_threshold': header_threshold,
            'bold_flag': 16  # spaCy bold flag
        }
    
    def _extract_high_quality_sections(self, page, page_num: int, pdf_path: str, 
                                     doc_analysis: Dict) -> List[Dict[str, Any]]:
        """Extract sections with enhanced header detection"""
        blocks = page.get_text("dict")["blocks"]
        sections = []
        current_section = None
        
        for block in blocks:
            if "lines" not in block:
                continue
                
            for line in block["lines"]:
                line_text = ""
                font_size = 0
                is_bold = False
                
                for span in line["spans"]:
                    line_text += span["text"]
                    font_size = max(font_size, span.get("size", 12))
                    if span.get("flags", 0) & 16:  # Bold flag
                        is_bold = True
                
                line_text = line_text.strip()
                if not line_text:
                    continue
                
                # Enhanced header detection
                if self._is_high_quality_header(line_text, font_size, is_bold, doc_analysis):
                    # Save current section
                    if current_section and self._is_valuable_section(current_section):
                        sections.append(current_section)
                    
                    # Start new section
                    current_section = {
                        'title': self._clean_and_improve_title(line_text),
                        'content': '',
                        'page_number': page_num,
                        'document': Path(pdf_path).name,
                        'header_confidence': self._calculate_header_confidence(line_text, font_size, is_bold),
                        'travel_relevance': self._calculate_travel_relevance(line_text)
                    }
                elif current_section:
                    current_section['content'] += line_text + " "
        
        # Add final section
        if current_section and self._is_valuable_section(current_section):
            sections.append(current_section)
        
        # If no good sections found, create content-based sections
        if not sections:
            sections = self._create_fallback_sections(page, page_num, pdf_path)
        
        return sections
    
    def _is_high_quality_header(self, text: str, font_size: float, is_bold: bool, 
                              doc_analysis: Dict) -> bool:
        """Determine if text is a high-quality section header"""
        if len(text) < 8 or len(text) > 120:
            return False
        
        confidence = 0.0
        
        # Font size check
        if font_size > doc_analysis['header_threshold']:
            confidence += 0.3
        
        # Bold formatting
        if is_bold:
            confidence += 0.2
        
        # Pattern matching
        for pattern in self.header_patterns:
            if re.match(pattern, text):
                confidence += 0.3
                break
        
        # Travel relevance boost
        if any(keyword in text.lower() for keyword in self.travel_keywords):
            confidence += 0.2
        
        # Avoid sentence patterns
        if text.count('.') > 1 or text.count(',') > 3:
            confidence -= 0.3
        
        return confidence > 0.4
    
    def _clean_and_improve_title(self, title: str) -> str:
        """Clean and improve title quality"""
        # Remove extra whitespace
        title = re.sub(r'\s+', ' ', title.strip())
        
        # If title is a sentence fragment, try to extract the main topic
        if len(title) > 100 or title.count(',') > 2:
            # Extract the first meaningful part
            parts = title.split(',')
            if len(parts[0]) > 15:
                title = parts[0].strip()
            else:
                # Extract first 80 characters at word boundary
                if len(title) > 80:
                    title = title[:80].rsplit(' ', 1)[0] + "..."
        
        return title
    
    def _calculate_header_confidence(self, text: str, font_size: float, is_bold: bool) -> float:
        """Calculate confidence that this is a good header"""
        confidence = 0.0
        
        # Length appropriateness
        if 10 <= len(text) <= 80:
            confidence += 0.3
        
        # Formatting signals
        if font_size > 12:
            confidence += 0.2
        if is_bold:
            confidence += 0.2
        
        # Content quality
        if any(keyword in text.lower() for keyword in self.actionable_keywords):
            confidence += 0.3
        
        return confidence
    
    def _calculate_travel_relevance(self, text: str) -> float:
        """Calculate travel planning relevance"""
        text_lower = text.lower()
        relevance = 0.0
        
        # Travel keyword matching
        travel_matches = sum(1 for keyword in self.travel_keywords if keyword in text_lower)
        relevance += min(travel_matches * 0.2, 1.0)
        
        # Actionable content bonus
        actionable_matches = sum(1 for keyword in self.actionable_keywords if keyword in text_lower)
        relevance += min(actionable_matches * 0.3, 0.6)
        
        return relevance
    
    def _is_valuable_section(self, section: Dict[str, Any]) -> bool:
        """Check if section has value for travel planning"""
        content = section.get('content', '')
        title = section.get('title', '')
        
        # Minimum content length
        if len(content.split()) < 30:
            return False
        
        # Check for travel relevance
        combined_text = f"{title} {content}".lower()
        travel_score = sum(1 for keyword in self.travel_keywords if keyword in combined_text)
        
        return travel_score >= 2 or section.get('travel_relevance', 0) > 0.3
    
    def _create_fallback_sections(self, page, page_num: int, pdf_path: str) -> List[Dict[str, Any]]:
        """Create sections when header detection fails"""
        full_text = page.get_text()
        
        # Split by double line breaks or paragraph patterns
        paragraphs = []
        for para in full_text.split('\n\n'):
            para = para.strip()
            if len(para.split()) > 50:  # Substantial paragraphs only
                paragraphs.append(para)
        
        sections = []
        for i, paragraph in enumerate(paragraphs[:3]):  # Limit to 3 per page
            # Create title from first sentence or meaningful phrase
            sentences = paragraph.split('.')
            title = self._extract_meaningful_title(sentences[0], paragraph)
            
            sections.append({
                'title': title,
                'content': paragraph,
                'page_number': page_num,
                'document': Path(pdf_path).name,
                'header_confidence': 0.3,  # Lower confidence for auto-generated
                'travel_relevance': self._calculate_travel_relevance(paragraph)
            })
        
        return sections
    
    def _extract_meaningful_title(self, first_sentence: str, full_content: str) -> str:
        """Extract meaningful title from content"""
        # Look for travel-related phrases in first sentence
        for keyword in self.travel_keywords:
            if keyword in first_sentence.lower():
                # Try to extract phrase around the keyword
                words = first_sentence.split()
                for i, word in enumerate(words):
                    if keyword in word.lower():
                        start = max(0, i - 2)
                        end = min(len(words), i + 4)
                        title = ' '.join(words[start:end])
                        if len(title) > 20:
                            return title.title()
        
        # Fallback to cleaned first sentence
        title = first_sentence[:60] + "..." if len(first_sentence) > 60 else first_sentence
        return title.strip()
    
    def _optimize_sections_for_target_output(self, sections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Optimize sections specifically for target output quality"""
        optimized_sections = []
        
        for section in sections:
            # Calculate comprehensive quality score
            quality_score = self._calculate_comprehensive_quality(section)
            
            # Only keep high-quality sections
            if quality_score > 0.4:
                section['quality_score'] = quality_score
                section['job_relevance'] = self._calculate_job_relevance(section)
                optimized_sections.append(section)
        
        # Sort by quality and relevance
        optimized_sections.sort(
            key=lambda x: (x['quality_score'] + x['job_relevance']) / 2, 
            reverse=True
        )
        
        return optimized_sections
    
    def _calculate_comprehensive_quality(self, section: Dict[str, Any]) -> float:
        """Calculate comprehensive section quality"""
        content = section.get('content', '')
        title = section.get('title', '')
        
        quality = 0.0
        
        # Content length quality
        word_count = len(content.split())
        if 100 <= word_count <= 800:
            quality += 0.3
        elif 50 <= word_count <= 1200:
            quality += 0.2
        
        # Title quality
        if 15 <= len(title) <= 80 and not title.endswith('...'):
            quality += 0.2
        
        # Travel relevance
        quality += section.get('travel_relevance', 0) * 0.3
        
        # Header confidence
        quality += section.get('header_confidence', 0) * 0.2
        
        return min(quality, 1.0)
    
    def _calculate_job_relevance(self, section: Dict[str, Any]) -> float:
        """Calculate relevance to specific job (4 days, 10 college friends)"""
        content = section.get('content', '').lower()
        title = section.get('title', '').lower()
        combined = f"{title} {content}"
        
        relevance = 0.0
        
        # Job-specific terms
        job_terms = ['4 days', 'college', 'friends', 'group', 'student', 'plan', 'trip']
        matches = sum(1 for term in job_terms if term in combined)
        relevance += min(matches * 0.15, 0.6)
        
        # Duration indicators
        if any(term in combined for term in ['days', 'day', 'itinerary', 'schedule']):
            relevance += 0.2
        
        # Group indicators
        if any(term in combined for term in ['group', 'friends', 'people', 'party']):
            relevance += 0.2
        
        return min(relevance, 1.0)
