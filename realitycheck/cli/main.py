import os
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




def process_file(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    tree = parse_file(file_path)

    if isinstance(tree, dict) and "error" in tree:
        print(f"[red]Syntax Error in {file_path}:[/red] {tree['error']}")
        return None

    structure = extract_structure(tree)
    complexity = analyze_complexity(tree)
    smells = analyze_code_smells(tree)

    feedback = generate_feedback(structure, complexity, smells)
    score, breakdown = calculate_score(complexity, smells)
    ai_feedback = get_ai_feedback(code)

    display_report(score, breakdown, feedback, ai_feedback)

    return {
        "file": file_path,
        "score": score
    }


def process_folder(folder_path):
    print(f"[bold cyan]Analyzing project:[/bold cyan] {folder_path}\n")

    results = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)

                print(f"\n[bold green]File:[/bold green] {full_path}")
                result = process_file(full_path)

                if result:
                    results.append(result)

    # 📊 PROJECT SUMMARY
    if results:
        avg_score = sum(r["score"] for r in results) / len(results)
        worst_file = min(results, key=lambda x: x["score"])

        print("\n[bold magenta]📁 Project Summary:[/bold magenta]")
        print(f"Files analyzed: {len(results)}")
        print(f"Average Score: {round(avg_score, 2)}/10")
        print(f"Worst File: {worst_file['file']} ({worst_file['score']}/10)")


@main.command()
@click.argument("path")
def analyze(path):

    if not os.path.exists(path):
        print("[red]Error: Path does not exist[/red]")
        return

    # 📄 SINGLE FILE MODE
    if os.path.isfile(path):
        process_file(path)

    # 📁 FOLDER MODE
    elif os.path.isdir(path):
        process_folder(path)

if __name__ == "__main__":
    main()