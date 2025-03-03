import argparse
from pathlib import Path
from src.utils.data_loader import load_results
from src.evaluators.mfq_evaluator import MFQEvaluator

def main():
    parser = argparse.ArgumentParser(description='Analyze MFQ experiment results')
    parser.add_argument('results_file', help='Path to results JSON file')
    parser.add_argument('--output-dir', help='Directory to save analysis results')
    args = parser.parse_args()
    
    # Load results
    results = load_results(args.results_file)
    
    # Determine output directory
    if args.output_dir:
        output_dir = args.output_dir
    else:
        results_path = Path(args.results_file)
        output_dir = results_path.parent / f"analysis_{results_path.stem}"
    
    # Run analysis
    evaluator = MFQEvaluator()
    report_path = evaluator.create_analysis_report(results, output_dir)
    
    print(f"Analysis complete! Report saved to {report_path}")
    print(f"Visualizations saved to {output_dir}")

if __name__ == "__main__":
    main()