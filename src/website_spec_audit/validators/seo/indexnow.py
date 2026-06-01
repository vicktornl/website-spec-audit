from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class IndexNowValidator(BaseValidator):
    slug = "indexnow"
    title = "IndexNow"
    category = "seo"
    status = TopicStatus.OPTIONAL
    spec_url = "https://specification.website/spec/seo/indexnow/"

    async def validate(self, context: AuditContext) -> CheckResult:
        return self.skip_result("IndexNow is a push protocol; cannot be verified by inspection")
