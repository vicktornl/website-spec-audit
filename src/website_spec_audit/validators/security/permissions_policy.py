from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class PermissionsPolicyValidator(BaseValidator):
    slug = "permissions-policy"
    title = "Permissions-Policy"
    category = "security"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/security/permissions-policy/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/")
        value = resource.headers.get("permissions-policy")

        if not value:
            return self.fail_result("Missing Permissions-Policy header.")

        return self.pass_result("Permissions-Policy header is present.")
