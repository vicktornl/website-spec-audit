from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class ColorContrastValidator(BaseValidator):
    slug = "color-contrast"
    title = "Colour contrast"
    category = "accessibility"
    status = TopicStatus.REQUIRED
    spec_url = "https://specification.website/spec/accessibility/color-contrast/"

    async def validate(self, context: AuditContext) -> CheckResult:
        return self.skip_result("requires rendered CSS; cannot verify via HTTP")
