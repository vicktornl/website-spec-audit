import asyncio

import click

from website_spec_audit.models import TopicStatus
from website_spec_audit.output import render_report
from website_spec_audit.registry import registry
from website_spec_audit.runner import AuditRunner

import website_spec_audit.validators  # noqa: F401


@click.command()
@click.argument("url")
@click.option(
    "--category",
    "-c",
    multiple=True,
    help="Filter by category (can be repeated). E.g. -c security -c seo",
)
@click.option(
    "--status",
    "-s",
    multiple=True,
    type=click.Choice(["required", "recommended", "optional", "avoid"], case_sensitive=False),
    help="Filter by topic status level. E.g. -s required",
)
@click.option(
    "--topic",
    "-t",
    multiple=True,
    help="Run only specific topics by slug. E.g. -t hsts -t robots-txt",
)
@click.option("--verbose", "-v", is_flag=True, help="Show detailed check output")
@click.option("--concurrency", default=10, help="Max concurrent HTTP requests")
@click.version_option()
def main(url: str, category: tuple, status: tuple, topic: tuple, verbose: bool, concurrency: int):
    """Audit a website against specification.website."""
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"

    categories = list(category) if category else None
    statuses = [TopicStatus(s.lower()) for s in status] if status else None
    slugs = list(topic) if topic else None

    validators = registry.filter(categories=categories, statuses=statuses, slugs=slugs)

    if not validators:
        click.echo("No validators match the given filters.", err=True)
        raise SystemExit(1)

    runner = AuditRunner(validators=validators, concurrency=concurrency)
    report = asyncio.run(runner.run(url))
    render_report(report, verbose=verbose)
