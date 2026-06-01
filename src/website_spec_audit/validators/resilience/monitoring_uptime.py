from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class MonitoringUptimeValidator(BaseValidator):
    slug = "monitoring-uptime"
    title = "Monitoring and uptime"
    category = "resilience"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/resilience/monitoring-uptime/"

    async def validate(self, context: AuditContext) -> CheckResult:
        return self.skip_result("requires infrastructure inspection")
