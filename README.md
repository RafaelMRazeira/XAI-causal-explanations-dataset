# 📝 Research Paper Repository

Welcome to the official repository for the research paper titled **"A Simple and Generic Conceptual Model for Causal Explanations"**.

## 📄 About

This repository contains all relevant materials, data, and code used in the development of the associated academic paper. The purpose is to promote transparency, reproducibility, and collaboration in research.

## 🧠 Paper Information

- **Title:** A Simple and Generic Conceptual Model for Causal Explanations
- **Authors:** Rafael Mecheseregian Razeira, Ildeberto Aparecido Rodello, Cléver Ricardo Guareis de Farias
- **Institution:** São Paulo's University
- **Status:** Under Review
- **Conference / Journal:** BRACIS 2025
<!-- - **DOI / Link:** None -->

## 📁 Repository Structure
```
├── data/ # Datasets used or referenced in the study
│   └──  sp_court_lawsuits.json # sp court lawsuits collected
│   └──  prompt_example.txt # few-shot structured ontology extraction prompt 
│   └──  lawsuits.json # ontology JSON extracted from lawsuits using ChatGPT4o
├── figures/ # Figures and diagrams used in the paper
├── results/ # Spreadsheet results from manual evaluation
├── src/ # Source script code to generate results
└── README.md # Project overview
```

## NOTES

* In lawsuits.json the key ***whole_gpt*** was the one used to evaluate the paper!


## 🚀 Getting Started

To run the code or reproduce results:

#### 1. Clone the repository:
```bash
git clone git@github.com:RafaelMRazeira/XAI-causal-explanations-dataset.git
cd XAI-causal-explanations-dataset
```

#### 2. Install dependencies:
```bash
pip install -r requirements.txt
```

#### 3. Set you OPENAI_API_KEY and run the script:
```bash
export OPENAI_API_KEY="your_key" 
python src/extract_json_from_lawsuits.py
```

## 📜 License
This project is licensed under the MIT License, unless stated otherwise.