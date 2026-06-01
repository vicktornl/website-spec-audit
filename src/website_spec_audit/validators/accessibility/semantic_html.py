from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class SemanticHtmlValidator(BaseValidator):
    slug = "semantic-html"
    title = "Semantic HTML and landmarks"
    category = "accessibility"
    status = TopicStatus.REQUIRED
    spec_url = "https://specification.website/spec/accessibility/semantic-html/"

    LANDMARKS = ["header", "nav", "main", "footer"]

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")

        found: list[str] = []
        missing: list[str] = []

        for tag in self.LANDMARKS:
            elements = doc.cssselect(tag)
            if elements:
                found.append(f"<{tag}> found ({len(elements)}).")
            else:
                missing.append(f"<{tag}> is missing.")

        if missing:
            return self.fail_result(
                f"{len(missing)} landmark element(s) missing.",
                details=missing + found,
            )

        return self.pass_result(
            "All landmark elements found (header, nav, main, footer)."
        )
