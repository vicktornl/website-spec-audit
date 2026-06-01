from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class FormErrorsValidator(BaseValidator):
    slug = "form-errors"
    title = "Accessible form errors"
    category = "accessibility"
    status = TopicStatus.REQUIRED
    spec_url = "https://specification.website/spec/accessibility/form-errors/"

    async def validate(self, context: AuditContext) -> CheckResult:
        return self.skip_result("requires form submission testing")
