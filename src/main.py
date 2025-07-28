"""
Main Pipeline - Optimized for Target Output Quality
"""

import json
import time
import sys
import os
from pathlib import Path

def main():
    """Main pipeline optimized for target accuracy"""
    
    start_time = time.time()
    print("🚀 Starting Challenge 1B - Target Output Optimization")
    print("="*60)
    
    os.chdir('/app')
    sys.path.insert(0, '/app/src')
    sys.path.insert(0, '/app')
    
    try:
        # Import optimized modules
        from model_loader import OfflineModelLoader
        from pdf_processor import PDFProcessor
        from semantic_analyzer import SemanticAnalyzer
        from relevance_scorer import RelevanceScorer
        from subsection_extractor import SubsectionExtractor
        from output_formatter import OutputFormatter
        
        # Load models
        print("📥 Loading optimized models...")
        model_loader = OfflineModelLoader()
        
        nlp_model = model_loader.load_spacy_model()
        flashrank_model = model_loader.load_flashrank_model()
        embedding_model = model_loader.create_lightweight_embedder()
        domain_vocabularies = model_loader.load_domain_vocabularies()
        
        print(f"✅ Models loaded in {time.time() - start_time:.1f}s")
        
        # Load configuration
        print("📋 Loading configuration...")
        config_path = "/app/input/challenge_config.json"
        
        with open(config_path, 'r', encoding='utf-8') as f:
            challenge_config = json.load(f)
        
        persona = challenge_config["persona"]["role"]
        job_description = challenge_config["job_to_be_done"]["task"]
        documents = challenge_config["documents"]
        
        print(f"✅ Target: {persona} - {job_description}")
        
        # Process PDFs with enhanced extraction
        print("\n📄 Processing PDFs for target output...")
        pdf_processor = PDFProcessor()
        all_sections = []
        
        for doc_info in documents:
            pdf_path = f"/app/input/pdf/{doc_info['filename']}"
            
            if Path(pdf_path).exists():
                print(f"  Processing: {doc_info['filename']}")
                sections = pdf_processor.extract_document_content(pdf_path)
                all_sections.extend(sections)
                print(f"    ✅ Extracted {len(sections)} quality sections")
        
        print(f"✅ Total sections: {len(all_sections)}")
        
        # Enhanced semantic analysis and scoring
        print("\n🧠 Performing target-optimized analysis...")
        semantic_analyzer = SemanticAnalyzer(nlp_model, embedding_model, domain_vocabularies)
        relevance_scorer = RelevanceScorer(semantic_analyzer)
        
        # Score sections for target output
        scored_sections = relevance_scorer.score_all_sections(
            all_sections, persona, job_description
        )
        
        # Get top sections
        top_sections = relevance_scorer.get_top_sections_for_target_output(
            scored_sections, top_k=7
        )
        
        # Extract refined subsections
        print("\n📝 Extracting target-quality subsections...")
        subsection_extractor = SubsectionExtractor(semantic_analyzer)
        
        refined_subsections = subsection_extractor.extract_refined_subsections(
            top_sections, persona, job_description
        )
        
        # Format final output
        print("\n💾 Generating target output...")
        output_formatter = OutputFormatter()
        
        final_output = output_formatter.format_final_output(
            challenge_config, top_sections, refined_subsections
        )
        
        # Save results
        output_path = "/app/output/results.json"
        Path("/app/output").mkdir(exist_ok=True)
        
        success = output_formatter.save_results(final_output, output_path)
        
        if success:
            output_formatter.print_target_summary(final_output)
        
        # Final metrics
        total_time = time.time() - start_time
        print(f"\n⏱️  Processing time: {total_time:.1f}s")
        print("🎯 Target output optimization completed!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
