from urllib.parse import urlparse

from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class InternalLinkingValidator(BaseValidator):
    slug = "internal-linking"
    title = "Internal linking"
    category = "seo"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/seo/internal-linking/"

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")
        target_host = urlparse(context.url).netloc.lower()

        internal_links: list[str] = []
        for anchor in doc.iter("a"):
            href = (anchor.get("href") or "").strip()
            if not href or href.startswith("#"):
                continue

            parsed = urlparse(href)

            # Relative links are internal
            if not parsed.netloc:
                internal_links.append(href)
                continue

            # Absolute links on the same host
            if parsed.netloc.lower() == target_host:
                internal_links.append(href)

        count = len(internal_links)

        if count == 0:
            return self.fail_result("No internal links found on the page.")

        if count < 3:
            return self.warn_result(
                f"Only {count} internal link(s) found; consider adding more for better crawlability.",
            )

        return self.pass_result(f"{count} internal links found on the page.")
