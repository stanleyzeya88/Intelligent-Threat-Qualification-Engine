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

## ⚠️ Model Weights Notice
Due to GitHub's 100MB file size limit, the fine-tuned DistilGPT2 model weights (`model.safetensors`, 319MB) are not tracked in this repository.

To reproduce the pipeline:
1. Download the model from: [INSERT GOOGLE DRIVE / HUGGINGFACE LINK HERE]
2. Place it in `models/fine_tuned_distilgpt2_security/model.safetensors`
3. Ensure the other model files (`config.json`, `tokenizer.json`, etc.) are present.
