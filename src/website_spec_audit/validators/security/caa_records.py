from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class CaaRecordsValidator(BaseValidator):
    slug = "caa-records"
    title = "DNS CAA records"
    category = "security"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/security/caa-records/"

    async def validate(self, context: AuditContext) -> CheckResult:
        return self.skip_result("requires DNS query")
