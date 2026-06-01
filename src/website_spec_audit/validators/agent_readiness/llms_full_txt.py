from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class LlmsFullTxtValidator(BaseValidator):
    slug = "llms-full-txt"
    title = "/llms-full.txt"
    category = "agent-readiness"
    status = TopicStatus.OPTIONAL
    spec_url = "https://specification.website/spec/agent-readiness/llms-full-txt/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/llms-full.txt")

        if resource.status_code == 404:
            return self.skip_result("/llms-full.txt not found (HTTP 404).")

        if resource.status_code != 200:
            return self.fail_result(
                f"/llms-full.txt returned HTTP {resource.status_code}."
            )

        if not resource.text.strip():
            return self.fail_result("/llms-full.txt is present but empty.")

        return self.pass_result(
            f"/llms-full.txt is present ({len(resource.text)} bytes)."
        )
