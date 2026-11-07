# Intelligent Threat Qualification Engine (ITQE)

## Project Overview
ITQE is an integrated, semi-autonomous AI pipeline for Security Operations Centers (SOCs). It synthesizes a machine learning classifier (Project 3), a fine-tuned generative language model (Project 5), and a bounded Plan-and-Execute agent (Project 6) to qualify network telemetry, draft incident briefs, and verify numerical fidelity before routing to a human analyst. 

By introducing a novel Slot Verifier (Project 7), the system programmatically checks LLM-generated text against raw tabular data to catch numerical hallucinations. The system enforces an autonomy boundary: it explicitly outputs `CANNOT_VERIFY` and routes the event to a human if the LLM drifts from the source data. It never auto-dispatches incident responses.

## Environment Setup
To run this project, ensure you have Python 3.10+ installed.

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv

   # Windows:
   venv\Scripts\activate

   # Mac/Linux:
   source venv/bin/activate
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Open the notebook:
   ```bash
   jupyter notebook pipeline.ipynb
   ```

## ⚠️ Data & Model Weights Notice
To respect GitHub's file size limits, the following large assets are **not** committed directly to this repository. Both must be downloaded and placed in their correct folders before running the notebook.

### 1. NSL-KDD Dataset (`KDDTrain+.csv`)
- **Download:** https://www.kaggle.com/datasets/harrisonm/nslkdd
- **Place in:** `data/KDDTrain+.csv`
- **Expected shape:** 25,192 rows × 43 columns

### 2. Fine-Tuned DistilGPT2 Model (`model.safetensors`)
- **Download:** [INSERT YOUR GOOGLE DRIVE OR HUGGINGFACE LINK HERE]
- **Place in:** `models/fine_tuned_distilgpt2_security/model.safetensors`
- **Also required in the same folder:** `config.json`, `generation_config.json`, `tokenizer.json`, `tokenizer_config.json`

## Project Structure
```text
intelligent-threat-qualification-engine/
├── README.md
├── requirements.txt
├── pipeline.ipynb
├── ITQE - Module Summary.pdf
├── The ITQE architecture Diagram.png
├── data/
│   └── KDDTrain+.csv          (download separately)
├── models/
│   └── fine_tuned_distilgpt2_security/
│       ├── config.json
│       ├── generation_config.json
│       ├── model.safetensors  (download separately)
│       ├── tokenizer.json
│       └── tokenizer_config.json
└── src/
    ├── __init__.py
    ├── input_gate.py
    ├── classifier.py
    ├── brief_writer.py
    ├── verifier.py
    ├── ITQE_agent.py
    └── report.py
```

## Evaluation Summary
The ITQE agent is tested on 5 real-world fixtures from the NSL-KDD dataset:

| Fixture | Input Type | Final Status | What It Proves |
| :--- | :--- | :--- | :--- |
| **F1** | Neptune DoS | `CANNOT_VERIFY` | Verifier caught severe LLM slot drift. |
| **F2** | Satan Probe | `CANNOT_VERIFY` | Verifier caught drift across different attack types. |
| **F3** | Normal Benign | `BENIGN` | Confidence gate saves LLM compute. |
| **F4** | Malformed | `REFUSED` | Input Gate rejected bad schema at Iteration 0. |
| **F5** | Loadmodule | `BENIGN` | **Silent False Negative** (Class Imbalance). |

## References
- Alahmadi et al. (2022). 99% false positives: SOC analysts' perspectives. *USENIX Security*.
- Ji et al. (2023). Survey of hallucination in natural language generation. *ACM Computing Surveys*.
- NIST (2023). *AI Risk Management Framework (AI RMF 1.0)*.
- Tavallaee et al. (2009). A detailed analysis of the KDD CUP 99 data set. *IEEE CISDA*.
- Yao et al. (2023). ReAct: Synergizing reasoning and acting in language models. *ICLR*.
```
