import click
from rich import print
from realitycheck.parser.ast_parser import parse_file, extract_structure
from realitycheck.analyzers.complexity import analyze_complexity
from realitycheck.analyzers.code_smells import analyze_code_smells

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

    print("[bold green]Structure:[/bold green]")
    print(structure)

    print("\n[bold yellow]Complexity Analysis:[/bold yellow]")
    print(complexity)

    print("\n[bold red]Code Smells:[/bold red]")
    print(smells)


if __name__ == "__main__":
    main()