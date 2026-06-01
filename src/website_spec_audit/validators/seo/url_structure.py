import re
from urllib.parse import urlparse

from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class UrlStructureValidator(BaseValidator):
    slug = "url-structure"
    title = "URL structure"
    category = "seo"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/seo/url-structure/"

    async def validate(self, context: AuditContext) -> CheckResult:
        parsed = urlparse(context.url)
        path = parsed.path
        issues: list[str] = []

        if parsed.netloc != parsed.netloc.lower():
            issues.append(f"Hostname contains uppercase characters: {parsed.netloc}")

        if path != path.lower():
            issues.append(f"Path contains uppercase characters: {path}")

        if "_" in path:
            issues.append("Path contains underscores; hyphens are preferred for word separation.")

        if re.search(r"//+", path):
            issues.append("Path contains consecutive slashes.")

        # Trailing slash: paths other than "/" should be consistent
        if len(path) > 1 and path.endswith("/"):
            issues.append("Path has a trailing slash; consider removing it for consistency.")

        if issues:
            return self.warn_result(
                "URL structure issues detected.",
                details=issues,
            )

        return self.pass_result("URL structure follows best practices (lowercase, hyphens, clean path).")
