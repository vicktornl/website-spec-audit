from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class SecurityTxtValidator(BaseValidator):
    slug = "security-txt"
    title = "/.well-known/security.txt"
    category = "security"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/security/security-txt/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/.well-known/security.txt")

        if resource.status_code != 200:
            return self.fail_result(
                f"/.well-known/security.txt returned HTTP {resource.status_code}."
            )

        text = resource.text
        lines = text.splitlines()

        missing: list[str] = []
        has_contact = any(
            line.strip().lower().startswith("contact:") for line in lines
        )
        has_expires = any(
            line.strip().lower().startswith("expires:") for line in lines
        )

        if not has_contact:
            missing.append("Missing required Contact: field.")

        if not has_expires:
            missing.append("Missing required Expires: field.")

        if missing:
            return self.warn_result(
                "security.txt found but missing required fields.", details=missing
            )

        return self.pass_result(
            "/.well-known/security.txt is present with Contact and Expires fields."
        )
