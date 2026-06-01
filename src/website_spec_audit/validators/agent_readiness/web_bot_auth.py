from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class WebBotAuthValidator(BaseValidator):
    slug = "web-bot-auth"
    title = "Web Bot Auth \u2014 verifiable bot identity"
    category = "agent-readiness"
    status = TopicStatus.OPTIONAL
    spec_url = "https://specification.website/spec/agent-readiness/web-bot-auth/"

    async def validate(self, context: AuditContext) -> CheckResult:
        return self.skip_result("requires request signing verification")
