from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class AvoidAutoGeoRedirectsValidator(BaseValidator):
    slug = "avoid-auto-geo-redirects"
    title = "Avoid automatic IP-based language redirects"
    category = "i18n"
    status = TopicStatus.AVOID
    spec_url = "https://specification.website/spec/i18n/avoid-auto-geo-redirects/"

    async def validate(self, context: AuditContext) -> CheckResult:
        return self.skip_result("requires multi-region request testing")
