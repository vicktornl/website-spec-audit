from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class MaintenancePagesValidator(BaseValidator):
    slug = "maintenance-pages"
    title = "Maintenance pages and 503"
    category = "resilience"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/resilience/maintenance-pages/"

    async def validate(self, context: AuditContext) -> CheckResult:
        return self.skip_result("requires intentional downtime to verify")
