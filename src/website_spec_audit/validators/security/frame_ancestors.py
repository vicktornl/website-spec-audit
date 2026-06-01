from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class FrameAncestorsValidator(BaseValidator):
    slug = "frame-ancestors"
    title = "Clickjacking protection (frame-ancestors / X-Frame-Options)"
    category = "security"
    status = TopicStatus.REQUIRED
    spec_url = "https://specification.website/spec/security/frame-ancestors/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/")

        # Prefer CSP frame-ancestors
        csp = resource.headers.get("content-security-policy", "")
        has_frame_ancestors = False

        for part in csp.split(";"):
            directive = part.strip().lower()
            if directive.startswith("frame-ancestors"):
                has_frame_ancestors = True
                break

        if has_frame_ancestors:
            return self.pass_result(
                "CSP frame-ancestors directive is set (preferred method)."
            )

        # Fall back to X-Frame-Options
        xfo = resource.headers.get("x-frame-options")

        if xfo:
            xfo_upper = xfo.strip().upper()
            if xfo_upper in ("DENY", "SAMEORIGIN"):
                return self.pass_result(
                    f"X-Frame-Options is set to '{xfo_upper}' (consider migrating to CSP frame-ancestors)."
                )
            return self.warn_result(
                f"X-Frame-Options is set to '{xfo}', which may not be well-supported.",
            )

        return self.fail_result(
            "No clickjacking protection found. Set CSP frame-ancestors or X-Frame-Options."
        )
