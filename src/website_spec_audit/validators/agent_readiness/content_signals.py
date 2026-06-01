from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class ContentSignalsValidator(BaseValidator):
    slug = "content-signals"
    title = "Content Signals in robots.txt"
    category = "agent-readiness"
    status = TopicStatus.OPTIONAL
    spec_url = "https://specification.website/spec/agent-readiness/content-signals/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/robots.txt")

        if resource.status_code != 200:
            return self.skip_result(
                f"/robots.txt returned HTTP {resource.status_code}."
            )

        text = resource.text.lower()

        if "content-signal" in text:
            return self.pass_result(
                "robots.txt contains Content-Signal directives."
            )

        return self.skip_result(
            "No Content-Signal directives found in robots.txt."
        )
