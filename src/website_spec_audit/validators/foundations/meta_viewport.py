from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class MetaViewportValidator(BaseValidator):
    slug = "meta-viewport"
    title = "<meta viewport>"
    category = "foundations"
    status = TopicStatus.REQUIRED
    spec_url = "https://specification.website/spec/foundations/meta-viewport/"

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")
        meta = doc.cssselect('meta[name="viewport"]')

        if not meta:
            return self.fail_result("No <meta name=\"viewport\"> found.")

        content = meta[0].get("content", "")
        if not content:
            return self.fail_result("Viewport meta tag has no content attribute.")

        content_lower = content.lower().replace(" ", "")

        if "width=device-width" not in content_lower:
            return self.fail_result(
                "Viewport meta tag is missing width=device-width.",
                details=[f'Found content="{content}"'],
            )

        warnings: list[str] = []
        if "user-scalable=no" in content_lower:
            warnings.append("user-scalable=no disables pinch-to-zoom.")
        if "maximum-scale=1" in content_lower:
            warnings.append("maximum-scale=1 prevents zooming.")

        if warnings:
            return self.warn_result(
                "Viewport meta tag found but may restrict accessibility.",
                details=warnings,
            )

        return self.pass_result("Valid viewport meta tag found.")
