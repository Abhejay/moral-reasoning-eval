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