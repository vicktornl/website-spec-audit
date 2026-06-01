from rich.console import Console
from rich.text import Text

from website_spec_audit.models import AuditReport, CheckStatus

STATUS_MARKERS = {
    CheckStatus.PASS: ("[x]", "green"),
    CheckStatus.FAIL: ("[ ]", "red"),
    CheckStatus.WARN: ("[~]", "yellow"),
    CheckStatus.SKIP: ("[-]", "dim"),
}

CATEGORY_LABELS = {
    "foundations": "Foundations",
    "seo": "SEO",
    "accessibility": "Accessibility",
    "security": "Security",
    "well-known": "Well-Known URIs",
    "agent-readiness": "Agent Readiness",
    "performance": "Performance",
    "privacy": "Privacy",
    "resilience": "Resilience",
    "i18n": "Internationalisation",
}


def render_report(report: AuditReport, verbose: bool = False) -> None:
    console = Console()
    console.print()
    console.print(f"[bold]Audit: {report.url}[/bold]")
    console.print()

    for cat_result in report.categories:
        label = CATEGORY_LABELS.get(cat_result.category, cat_result.category)
        console.print(f"[bold underline]{label}[/bold underline] ({cat_result.passed}/{cat_result.total})")
        console.print()

        for result in cat_result.results:
            marker, color = STATUS_MARKERS[result.check_status]
            status_label = f"({result.topic.status.value})"

            line = Text()
            line.append(f"  {marker} ", style=color)
            line.append(f"{result.topic.title}", style="bold")
            line.append(f" {status_label}", style="dim italic")
            line.append(f" — {result.message}", style=color)
            console.print(line)

            if verbose and result.details:
                for detail in result.details:
                    console.print(f"       {detail}", style="dim")

        console.print()

    console.print(f"[bold]Total: {report.total_passed}/{report.total_checks} passed[/bold]")
    console.print()
