from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class CacheControlValidator(BaseValidator):
    slug = "cache-control"
    title = "Cache-Control headers"
    category = "performance"
    status = TopicStatus.REQUIRED
    spec_url = "https://specification.website/spec/performance/cache-control/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/")
        cache_control = resource.headers.get("cache-control")

        if not cache_control:
            return self.fail_result("Missing Cache-Control response header.")

        cc_lower = cache_control.lower()
        details: list[str] = [f"Cache-Control: {cache_control}"]

        if "no-store" in cc_lower:
            return self.warn_result(
                "Cache-Control header is set to no-store. "
                "This is acceptable for dynamic HTML but prevents all caching.",
                details=details,
            )

        if "no-cache" in cc_lower and "max-age" not in cc_lower:
            return self.warn_result(
                "Cache-Control uses no-cache without max-age. "
                "The browser will revalidate on every request.",
                details=details,
            )

        return self.pass_result(
            f"Cache-Control header is present: {cache_control}"
        )
