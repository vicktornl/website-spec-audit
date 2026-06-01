from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class WebfingerValidator(BaseValidator):
    slug = "webfinger"
    title = "/.well-known/webfinger"
    category = "well-known"
    status = TopicStatus.OPTIONAL
    spec_url = "https://specification.website/spec/well-known/webfinger/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/.well-known/webfinger")

        if resource.status_code == 404:
            return self.skip_result(
                "/.well-known/webfinger not found (HTTP 404)."
            )

        if resource.status_code in (200, 400):
            return self.pass_result(
                f"/.well-known/webfinger is reachable (HTTP {resource.status_code})."
            )

        return self.fail_result(
            f"/.well-known/webfinger returned HTTP {resource.status_code}; "
            "expected 200 or 400."
        )
