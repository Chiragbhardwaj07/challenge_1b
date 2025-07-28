# Challenge 1B: Execution Instructions

## 📘 Overview
This guide will help you run the Challenge 1B solution step-by-step, even if you're new to Docker or command-line tools. The system analyzes PDF documents and extracts the most relevant sections based on a specific persona and job requirements.

### What this system does
Given a collection of PDF documents and a specific task (like "plan a trip for college friends"), it finds and ranks the most useful sections from those documents.

## 💻 Prerequisites & Setup

### What You Need
- Docker Desktop installed on your computer
- At least 8GB of RAM (16GB recommended)
- 2GB of free storage space
- Your PDF documents that need to be analyzed

### Step 1: Install Docker Desktop
1. Go to [docker.com](https://www.docker.com)
2. Download Docker Desktop for your OS (Windows, Mac, or Linux)
3. Install and start Docker Desktop
4. Wait for Docker to fully start (you'll see a green indicator)

### Step 2: Verify Docker Works
Open your terminal/command prompt and type:

```bash
docker --version
```

You should see something like `Docker version 20.10.x`. If not, Docker isn't installed correctly.

## 📂 Preparing Your Input Files

### Step 1: Organize Your PDF Documents
Create a folder structure like this:

```
challenge-1b/
├── input/
│   ├── pdf/                  ← Put ALL your PDF files here
│   └── challenge_config.json ← Configuration file (see below)
└── (other project files...)
```

### Step 2: Create Configuration File
Inside the `input/` folder, create a file `challenge_config.json` with this structure:

```json
{
    "challenge_info": {
        "challenge_id": "round_1b_XXX",
        "test_case_name": "your_test_case_name",
        "description": "Brief description of your test case"
    },
    "documents": [
        {
            "filename": "your_first_document.pdf",
            "title": "First Document Title"
        },
        {
            "filename": "your_second_document.pdf",
            "title": "Second Document Title"
        }
    ],
    "persona": {
        "role": "Travel Planner"
    },
    "job_to_be_done": {
        "task": "Plan a trip of 4 days for a group of 10 college friends."
    }
}
```

Update `"documents"` with your actual file names and readable titles.

## 🔧 Step 3: Customize the Configuration

You **must** update the configuration file (`input/challenge_config.json`) to match your specific use case.

### 🗂️ Update the `documents` Section

List every PDF file you placed in the `input/pdf/` folder.

Example:

```json
"documents": [
  {
    "filename": "document1.pdf",   
    "title": "Readable title"
  },
  {
    "filename": "document2.pdf",   
    "title": "Another document"
  }
]
```

- **`filename`**: Must exactly match the file name in your `input/pdf/` folder (case-sensitive).
- **`title`**: A human-friendly name for the document (can include spaces).

### 👤 Set Your Persona

Change the role according to who is performing the task.

Example:

```json
"persona": {
  "role": "Travel Planner"
}
```

Other sample roles:
- `"Research Analyst"`
- `"Business Consultant"`
- `"Event Organizer"`
- `"Software Tester"`

### 🎯 Define Your Task

Clearly describe what you want the system to accomplish.

Example:

```json
"job_to_be_done": {
  "task": "Plan a trip of 4 days for a group of 10 college friends."
}
```

### ✅ Complete Example for a Different Use Case

```json
{
  "challenge_info": {
    "challenge_id": "round_1b_003",
    "test_case_name": "business_analysis",
    "description": "Market Research Analysis"
  },
  "documents": [
    {
      "filename": "Market_Report_2024.pdf",
      "title": "Annual Market Report"
    },
    {
      "filename": "Competitor_Analysis.pdf",
      "title": "Competitor Analysis"
    },
    {
      "filename": "Customer_Survey.pdf",
      "title": "Customer Survey Results"
    }
  ],
  "persona": {
    "role": "Business Analyst"
  },
  "job_to_be_done": {
    "task": "Analyze market trends and provide recommendations for product launch strategy."
  }
}
```


## 🚀 Running the Solution

### Step 1: Open Terminal/Command Prompt
- **Windows:** Press Windows + R → type `cmd` or open PowerShell
- **Mac:** Press Cmd + Space → type `Terminal`
- **Linux:** Press Ctrl + Alt + T

### Step 2: Navigate to Your Project Folder
```bash
cd path/to/your/challenge-1b
```

### Step 3: Verify Your Files
```bash
ls input/pdf/
cat input/challenge_config.json
```

### Step 4: Build the Docker Image
```bash
docker build --platform linux/amd64 -t challenge1b:submission .
```

### Step 5: Check the Image Size
```bash
docker images challenge1b:submission
```

### Step 6: Run the Analysis

#### Mac/Linux:
```bash
docker run --rm   --platform linux/amd64   -v $(pwd)/input:/app/input   -v $(pwd)/output:/app/output   --network none   challenge1b:submission
```

#### Windows PowerShell:
```powershell
docker run --rm --platform linux/amd64 -v ${PWD}/input:/app/input -v ${PWD}/output:/app/output --network none challenge1b:submission

```

#### Windows Command Prompt:
```cmd
docker run --rm --platform linux/amd64 -v %cd%/input:/app/input -v %cd%/output:/app/output --network none challenge1b:submission
```

### What to Expect
You'll see messages like:

```
🚀 Starting Challenge 1B - Target Output Optimization
✅ Models loaded in 3.2s
📄 Processing PDFs...
📊 Target Output Ranking:
💾 Generating target output...
✅ Results saved to /app/output/results.json
```

## 📄 Understanding Your Results

Output will be saved in:

```
output/
└── results.json
```

### What's in results.json
```json
{
    "metadata": {
        "input_documents": ["doc1.pdf", "doc2.pdf"],
        "persona": "Travel Planner",
        "job_to_be_done": "Plan a trip...",
        "processing_timestamp": "2025-01-27T22:30:45.123456"
    },
    "extracted_sections": [
        {
            "document": "document1.pdf",
            "section_title": "Planning Multi-Day Group Itineraries",
            "importance_rank": 1,
            "page_number": 3
        }
    ],
    "subsection_analysis": [
        {
            "document": "document1.pdf",
            "refined_text": "Specific advice for your task...",
            "page_number": 3
        }
    ]
}
```
