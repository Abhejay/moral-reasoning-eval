import json
from typing import Dict, List, Any
from pathlib import Path

def load_questionnaire(filepath: str) -> Dict[str, Any]:
    """Load questionnaire data from a JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)

def get_all_questions(questionnaire: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract all questions from the questionnaire."""
    questions = []
    
    # Process the MFQ structure specifically
    foundations = questionnaire.get('foundations', {})
    for foundation_key, foundation in foundations.items():
        # Add relevance questions
        for question in foundation.get('relevance_questions', []):
            questions.append({
                'id': question['id'],
                'foundation': foundation_key,
                'foundation_name': foundation.get('name', foundation_key),
                'type': 'relevance',
                'prompt': question['prompt'],
                'original': question.get('original', ''),
                'ground_truth': question['ground_truth']
            })
        
        # Add agreement questions
        for question in foundation.get('agreement_questions', []):
            questions.append({
                'id': question['id'],
                'foundation': foundation_key,
                'foundation_name': foundation.get('name', foundation_key),
                'type': 'agreement',
                'prompt': question['prompt'],
                'original': question.get('original', ''),
                'ground_truth': question['ground_truth']
            })
    
    return questions

def save_results(results: List[Dict[str, Any]], filepath: str) -> None:
    """Save results to a JSON file."""
    # Ensure directory exists
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2)

def load_results(filepath: str) -> List[Dict[str, Any]]:
    """Load results from a JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)