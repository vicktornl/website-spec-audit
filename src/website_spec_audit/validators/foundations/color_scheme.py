from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus

VALID_SCHEMES = {"light", "dark", "light dark", "dark light"}


class ColorSchemeValidator(BaseValidator):
    slug = "color-scheme"
    title = '<meta name="color-scheme">'
    category = "foundations"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/foundations/color-scheme/"

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")
        meta = doc.cssselect('meta[name="color-scheme"]')

        if not meta:
            return self.fail_result("No <meta name=\"color-scheme\"> found.")

        content = meta[0].get("content", "").strip()
        if not content:
            return self.fail_result("Color-scheme meta tag has an empty content attribute.")

        normalised = " ".join(content.lower().split())
        if normalised not in VALID_SCHEMES:
            return self.warn_result(
                f"Unexpected color-scheme value: \"{content}\".",
                details=[f"Expected one of: {', '.join(sorted(VALID_SCHEMES))}"],
            )

        return self.pass_result(f"Color scheme found: {content}")
