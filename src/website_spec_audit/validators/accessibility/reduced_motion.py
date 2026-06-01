from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class ReducedMotionValidator(BaseValidator):
    slug = "reduced-motion"
    title = "Reduced motion"
    category = "accessibility"
    status = TopicStatus.REQUIRED
    spec_url = "https://specification.website/spec/accessibility/reduced-motion/"

    async def validate(self, context: AuditContext) -> CheckResult:
        return self.skip_result("requires CSS inspection for prefers-reduced-motion")
