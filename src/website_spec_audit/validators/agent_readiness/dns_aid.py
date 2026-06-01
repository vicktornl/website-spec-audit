from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class DnsAidValidator(BaseValidator):
    slug = "dns-aid"
    title = "DNS for AI Discovery (DNS-AID)"
    category = "agent-readiness"
    status = TopicStatus.OPTIONAL
    spec_url = "https://specification.website/spec/agent-readiness/dns-aid/"

    async def validate(self, context: AuditContext) -> CheckResult:
        return self.skip_result("requires DNS query")
