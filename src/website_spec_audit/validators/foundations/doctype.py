from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class DoctypeValidator(BaseValidator):
    slug = "doctype"
    title = "The HTML doctype"
    category = "foundations"
    status = TopicStatus.REQUIRED
    spec_url = "https://specification.website/spec/foundations/doctype/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/")
        text = resource.text.lstrip()

        if text.lower().startswith("<!doctype html>"):
            return self.pass_result("Page starts with <!doctype html>.")

        return self.fail_result("Missing or incorrect doctype declaration.")
