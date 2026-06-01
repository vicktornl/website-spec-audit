from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class HstsValidator(BaseValidator):
    slug = "hsts"
    title = "HSTS (Strict-Transport-Security)"
    category = "security"
    status = TopicStatus.REQUIRED
    spec_url = "https://specification.website/spec/security/hsts/"

    MIN_MAX_AGE = 31536000  # 1 year in seconds

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/")
        hsts = resource.headers.get("strict-transport-security")

        if not hsts:
            return self.fail_result("Missing Strict-Transport-Security header.")

        hsts_lower = hsts.lower()
        directives = [d.strip() for d in hsts_lower.split(";")]

        # Parse max-age
        max_age = None
        for directive in directives:
            if directive.startswith("max-age"):
                try:
                    max_age = int(directive.split("=", 1)[1].strip())
                except (IndexError, ValueError):
                    return self.fail_result("Invalid max-age value in HSTS header.")

        if max_age is None:
            return self.fail_result("HSTS header missing max-age directive.")

        warnings: list[str] = []

        if max_age < self.MIN_MAX_AGE:
            warnings.append(
                f"max-age is {max_age}, should be at least {self.MIN_MAX_AGE} (1 year)."
            )

        has_include_subdomains = any(
            d == "includesubdomains" for d in directives
        )
        has_preload = any(d == "preload" for d in directives)

        if not has_include_subdomains:
            warnings.append("Missing includeSubDomains directive.")

        if not has_preload:
            warnings.append("Missing preload directive.")

        if warnings:
            return self.warn_result(
                "HSTS header present but could be improved.", details=warnings
            )

        return self.pass_result(
            f"HSTS header is well-configured (max-age={max_age}, includeSubDomains, preload)."
        )
