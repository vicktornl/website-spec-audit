from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class ImageAltTextValidator(BaseValidator):
    slug = "image-alt-text"
    title = "Image alt text"
    category = "accessibility"
    status = TopicStatus.REQUIRED
    spec_url = "https://specification.website/spec/accessibility/image-alt-text/"

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")

        images = doc.cssselect("img")

        if not images:
            return self.pass_result("No <img> elements found.")

        missing_alt: list[str] = []
        for img in images:
            if img.get("alt") is None:
                src = img.get("src", "(unknown src)")
                missing_alt.append(f'<img src="{src}"> is missing an alt attribute.')

        if missing_alt:
            return self.fail_result(
                f"{len(missing_alt)} image(s) missing alt attribute.",
                details=missing_alt,
            )

        return self.pass_result(
            f"All {len(images)} image(s) have an alt attribute."
        )
