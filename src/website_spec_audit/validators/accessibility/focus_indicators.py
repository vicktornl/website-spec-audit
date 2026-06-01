from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class FocusIndicatorsValidator(BaseValidator):
    slug = "focus-indicators"
    title = "Visible focus indicators"
    category = "accessibility"
    status = TopicStatus.REQUIRED
    spec_url = "https://specification.website/spec/accessibility/focus-indicators/"

    async def validate(self, context: AuditContext) -> CheckResult:
        return self.skip_result("requires rendered CSS inspection")
