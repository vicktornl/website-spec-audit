from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus

ALTERNATE_TYPES = [
    "application/json",
    "application/feed+json",
    "application/rss+xml",
    "application/atom+xml",
    "application/xml",
    "text/xml",
]


class MachineReadableFormatsValidator(BaseValidator):
    slug = "machine-readable-formats"
    title = "Machine-readable formats"
    category = "agent-readiness"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/agent-readiness/machine-readable-formats/"

    async def validate(self, context: AuditContext) -> CheckResult:
        details: list[str] = []

        # Check HTML for alternate links
        doc = await context.fetch_html("/")
        links = doc.cssselect("link[rel='alternate']")
        for link in links:
            link_type = link.get("type", "")
            href = link.get("href", "")
            if link_type.lower() in ALTERNATE_TYPES:
                details.append(
                    f"<link rel=\"alternate\" type=\"{link_type}\" href=\"{href}\">"
                )

        # Check for RSS/Atom feed links
        feed_links = doc.cssselect(
            "link[type='application/rss+xml'], link[type='application/atom+xml']"
        )
        for link in feed_links:
            rel = link.get("rel", "")
            if rel != "alternate":
                href = link.get("href", "")
                link_type = link.get("type", "")
                details.append(
                    f"<link rel=\"{rel}\" type=\"{link_type}\" href=\"{href}\">"
                )

        # Check Link HTTP headers for alternate formats
        resource = await context.fetch("/")
        link_header = resource.headers.get("link", "")
        if link_header:
            for part in link_header.split(","):
                part_lower = part.lower()
                if "rel=" in part_lower and (
                    "alternate" in part_lower
                    or any(t in part_lower for t in ALTERNATE_TYPES)
                ):
                    details.append(f"Link header: {part.strip()}")

        if details:
            return self.pass_result(
                f"Found {len(details)} machine-readable format reference(s).",
                details=details,
            )

        return self.fail_result(
            "No machine-readable alternate formats found. "
            "Consider adding RSS/Atom feeds or JSON alternate links."
        )
