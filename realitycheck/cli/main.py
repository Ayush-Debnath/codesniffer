import click
from rich import print
from realitycheck.parser.ast_parser import parse_file, extract_structure
from realitycheck.analyzers.complexity import analyze_complexity
from realitycheck.analyzers.code_smells import analyze_code_smells
from realitycheck.rules.rules_engine import generate_feedback
from realitycheck.scoring.scorer import calculate_score

@click.group()
def main():
    """RealityCheck AI - Code Honesty Detector"""
    pass

@main.command()
@click.argument("file_path")
def analyze(file_path):
    tree = parse_file(file_path)

    if isinstance(tree, dict) and "error" in tree:
        print(f"[red]Syntax Error:[/red] {tree['error']}")
        return

    structure = extract_structure(tree)
    complexity = analyze_complexity(tree)
    smells = analyze_code_smells(tree)

    feedback = generate_feedback(structure, complexity, smells)
    score, breakdown = calculate_score(complexity, smells)

    print("[bold green]RealityCheck Report:[/bold green]\n")

    # 🔥 Score first (important UX)
    print(f"[bold cyan]Code Quality Score:[/bold cyan] {score}/10\n")

    print("[bold blue]Breakdown:[/bold blue]")
    for key, value in breakdown.items():
        print(f"{key.capitalize()}: {value}/10")

    print("\n[bold yellow]Feedback:[/bold yellow]")
    for item in feedback:
        print(item)

if __name__ == "__main__":
    main()