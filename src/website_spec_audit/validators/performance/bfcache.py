from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class BfcacheValidator(BaseValidator):
    slug = "bfcache"
    title = "Back/forward cache (BFCache)"
    category = "performance"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/performance/bfcache/"

    async def validate(self, context: AuditContext) -> CheckResult:
        return self.skip_result("requires browser navigation testing")
