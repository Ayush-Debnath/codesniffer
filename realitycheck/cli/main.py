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
from realitycheck.analyzers.performance import analyze_performance
from realitycheck.analyzers.security import analyze_security
from realitycheck.core.aggregator import aggregate_project, generate_project_insights
from realitycheck.analyzers.ai_project import get_project_ai_insights


@click.group()
def main():
    """RealityCheck AI - Code Honesty Detector"""
    pass




def process_file(file_path):

    # 📄 Read file content
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
    except Exception as e:
        print(f"[red]Error reading {file_path}:[/red] {str(e)}")
        return None

    # 🌳 Parse AST
    tree = parse_file(file_path)

    if isinstance(tree, dict) and "error" in tree:
        print(f"[red]Syntax Error in {file_path}:[/red] {tree['error']}")
        return None

    # 🧠 Run analyzers
    structure = extract_structure(tree)
    complexity = analyze_complexity(tree)
    smells = analyze_code_smells(tree)
    performance_issues = analyze_performance(tree)
    security_issues = analyze_security(tree)

    # 🧾 Generate rule-based feedback
    feedback = generate_feedback(structure, complexity, smells)

    # ⚡ Add performance insights
    feedback.extend(performance_issues)
    feedback.extend(security_issues)

    # 📊 Score calculation
    score, breakdown = calculate_score(complexity, smells)

    # 🤖 AI feedback
    ai_feedback = get_ai_feedback(code)

    # 🎨 Display report
    display_report(score, breakdown, feedback, ai_feedback)

    # 📦 Return for aggregation (project-level)
    return {
        "file": file_path,
        "score": score,
        "issues": len(feedback) + len(ai_feedback)
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
        summary = aggregate_project(results)
        insights = generate_project_insights(results)

        print("\n[bold magenta]📁 Project Summary:[/bold magenta]")
        print(f"Files analyzed: {summary['total_files']}")
        print(f"Average Score: {summary['avg_score']}/10")
        print(f"Worst File: {summary['worst_file']}")
        print(f"Total Issues: {summary['total_issues']}")

        print("\n[bold yellow]🧠 Project Insights:[/bold yellow]")
        for insight in insights:
            print(f"• {insight}")
    
    project_ai = get_project_ai_insights(summary, results)

    print("\n[bold magenta]🤖 AI Project Review:[/bold magenta]")
    for item in project_ai:
        print(f"• {item}")


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