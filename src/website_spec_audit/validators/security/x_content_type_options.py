from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class XContentTypeOptionsValidator(BaseValidator):
    slug = "x-content-type-options"
    title = "X-Content-Type-Options: nosniff"
    category = "security"
    status = TopicStatus.REQUIRED
    spec_url = "https://specification.website/spec/security/x-content-type-options/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/")
        value = resource.headers.get("x-content-type-options")

        if not value:
            return self.fail_result("Missing X-Content-Type-Options header.")

        if value.strip().lower() != "nosniff":
            return self.fail_result(
                f"X-Content-Type-Options is '{value}', expected 'nosniff'."
            )

        return self.pass_result("X-Content-Type-Options is set to 'nosniff'.")
