# Intelligent Threat Qualification Engine (ITQE)

## Project Overview
ITQE is an integrated, semi-autonomous AI pipeline for Security Operations Centers (SOCs). It synthesizes a machine learning classifier (P3), a fine-tuned generative language model (P5), and a bounded Plan-and-Execute agent (P6) to qualify network telemetry, draft incident briefs, and verify numerical fidelity before routing to a human analyst.

## Environment Setup
To run this project, ensure you have Python 3.10+ installed. 

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate