from urllib.parse import urljoin

from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class MarkdownSourceEndpointsValidator(BaseValidator):
    slug = "markdown-source-endpoints"
    title = "Per-page Markdown source endpoints"
    category = "agent-readiness"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/agent-readiness/markdown-source-endpoints/"

    async def validate(self, context: AuditContext) -> CheckResult:
        details: list[str] = []
        found = False

        # Check if appending .md to the URL returns markdown content
        url = context.url.rstrip("/")
        md_path = url + ".md"
        # Build the relative path from the full URL
        from urllib.parse import urlparse

        parsed = urlparse(context.url)
        path = parsed.path.rstrip("/") or ""
        md_relative = path + ".md" if path else "/.md"

        resource = await context.fetch(md_relative)
        if resource.status_code == 200:
            content_type = resource.headers.get("content-type", "")
            if resource.text.strip():
                details.append(f"{md_relative} returned 200 ({content_type}).")
                found = True

        # Check content-type negotiation via Accept: text/markdown header
        # We fetch the main page and check if there's a Link header pointing to markdown
        main_resource = await context.fetch("/")
        link_header = main_resource.headers.get("link", "")
        if "text/markdown" in link_header:
            details.append("Link header references text/markdown alternate.")
            found = True

        if found:
            return self.pass_result(
                "Markdown source endpoints detected.", details=details
            )

        return self.fail_result(
            "No Markdown source endpoints found. "
            "Try serving .md versions of pages or supporting Accept: text/markdown."
        )
