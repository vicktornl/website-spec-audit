from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class LlmsTxtValidator(BaseValidator):
    slug = "llms-txt"
    title = "/llms.txt"
    category = "agent-readiness"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/agent-readiness/llms-txt/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/llms.txt")

        if resource.status_code != 200:
            return self.fail_result(
                f"/llms.txt returned HTTP {resource.status_code}."
            )

        if not resource.text.strip():
            return self.fail_result("/llms.txt is present but empty.")

        return self.pass_result(
            f"/llms.txt is present ({len(resource.text)} bytes)."
        )
