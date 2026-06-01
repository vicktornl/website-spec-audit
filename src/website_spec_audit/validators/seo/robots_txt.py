from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class RobotsTxtValidator(BaseValidator):
    slug = "robots-txt"
    title = "robots.txt"
    category = "seo"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/seo/robots-txt/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/robots.txt")

        if resource.status_code != 200:
            return self.fail_result(
                f"/robots.txt returned HTTP {resource.status_code}.",
            )

        content_type = resource.headers.get("content-type", "")
        if "text/plain" not in content_type:
            return self.warn_result(
                "robots.txt served with unexpected Content-Type.",
                details=[f"Content-Type: {content_type}"],
            )

        details: list[str] = []
        has_sitemap = False
        for line in resource.text.splitlines():
            stripped = line.strip()
            if stripped.lower().startswith("sitemap:"):
                has_sitemap = True
                details.append(stripped)

        if not has_sitemap:
            return self.warn_result(
                "robots.txt found but contains no Sitemap: directive.",
            )

        return self.pass_result(
            f"robots.txt found with Sitemap directive(s): {', '.join(details)}"
        )
