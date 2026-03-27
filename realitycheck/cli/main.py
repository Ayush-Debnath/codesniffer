import click
from rich import print
from realitycheck.parser.ast_parser import parse_file, extract_structure
from realitycheck.analyzers.complexity import analyze_complexity
from realitycheck.analyzers.code_smells import analyze_code_smells
from realitycheck.rules.rules_engine import generate_feedback
from realitycheck.scoring.scorer import calculate_score
from realitycheck.reporter.report_generator import display_report
from realitycheck.analyzers.ai_detector import get_ai_feedback

@click.group()
def main():
    """RealityCheck AI - Code Honesty Detector"""
    pass

@main.command()
@click.argument("file_path")
def analyze(file_path):
    tree = parse_file(file_path)

    import os

    if not os.path.exists(file_path):
        print("[red]Error: File does not exist[/red]")
        return

    if not file_path.endswith(".py"):
        print("[red]Error: Only Python files supported[/red]")
        return

    if isinstance(tree, dict) and "error" in tree:
        print(f"[red]Syntax Error:[/red] {tree['error']}")
        return

    structure = extract_structure(tree)
    complexity = analyze_complexity(tree)
    smells = analyze_code_smells(tree)

    feedback = generate_feedback(structure, complexity, smells)
    score, breakdown = calculate_score(complexity, smells)

    

    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()
    ai_feedback = get_ai_feedback(code)
    display_report(score, breakdown, feedback, ai_feedback)

if __name__ == "__main__":
    main()