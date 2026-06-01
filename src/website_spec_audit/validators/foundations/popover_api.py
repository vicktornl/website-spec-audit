from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class PopoverApiValidator(BaseValidator):
    slug = "popover-api"
    title = "Popover API"
    category = "foundations"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/foundations/popover-api/"

    async def validate(self, context: AuditContext) -> CheckResult:
        return self.skip_result("Requires rendered DOM inspection.")
