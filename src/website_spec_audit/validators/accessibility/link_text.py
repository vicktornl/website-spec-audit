from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class LinkTextValidator(BaseValidator):
    slug = "link-text"
    title = "Descriptive link text"
    category = "accessibility"
    status = TopicStatus.REQUIRED
    spec_url = "https://specification.website/spec/accessibility/link-text/"

    VAGUE_TEXTS = {
        "click here",
        "here",
        "read more",
        "more",
        "learn more",
        "link",
        "this",
        "this link",
        "go",
        "details",
        "more details",
        "more info",
        "info",
    }

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")

        links = doc.cssselect("a")

        if not links:
            return self.pass_result("No links found.")

        vague: list[str] = []
        for link in links:
            text = (link.text_content() or "").strip().lower()
            if text in self.VAGUE_TEXTS:
                href = link.get("href", "")
                vague.append(
                    f'Link with text "{text}" (href="{href}") is not descriptive.'
                )

        if vague:
            return self.warn_result(
                f"{len(vague)} link(s) with vague or non-descriptive text.",
                details=vague,
            )

        return self.pass_result(
            f"All {len(links)} link(s) have descriptive text."
        )
