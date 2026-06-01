from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class DataMinimizationValidator(BaseValidator):
    slug = "data-minimization"
    title = "Data minimisation"
    category = "privacy"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/privacy/data-minimization/"

    async def validate(self, context: AuditContext) -> CheckResult:
        return self.skip_result("requires manual policy review")
