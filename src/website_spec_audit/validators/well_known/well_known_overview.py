from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class WellKnownOverviewValidator(BaseValidator):
    slug = "well-known-overview"
    title = "Well-known URIs"
    category = "well-known"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/well-known/well-known-overview/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/.well-known/")

        if resource.status_code in (200, 403):
            return self.pass_result(
                f"/.well-known/ is reachable (HTTP {resource.status_code})."
            )

        return self.fail_result(
            f"/.well-known/ returned HTTP {resource.status_code}; expected 200 or 403."
        )
