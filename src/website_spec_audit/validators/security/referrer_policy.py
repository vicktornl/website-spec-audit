from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class ReferrerPolicyValidator(BaseValidator):
    slug = "referrer-policy"
    title = "Referrer-Policy"
    category = "security"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/security/referrer-policy/"

    UNSAFE_POLICIES = {"unsafe-url", "no-referrer-when-downgrade"}

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/")
        value = resource.headers.get("referrer-policy")

        if not value:
            return self.fail_result("Missing Referrer-Policy header.")

        policy = value.strip().lower()

        if policy in self.UNSAFE_POLICIES:
            return self.warn_result(
                f"Referrer-Policy is '{value}', which may leak sensitive information."
            )

        return self.pass_result(f"Referrer-Policy is set to '{value}'.")
