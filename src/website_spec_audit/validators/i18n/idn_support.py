from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class IdnSupportValidator(BaseValidator):
    slug = "idn-support"
    title = "Internationalised Domain Names (IDN)"
    category = "i18n"
    status = TopicStatus.OPTIONAL
    spec_url = "https://specification.website/spec/i18n/idn-support/"

    async def validate(self, context: AuditContext) -> CheckResult:
        return self.skip_result("requires DNS-level inspection")
