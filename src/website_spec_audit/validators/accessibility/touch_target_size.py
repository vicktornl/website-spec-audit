from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class TouchTargetSizeValidator(BaseValidator):
    slug = "touch-target-size"
    title = "Touch target size"
    category = "accessibility"
    status = TopicStatus.REQUIRED
    spec_url = "https://specification.website/spec/accessibility/touch-target-size/"

    async def validate(self, context: AuditContext) -> CheckResult:
        return self.skip_result("requires rendered layout measurement")
