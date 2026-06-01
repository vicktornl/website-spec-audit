from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class ContentSecurityPolicyValidator(BaseValidator):
    slug = "content-security-policy"
    title = "Content Security Policy (CSP)"
    category = "security"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/security/content-security-policy/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/")
        csp = resource.headers.get("content-security-policy")

        if not csp:
            return self.fail_result("Missing Content-Security-Policy header.")

        warnings: list[str] = []

        # Parse directives
        directives: dict[str, str] = {}
        for part in csp.split(";"):
            part = part.strip()
            if not part:
                continue
            tokens = part.split(None, 1)
            name = tokens[0].lower()
            value = tokens[1] if len(tokens) > 1 else ""
            directives[name] = value

        # Check script-src (or default-src as fallback)
        script_src = directives.get("script-src", directives.get("default-src", ""))

        if "'unsafe-inline'" in script_src:
            warnings.append("script-src contains 'unsafe-inline'.")

        if "'unsafe-eval'" in script_src:
            warnings.append("script-src contains 'unsafe-eval'.")

        if warnings:
            return self.warn_result(
                "Content-Security-Policy header present but has unsafe directives.",
                details=warnings,
            )

        return self.pass_result("Content-Security-Policy header is present.")
