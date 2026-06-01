from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class CanonicalUrlValidator(BaseValidator):
    slug = "canonical-url"
    title = 'Canonical URL (rel="canonical")'
    category = "foundations"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/foundations/canonical-url/"

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")
        links = doc.cssselect('link[rel="canonical"]')

        if not links:
            return self.fail_result("No <link rel=\"canonical\"> found.")

        href = links[0].get("href", "").strip()
        if not href:
            return self.fail_result("Canonical link has an empty href attribute.")

        if not href.startswith(("http://", "https://")):
            return self.warn_result(
                "Canonical URL is relative; an absolute URL is recommended.",
                details=[f'Found href="{href}"'],
            )

        return self.pass_result(f"Canonical URL found: {href}")
