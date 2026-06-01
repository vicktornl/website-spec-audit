from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class NlwebValidator(BaseValidator):
    slug = "nlweb"
    title = "NLWeb \u2014 conversational interface discovery"
    category = "agent-readiness"
    status = TopicStatus.OPTIONAL
    spec_url = "https://specification.website/spec/agent-readiness/nlweb/"

    async def validate(self, context: AuditContext) -> CheckResult:
        details: list[str] = []

        # Check HTML for <link rel="nlweb">
        doc = await context.fetch_html("/")
        nlweb_links = doc.cssselect('link[rel="nlweb"]')
        if nlweb_links:
            for link in nlweb_links:
                href = link.get("href", "")
                details.append(f'<link rel="nlweb" href="{href}">')

        # Check Link header for rel="nlweb"
        resource = await context.fetch("/")
        link_header = resource.headers.get("link", "")
        if link_header:
            for part in link_header.split(","):
                part_lower = part.lower()
                if "nlweb" in part_lower:
                    details.append(f"Link header: {part.strip()}")

        if details:
            return self.pass_result(
                "NLWeb discovery endpoint found.", details=details
            )

        return self.skip_result("No NLWeb discovery (rel=\"nlweb\") found.")
