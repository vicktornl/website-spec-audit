from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class ScrollbarGutterValidator(BaseValidator):
    slug = "scrollbar-gutter"
    title = "Scrollbar gutter"
    category = "performance"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/performance/scrollbar-gutter/"

    async def validate(self, context: AuditContext) -> CheckResult:
        return self.skip_result("requires CSS analysis")
