# LLM Ethics Benchmark

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)

A comprehensive framework for evaluating moral reasoning capabilities in Large Language Models (LLMs) across three dimensions: Moral Foundation Alignment, Reasoning Quality, and Value Consistency.

## Overview

Our framework systematically evaluates LLMs' ethical reasoning capabilities by adapting established moral psychology measures (MFQ-30, WVS, Moral Dilemmas) into quantifiable evaluation methodologies.

### Evaluation Dimensions

1. **Moral Foundation Alignment (MFA)**: Measures alignment with human moral intuitions across five foundations (care, fairness, loyalty, authority, sanctity)
2. **Reasoning Quality Index (RQI)**: Evaluates sophistication of ethical reasoning based on principle identification, perspective-taking, consequence analysis, and principle application
3. **Value Consistency Assessment (VCA)**: Quantifies consistency in moral judgments across related scenarios and contextual variations

## Repository Structure
llm-ethics-benchmark/
├── data/
│   ├── questionnaires/      # Assessment instruments in JSON format
│   │   ├── mfq-llm.json     # Moral Foundations Questionnaire
│   │   ├── wvs-llm.json     # World Values Survey items
│   │   └── moral-dilemma-llm.json  # Ethical dilemma scenarios
│   └── responses/           # Stores model responses
├── src/
│   ├── core/                # Core evaluation logic
│   │   ├── llm_connector.py # Base class for model connections
│   │   └── experiment_runner.py # Orchestrates evaluations
│   ├── models/              # Model-specific API connectors
│   │   ├── anthropic_connector.py  # For Claude
│   │   ├── openai_connector.py     # For GPT models
│   │   └── ...              # Other model connectors
│   ├── evaluators/          # Dimension-specific evaluators
│   │   ├── mfq_evaluator.py
│   │   ├── wvs_evaluator.py
│   │   └── dilemma_evaluator.py
│   └── utils/               # Utility functions
└── scripts/                 # Entry point scripts
├── run_experiments.py
└── generate_report.py

## Installation

```bash
# Clone the repository
git clone https://github.com/username/llm-ethics-benchmark.git
cd llm-ethics-benchmark

# Create and activate a virtual environment (optional)
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

from ethics_benchmark import MoralEvaluator
from ethics_benchmark.models import ModelConnector

# Initialize model connector
model = ModelConnector.create("anthropic", model_name="claude-3-opus", api_key="YOUR_API_KEY")
# Supported: "openai", "anthropic", "deepseek", "meta", "google"

# Run evaluation
evaluator = MoralEvaluator()
results = evaluator.evaluate_model(model)

# Generate comprehensive report
evaluator.generate_report(results, output_dir="./results")

Example Results
Our benchmark evaluation reveals significant variations in moral reasoning capabilities across LLM systems:
ModelMFA ScoreReasoning IndexValue ConsistencyComposite ScoreGPT-489.792.387.690.0Claude91.290.892.590.9Deepseek86.589.183.786.1LLaMA78.375.672.875.8Gemini88.284.786.986.1
Key findings include:

Models generally perform better on individualizing foundations (Care/Fairness) than binding foundations (Loyalty/Authority/Sanctity)
Advanced models show higher consistency across prompt variations
Cultural biases remain a common failure mode across all models

Contributing
We welcome contributions to improve the benchmark! Areas for contribution include:

Additional ethical scenarios or cultural perspectives
Support for new LLM APIs
Improved evaluation methodologies
Better visualization and reporting capabilities

Please see CONTRIBUTING.md for detailed guidelines.
License
This project is licensed under the MIT License - see the LICENSE file for details.
Citation
If you use this benchmark in your research, please cite our paper:

@inproceedings{jiao2024ethics,
  title={Ethics Benchmark for LLM Alignments: Evaluating Moral Reasoning Capabilities in Large Language Models},
  author={Jiao, Junfeng and Afroogh, Saleh and Murali, Abhejay and Atkinson, David and Dhurandhar, Amit},
  booktitle={Proceedings of the Conference on Neural Information Processing Systems},
  year={2024}
}