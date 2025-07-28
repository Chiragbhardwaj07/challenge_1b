# Challenge 1B: Approach Explanation

## 📘 Methodology Overview

Our solution implements a multi-layered persona-driven document intelligence system that extracts and ranks document sections based on specific job requirements and user personas. The approach combines traditional NLP techniques with semantic analysis to achieve high relevance scoring while maintaining computational efficiency.

---

## 🏗️ Core Architecture

### 1. Enhanced PDF Processing

We developed a font-aware section detection system that analyzes document structure using multiple signals:

- Font size analysis to identify headers vs. content
- Pattern matching for section titles using regex patterns
- Content quality assessment to filter generic introductory material
- Actionable keyword detection to prioritize practical information

### 2. Semantic Analysis Engine

The system employs a lightweight semantic analyzer that combines:

- spaCy-based NLP processing for entity recognition and linguistic analysis
- Custom lightweight embeddings using spaCy word vectors (avoiding heavy transformer models)
- Job-specific pattern matching for exact correlation with requirements (e.g., "4 days", "college friends", "group of 10")

### 3. Multi-Factor Relevance Scoring

Our scoring algorithm uses weighted relevance factors:

- **Exact Job Match (35%)**: Direct correlation with specific job requirements
- **Critical Keywords (25%)**: Persona-specific essential terms
- **Semantic Similarity (20%)**: Contextual understanding using embeddings
- **Actionable Content (10%)**: Practical, implementable information
- **Section Quality (10%)**: Content structure and completeness

### 4. Intelligent Content Extraction

The subsection extractor employs sentence-level correlation scoring:

- Sentence segmentation using spaCy's linguistic models
- Individual sentence scoring against job requirements
- Generic content avoidance (filtering "introduction", "overview" patterns)
- Quality thresholds to ensure meaningful extracted content

---

## ⚙️ Optimization Strategies

### 🔧 Performance Optimization

- **Lightweight dependencies**: Eliminated heavy ML libraries (e.g., scikit-learn, transformers) to reduce Docker image size from 11GB to <500MB
- **CPU-only execution**: Used spaCy word vectors instead of transformer-based embeddings
- **Caching mechanisms**: Offline model loading with local storage

### 🎯 Accuracy Optimization

- **Job-specific boosting**: 50% score boost for content containing exact job requirements
- **Audience targeting**: Heavy penalties for mismatched content (e.g., family tips for college friends)
- **Section quality filtering**: Minimum thresholds for content length and informativeness
- **Duplicate content detection**: Prevents redundant sections from dominating results

---

## 📏 Evaluation-Focused Design

The system prioritizes **Section Relevance (60 points)** and **Sub-section Relevance (40 points)** evaluation criteria:

- Decreasing importance ranking ensures most relevant content appears first
- Exact line correlation extraction provides precise, actionable subsections
- Timeline timestamps enable processing time evaluation
- Strict JSON format validation ensures submission compliance

---

## 🚀 Key Innovation

Our approach balances computational efficiency with semantic understanding by combining traditional NLP techniques with targeted semantic analysis, achieving competitive accuracy while maintaining deployment constraints and fast processing times.
