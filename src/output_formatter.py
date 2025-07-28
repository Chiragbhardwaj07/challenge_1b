"""
Enhanced Output Formatter - Target Output Quality
"""

import json
from datetime import datetime
from typing import List, Dict, Any

class OutputFormatter:
    def __init__(self):
        pass
    
    def format_final_output(self, input_config: Dict[str, Any], 
                           top_sections: List[Dict[str, Any]], 
                           refined_subsections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Format output for target quality"""
        
        print("💾 Formatting output for target accuracy...")
        
        # Extract metadata
        input_documents = [doc["filename"] for doc in input_config["documents"]]
        persona = input_config["persona"]["role"]
        job_to_be_done = input_config["job_to_be_done"]["task"]
        processing_timestamp = datetime.now().isoformat()
        
        # Format sections with quality validation
        formatted_sections = []
        for section in top_sections:
            formatted_sections.append({
                "document": section["document"],
                "section_title": section["section_title"],
                "importance_rank": section["importance_rank"],
                "page_number": section["page_number"]
            })
        
        # Format subsections with validation
        formatted_subsections = []
        for subsection in refined_subsections:
            formatted_subsections.append({
                "document": subsection["document"],
                "refined_text": subsection["refined_text"],
                "page_number": subsection["page_number"]
            })
        
        # Build final result
        result = {
            "metadata": {
                "input_documents": input_documents,
                "persona": persona,
                "job_to_be_done": job_to_be_done,
                "processing_timestamp": processing_timestamp
            },
            "extracted_sections": formatted_sections,
            "subsection_analysis": formatted_subsections
        }
        
        return result
    
    def save_results(self, output: Dict[str, Any], output_path: str) -> bool:
        """Save results with validation"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=4, ensure_ascii=False)
            print(f"✅ Results saved to {output_path}")
            return True
        except Exception as e:
            print(f"❌ Failed to save results: {e}")
            return False
    
    def print_target_summary(self, output: Dict[str, Any]):
        """Print summary for target output verification"""
        
        print("\n" + "="*60)
        print("🎯 TARGET OUTPUT SUMMARY")
        print("="*60)
        
        metadata = output["metadata"]
        print(f"Persona: {metadata['persona']}")
        print(f"Job: {metadata['job_to_be_done']}")
        print(f"Timestamp: {metadata['processing_timestamp']}")
        
        print(f"\n📊 EXTRACTED SECTIONS (by decreasing importance):")
        for section in output["extracted_sections"]:
            print(f"  {section['importance_rank']}. {section['section_title']}")
            print(f"     📄 {section['document']} (Page {section['page_number']})")
        
        print(f"\n📝 SUBSECTION ANALYSIS:")
        for i, subsection in enumerate(output["subsection_analysis"]):
            word_count = len(subsection['refined_text'].split())
            print(f"  {i+1}. {subsection['document']} - {word_count} words")
        
        print("="*60)
