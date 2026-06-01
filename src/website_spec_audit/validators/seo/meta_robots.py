from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class MetaRobotsValidator(BaseValidator):
    slug = "meta-robots"
    title = "Meta robots and X-Robots-Tag"
    category = "seo"
    status = TopicStatus.REQUIRED
    spec_url = "https://specification.website/spec/seo/meta-robots/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/")
        doc = await context.fetch_html("/")
        details: list[str] = []

        # Check <meta name="robots"> tag
        meta_tags = doc.cssselect('meta[name="robots"]')
        meta_content = ""
        if meta_tags:
            meta_content = meta_tags[0].get("content", "").lower()
            details.append(f'<meta name="robots" content="{meta_content}">')

        # Check X-Robots-Tag header
        x_robots = resource.headers.get("x-robots-tag", "").lower()
        if x_robots:
            details.append(f"X-Robots-Tag: {x_robots}")

        # Warn if noindex is present on what should be a public page
        has_noindex = "noindex" in meta_content or "noindex" in x_robots

        if has_noindex:
            return self.warn_result(
                "Page is marked as noindex; search engines will not index this page.",
                details=details,
            )

        if not meta_tags and not x_robots:
            return self.pass_result(
                "No restrictive robots directives found (page is indexable by default)."
            )

        return self.pass_result(
            f"Robots directives found and page is indexable. {'; '.join(details)}"
        )
