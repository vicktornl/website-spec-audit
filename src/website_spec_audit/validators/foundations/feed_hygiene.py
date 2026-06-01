from urllib.parse import urljoin

from lxml import etree

from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus

FEED_TYPES = {
    "application/rss+xml",
    "application/atom+xml",
    "application/feed+json",
}


class FeedHygieneValidator(BaseValidator):
    slug = "feed-hygiene"
    title = "Feed content hygiene"
    category = "foundations"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/foundations/feed-hygiene/"

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")
        alternates = doc.cssselect('link[rel="alternate"]')

        feed_links: list[tuple[str, str]] = []
        for link in alternates:
            link_type = (link.get("type") or "").strip().lower()
            if link_type in FEED_TYPES:
                href = link.get("href", "").strip()
                if href:
                    feed_links.append((href, link_type))

        if not feed_links:
            return self.skip_result("No feed link found in HTML; nothing to check.")

        errors: list[str] = []
        checked = 0

        for href, feed_type in feed_links:
            full_url = urljoin(context.url, href)
            try:
                resource = await context.fetch(href)
            except Exception as exc:
                errors.append(f"Failed to fetch {full_url}: {exc}")
                continue

            if resource.status_code != 200:
                errors.append(f"{full_url} returned HTTP {resource.status_code}.")
                continue

            checked += 1

            if feed_type == "application/feed+json":
                import json

                try:
                    json.loads(resource.text)
                except (json.JSONDecodeError, ValueError) as exc:
                    errors.append(f"{full_url} is not valid JSON: {exc}")
            else:
                try:
                    etree.fromstring(resource.text.encode("utf-8"))
                except etree.XMLSyntaxError as exc:
                    errors.append(f"{full_url} is not valid XML: {exc}")

        if errors:
            return self.fail_result(
                f"Feed hygiene issues found ({len(errors)}).",
                details=errors,
            )

        return self.pass_result(f"All {checked} discovered feed(s) are well-formed.")
