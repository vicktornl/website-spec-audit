from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class Http3Validator(BaseValidator):
    slug = "http3"
    title = "HTTP/2 and HTTP/3"
    category = "performance"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/performance/http3/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/")
        alt_svc = resource.headers.get("alt-svc", "")

        details: list[str] = []

        if alt_svc:
            details.append(f"Alt-Svc: {alt_svc}")

        if "h3" in alt_svc.lower():
            return self.pass_result(
                "HTTP/3 support advertised via Alt-Svc header.",
            )

        if alt_svc:
            return self.warn_result(
                "Alt-Svc header present but does not advertise HTTP/3 (h3).",
                details=details,
            )

        return self.warn_result(
            "No Alt-Svc header found. HTTP/3 support could not be confirmed. "
            "Note: HTTP/2 is likely in use but cannot be verified via response headers alone."
        )
