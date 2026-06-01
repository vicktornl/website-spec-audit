from urllib.parse import urlparse

from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class RedirectsValidator(BaseValidator):
    slug = "redirects"
    title = "Redirects (301/302/308)"
    category = "seo"
    status = TopicStatus.REQUIRED
    spec_url = "https://specification.website/spec/seo/redirects/"

    async def validate(self, context: AuditContext) -> CheckResult:
        parsed = urlparse(context.url)

        # Only test HTTP->HTTPS redirect if the target is already HTTPS
        if parsed.scheme != "https":
            return self.skip_result("Target URL is not HTTPS; cannot test HTTP-to-HTTPS redirect.")

        http_url = f"http://{parsed.netloc}{parsed.path}"
        try:
            resource = await context.fetch(http_url, follow_redirects=False)
        except Exception as exc:
            return self.warn_result(
                "Could not connect to HTTP version of the URL.",
                details=[str(exc)],
            )

        if resource.status_code in (301, 308):
            location = resource.headers.get("location", "")
            if location.startswith("https://"):
                return self.pass_result(
                    f"HTTP request returns {resource.status_code} redirect to HTTPS ({location})."
                )
            return self.warn_result(
                f"HTTP returns {resource.status_code} but Location does not point to HTTPS.",
                details=[f"Location: {location}"],
            )

        if resource.status_code in (302, 307):
            location = resource.headers.get("location", "")
            return self.warn_result(
                f"HTTP returns temporary redirect ({resource.status_code}); a permanent redirect (301/308) is preferred.",
                details=[f"Location: {location}"],
            )

        return self.fail_result(
            f"HTTP request returned {resource.status_code} instead of a redirect to HTTPS.",
        )
