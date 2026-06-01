from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class CssStateSelectorsValidator(BaseValidator):
    slug = "css-state-selectors"
    title = "CSS state and relational selectors"
    category = "accessibility"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/accessibility/css-state-selectors/"

    async def validate(self, context: AuditContext) -> CheckResult:
        return self.skip_result("requires CSS analysis")
