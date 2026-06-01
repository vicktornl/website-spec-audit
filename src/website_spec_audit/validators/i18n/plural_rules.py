from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class PluralRulesValidator(BaseValidator):
    slug = "plural-rules"
    title = "Plural rules and grammatical number"
    category = "i18n"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/i18n/plural-rules/"

    async def validate(self, context: AuditContext) -> CheckResult:
        return self.skip_result("requires code-level inspection")
