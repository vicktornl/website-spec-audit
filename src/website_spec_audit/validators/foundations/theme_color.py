from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class ThemeColorValidator(BaseValidator):
    slug = "theme-color"
    title = '<meta name="theme-color">'
    category = "foundations"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/foundations/theme-color/"

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")
        meta = doc.cssselect('meta[name="theme-color"]')

        if not meta:
            return self.fail_result("No <meta name=\"theme-color\"> found.")

        content = meta[0].get("content", "").strip()
        if not content:
            return self.fail_result("Theme-color meta tag has an empty content attribute.")

        return self.pass_result(f"Theme color found: {content}")
