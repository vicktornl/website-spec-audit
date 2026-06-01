from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class WebmcpValidator(BaseValidator):
    slug = "webmcp"
    title = "WebMCP \u2014 browser-native tools for agents"
    category = "agent-readiness"
    status = TopicStatus.OPTIONAL
    spec_url = "https://specification.website/spec/agent-readiness/webmcp/"

    async def validate(self, context: AuditContext) -> CheckResult:
        return self.skip_result("requires JavaScript runtime inspection")
