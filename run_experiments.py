import os
import json
import time
from dotenv import load_dotenv
from pathlib import Path
from tqdm import tqdm
from datetime import datetime
import argparse

from src.models.anthropic_connector import AnthropicConnector
from src.utils.data_loader import load_questionnaire, get_all_questions, save_results
from src.evaluators.mfq_evaluator import MFQEvaluator

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run MFQ experiment on Claude')
    parser.add_argument('--model', default='claude-3-5-sonnet-20240620', 
                        help='Claude model to use (default: claude-3-5-sonnet-20240620)')
    parser.add_argument('--max-tokens', type=int, default=1000,
                        help='Maximum tokens for response (default: 1000)')
    parser.add_argument('--questionnaire', default='data/questionnares/mfq-llm.json',
                        help='Path to questionnaire JSON file')
    parser.add_argument('--output-dir', default='data/responses/claude',
                        help='Directory to save results')
    parser.add_argument('--analyze', action='store_true',
                        help='Run analysis after experiment')
    args = parser.parse_args()
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Initialize the Claude connector
    connector = AnthropicConnector(model_name=args.model)
    
    # Load the questionnaire
    try:
        questionnaire = load_questionnaire(args.questionnaire)
        questions = get_all_questions(questionnaire)
        print(f"Loaded {len(questions)} questions from the MFQ questionnaire")
    except Exception as e:
        print(f"Error loading questionnaire: {e}")
        return
    
    # Create output directory if it doesn't exist
    output_dir = Path(f"{args.output_dir}/{args.model}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Timestamp for the run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"mfq_results_{timestamp}.json"
    
    # Track costs
    total_input_tokens = 0
    total_output_tokens = 0
    
    # Process each question
    results = []
    for q in tqdm(questions, desc="Processing questions"):
        # Generate response
        response = connector.generate_response(q['prompt'], max_tokens=args.max_tokens)
        
        if "error" in response:
            print(f"Error with question {q['id']}: {response['error']}")
            continue
            
        # Update token counts
        total_input_tokens += response["usage"]["prompt_tokens"]
        total_output_tokens += response["usage"]["completion_tokens"]
        
        # Extract score and reasoning
        extracted = connector.extract_score_and_reasoning(response["text"])
        
        # Compile result
        result = {
            "question_id": q["id"],
            "foundation": q["foundation"],
            "foundation_name": q["foundation_name"],
            "type": q["type"],
            "model": args.model,
            "original_question": q["original"],
            "prompt": q["prompt"],
            "response": response["text"],
            "extracted_score": extracted.get("score"),
            "extracted_reasoning": extracted.get("reasoning"),
            "ground_truth_mean": q["ground_truth"]["mean_score"],
            "ground_truth_consensus": q["ground_truth"]["consensus_score"],
            "ground_truth_std": q["ground_truth"]["std_score"],
            "usage": response["usage"]
        }
        
        results.append(result)
        
        # Small delay to avoid rate limits
        time.sleep(0.5)
    
    # Save results
    save_results(results, output_file)
    
    # Calculate costs
    input_cost = (total_input_tokens / 1_000_000) * 3.0  # $3 per million tokens (Claude 3.5 Sonnet)
    output_cost = (total_output_tokens / 1_000_000) * 15.0  # $15 per million tokens (Claude 3.5 Sonnet)
    total_cost = input_cost + output_cost
    
    print(f"\nRun complete! Results saved to {output_file}")
    print(f"Total input tokens: {total_input_tokens:,}")
    print(f"Total output tokens: {total_output_tokens:,}")
    print(f"Estimated cost: ${total_cost:.2f}")
    
    # Run analysis if requested
    if args.analyze:
        evaluator = MFQEvaluator()
        analysis_dir = output_dir / f"analysis_{timestamp}"
        report_path = evaluator.create_analysis_report(results, analysis_dir)
        print(f"Analysis complete! Report saved to {report_path}")
        print(f"Visualizations saved to {analysis_dir}")

if __name__ == "__main__":
    main()