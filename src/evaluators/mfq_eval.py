from typing import Dict, Any, List
import numpy as np
from pathlib import Path
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class MFQEvaluator:
    """Evaluator for Moral Foundations Questionnaire responses."""
    
    def __init__(self):
        self.foundation_colors = {
            'care': '#FF9999',      # Light red
            'fairness': '#99FF99',  # Light green
            'loyalty': '#9999FF',   # Light blue
            'authority': '#FFFF99', # Light yellow
            'sanctity': '#FF99FF'   # Light purple
        }
    
    def calculate_score_metrics(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate score metrics from results."""
        # Extract scores
        model_scores = []
        ground_truth_scores = []
        
        for result in results:
            if result.get('extracted_score') is not None:
                model_scores.append(result['extracted_score'])
                ground_truth_scores.append(result['ground_truth_mean'])
        
        model_scores = np.array(model_scores)
        ground_truth_scores = np.array(ground_truth_scores)
        
        # Calculate differences
        score_diff = model_scores - ground_truth_scores
        
        # Calculate metrics
        metrics = {
            'accuracy': {
                'exact_match': np.mean(model_scores == ground_truth_scores) * 100,
                'within_0.5': np.mean(np.abs(score_diff) <= 0.5) * 100,
                'within_1.0': np.mean(np.abs(score_diff) <= 1.0) * 100
            },
            'error': {
                'mae': np.mean(np.abs(score_diff)),
                'rmse': np.sqrt(np.mean(score_diff ** 2)),
                'bias': np.mean(score_diff)
            },
            'correlation': {
                'pearson': np.corrcoef(model_scores, ground_truth_scores)[0, 1]
            }
        }
        
        return metrics

    def calculate_foundation_metrics(self, results: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Calculate metrics per foundation."""
        foundations = {}
        
        # Group results by foundation
        for result in results:
            foundation = result.get('foundation')
            if not foundation:
                continue
                
            if foundation not in foundations:
                foundations[foundation] = []
                
            foundations[foundation].append(result)
            
        # Calculate metrics per foundation
        foundation_metrics = {}
        for foundation, foundation_results in foundations.items():
            foundation_metrics[foundation] = self.calculate_score_metrics(foundation_results)
            
        return foundation_metrics
    
    def create_analysis_report(self, results: List[Dict[str, Any]], output_dir: str) -> str:
        """Create an analysis report from results."""
        # Ensure output directory exists
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Calculate overall metrics
        overall_metrics = self.calculate_score_metrics(results)
        foundation_metrics = self.calculate_foundation_metrics(results)
        
        # Convert results to DataFrame for easier analysis
        df = pd.DataFrame(results)
        
        # Create basic report
        report = {
            'overall_metrics': overall_metrics,
            'foundation_metrics': foundation_metrics,
            'summary': {
                'total_questions': len(results),
                'valid_responses': sum(1 for r in results if r.get('extracted_score') is not None),
                'model': results[0].get('model') if results else 'unknown'
            }
        }
        
        # Save report
        report_path = Path(output_dir) / 'analysis_report.json'
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
            
        # Create visualizations
        self._create_score_comparison_chart(df, output_dir)
        self._create_foundation_error_chart(df, output_dir)
        
        return str(report_path)
    
    def _create_score_comparison_chart(self, df: pd.DataFrame, output_dir: str) -> None:
        """Create a score comparison chart."""
        # Filter valid responses
        valid_df = df[df['extracted_score'].notna()].copy()
        
        plt.figure(figsize=(10, 6))
        plt.scatter(valid_df['ground_truth_mean'], valid_df['extracted_score'], 
                   c=[self.foundation_colors.get(f, '#CCCCCC') for f in valid_df['foundation']], alpha=0.7)
        
        # Add diagonal line (perfect prediction)
        min_val = min(valid_df['ground_truth_mean'].min(), valid_df['extracted_score'].min())
        max_val = max(valid_df['ground_truth_mean'].max(), valid_df['extracted_score'].max())
        plt.plot([min_val, max_val], [min_val, max_val], 'k--', alpha=0.5)
        
        plt.xlabel('Ground Truth Score')
        plt.ylabel('Model Score')
        plt.title('Comparison of Model Scores vs Ground Truth')
        plt.grid(alpha=0.3)
        
        # Add foundation legend
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor=color, label=foundation.capitalize())
                         for foundation, color in self.foundation_colors.items()]
        plt.legend(handles=legend_elements, loc='best')
        
        plt.tight_layout()
        plt.savefig(Path(output_dir) / 'score_comparison.png', dpi=300)
        plt.close()
    
    def _create_foundation_error_chart(self, df: pd.DataFrame, output_dir: str) -> None:
        """Create a foundation error chart."""
        # Filter valid responses and calculate error
        valid_df = df[df['extracted_score'].notna()].copy()
        valid_df['error'] = valid_df['extracted_score'] - valid_df['ground_truth_mean']
        
        plt.figure(figsize=(10, 6))
        
        # Create boxplot for each foundation
        sns.boxplot(x='foundation', y='error', data=valid_df, 
                   palette=self.foundation_colors, showfliers=False)
        
        sns.stripplot(x='foundation', y='error', data=valid_df, 
                     color='black', alpha=0.5, jitter=True, size=3)
        
        plt.axhline(y=0, color='red', linestyle='--', alpha=0.5)
        
        plt.xlabel('Moral Foundation')
        plt.ylabel('Error (Model - Ground Truth)')
        plt.title('Error Distribution by Moral Foundation')
        plt.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(Path(output_dir) / 'foundation_error.png', dpi=300)
        plt.close()