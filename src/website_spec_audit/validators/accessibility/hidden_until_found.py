from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class HiddenUntilFoundValidator(BaseValidator):
    slug = "hidden-until-found"
    title = "Hidden until found"
    category = "accessibility"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/accessibility/hidden-until-found/"

    async def validate(self, context: AuditContext) -> CheckResult:
        return self.skip_result("requires DOM inspection")
