from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def display_report(score, breakdown, feedback):
    
    # 🔥 Title Panel
    console.print(Panel.fit("🚨 RealityCheck Report", style="bold red"))

    # 🎯 Score
    console.print(f"\n[bold cyan]Code Quality Score:[/bold cyan] {score}/10\n")

    # 📊 Breakdown Table
    table = Table(title="Breakdown")

    table.add_column("Metric", style="bold blue")
    table.add_column("Score", style="bold green")

    for key, value in breakdown.items():
        table.add_row(key.capitalize(), f"{value}/10")

    console.print(table)

    # ⚠️ Feedback
    console.print("\n[bold yellow]Feedback:[/bold yellow]")
    for item in feedback:
        console.print(f"• {item}")