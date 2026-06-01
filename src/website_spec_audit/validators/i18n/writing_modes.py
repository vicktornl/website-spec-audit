from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class WritingModesValidator(BaseValidator):
    slug = "writing-modes"
    title = "Writing modes and CJK line breaking"
    category = "i18n"
    status = TopicStatus.OPTIONAL
    spec_url = "https://specification.website/spec/i18n/writing-modes/"

    async def validate(self, context: AuditContext) -> CheckResult:
        return self.skip_result("requires CSS analysis")
