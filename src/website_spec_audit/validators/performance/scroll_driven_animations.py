from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class ScrollDrivenAnimationsValidator(BaseValidator):
    slug = "scroll-driven-animations"
    title = "Scroll-driven animations"
    category = "performance"
    status = TopicStatus.OPTIONAL
    spec_url = "https://specification.website/spec/performance/scroll-driven-animations/"

    async def validate(self, context: AuditContext) -> CheckResult:
        return self.skip_result("requires CSS analysis")
