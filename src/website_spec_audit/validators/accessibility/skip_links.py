from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class SkipLinksValidator(BaseValidator):
    slug = "skip-links"
    title = "Skip links"
    category = "accessibility"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/accessibility/skip-links/"

    SKIP_TARGETS = {"main", "content", "main-content", "maincontent", "skip"}

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")

        body = doc.cssselect("body")
        if not body:
            return self.fail_result("No <body> element found.")

        # Look for anchor links early in the body that point to a fragment
        all_links = body[0].cssselect("a[href]")

        # Only consider the first 10 links in the body as "early"
        early_links = all_links[:10]

        skip_link_found = False
        target_id = None

        for link in early_links:
            href = (link.get("href") or "").strip()
            if href.startswith("#") and len(href) > 1:
                fragment = href[1:].lower()
                if fragment in self.SKIP_TARGETS:
                    skip_link_found = True
                    target_id = href[1:]
                    break

        if not skip_link_found:
            return self.warn_result(
                "No skip link found early in the document."
            )

        # Verify the target exists
        main_elements = doc.cssselect("main")
        target_elements = doc.cssselect(f'#{target_id}') if target_id else []

        if main_elements or target_elements:
            return self.pass_result(
                f'Skip link found pointing to "#{target_id}" with a matching target.'
            )

        return self.warn_result(
            f'Skip link points to "#{target_id}" but no matching element found.',
        )
