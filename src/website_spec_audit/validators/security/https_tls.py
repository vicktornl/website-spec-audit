from urllib.parse import urlparse

from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class HttpsTlsValidator(BaseValidator):
    slug = "https-tls"
    title = "HTTPS and TLS"
    category = "security"
    status = TopicStatus.REQUIRED
    spec_url = "https://specification.website/spec/security/https-tls/"

    async def validate(self, context: AuditContext) -> CheckResult:
        parsed = urlparse(context.url)

        if parsed.scheme != "https":
            return self.fail_result("Site URL does not use HTTPS.")

        # Check if HTTP redirects to HTTPS
        http_url = context.url.replace("https://", "http://", 1)
        details: list[str] = []

        try:
            http_resource = await context.fetch(http_url, follow_redirects=True)

            if http_resource.is_redirect and http_resource.redirect_url:
                redirect_parsed = urlparse(http_resource.redirect_url)
                if redirect_parsed.scheme == "https":
                    details.append("HTTP redirects to HTTPS.")
                else:
                    details.append(
                        f"HTTP redirects to {http_resource.redirect_url} (not HTTPS)."
                    )
            else:
                details.append("HTTP does not redirect to HTTPS.")
        except Exception:
            details.append("Could not verify HTTP-to-HTTPS redirect.")

        return self.pass_result("Site is served over HTTPS.")
