from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus

FEED_TYPES = {
    "application/rss+xml",
    "application/atom+xml",
    "application/feed+json",
}


class FeedDiscoveryValidator(BaseValidator):
    slug = "feed-discovery"
    title = 'Feed discovery with rel="alternate"'
    category = "foundations"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/foundations/feed-discovery/"

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")
        alternates = doc.cssselect('link[rel="alternate"]')

        feeds: list[str] = []
        for link in alternates:
            link_type = (link.get("type") or "").strip().lower()
            if link_type in FEED_TYPES:
                href = link.get("href", "").strip()
                title = link.get("title", "").strip()
                label = title if title else href
                feeds.append(f"{link_type}: {label}")

        if not feeds:
            return self.skip_result("No feed link found; site may not provide feeds.")

        return self.pass_result(
            f"Found {len(feeds)} feed(s) via rel=\"alternate\".",
        )
