from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class VisibilityAwareRenderingValidator(BaseValidator):
    slug = "visibility-aware-rendering"
    title = "Visibility-aware rendering"
    category = "performance"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/performance/visibility-aware-rendering/"

    async def validate(self, context: AuditContext) -> CheckResult:
        return self.skip_result("requires CSS analysis")
