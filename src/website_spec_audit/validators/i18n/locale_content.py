from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class LocaleContentValidator(BaseValidator):
    slug = "locale-content"
    title = "Locale-aware content"
    category = "i18n"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/i18n/locale-content/"

    async def validate(self, context: AuditContext) -> CheckResult:
        return self.skip_result("requires content analysis across locales")
