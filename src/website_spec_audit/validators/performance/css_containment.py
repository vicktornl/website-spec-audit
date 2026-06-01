from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class CssContainmentValidator(BaseValidator):
    slug = "css-containment"
    title = "CSS containment"
    category = "performance"
    status = TopicStatus.OPTIONAL
    spec_url = "https://specification.website/spec/performance/css-containment/"

    async def validate(self, context: AuditContext) -> CheckResult:
        return self.skip_result("requires CSS analysis")
