from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class Soft404Validator(BaseValidator):
    slug = "soft-404"
    title = "Soft 404s"
    category = "seo"
    status = TopicStatus.AVOID
    spec_url = "https://specification.website/spec/seo/soft-404/"

    NON_EXISTENT_PATH = "/this-page-does-not-exist-spec-audit-test"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch(self.NON_EXISTENT_PATH)

        if resource.status_code == 404:
            return self.pass_result("Non-existent page correctly returns HTTP 404.")

        if resource.status_code == 410:
            return self.pass_result("Non-existent page returns HTTP 410 Gone (acceptable).")

        if resource.status_code == 200:
            return self.fail_result(
                "Non-existent page returns HTTP 200 instead of 404 (soft 404 detected).",
                details=[f"Tested path: {self.NON_EXISTENT_PATH}"],
            )

        return self.warn_result(
            f"Non-existent page returns unexpected status {resource.status_code}.",
            details=[f"Tested path: {self.NON_EXISTENT_PATH}"],
        )
