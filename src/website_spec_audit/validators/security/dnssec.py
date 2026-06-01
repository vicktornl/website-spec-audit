from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class DnssecValidator(BaseValidator):
    slug = "dnssec"
    title = "DNSSEC"
    category = "security"
    status = TopicStatus.OPTIONAL
    spec_url = "https://specification.website/spec/security/dnssec/"

    async def validate(self, context: AuditContext) -> CheckResult:
        return self.skip_result("requires DNS query")
