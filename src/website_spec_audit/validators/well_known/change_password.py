from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class ChangePasswordValidator(BaseValidator):
    slug = "change-password"
    title = "/.well-known/change-password"
    category = "well-known"
    status = TopicStatus.OPTIONAL
    spec_url = "https://specification.website/spec/well-known/change-password/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch(
            "/.well-known/change-password", follow_redirects=False
        )

        if resource.status_code == 404:
            return self.skip_result(
                "/.well-known/change-password not found (HTTP 404)."
            )

        if resource.status_code in (301, 302, 307, 308):
            location = resource.headers.get("location", "")
            return self.pass_result(
                f"/.well-known/change-password redirects ({resource.status_code}) to {location}."
            )

        return self.fail_result(
            f"/.well-known/change-password returned HTTP {resource.status_code}; "
            "expected a redirect (301/302/307/308)."
        )
