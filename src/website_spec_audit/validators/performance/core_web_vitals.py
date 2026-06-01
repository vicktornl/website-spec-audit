from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class CoreWebVitalsValidator(BaseValidator):
    slug = "core-web-vitals"
    title = "Core Web Vitals (LCP, INP, CLS)"
    category = "performance"
    status = TopicStatus.REQUIRED
    spec_url = "https://specification.website/spec/performance/core-web-vitals/"

    async def validate(self, context: AuditContext) -> CheckResult:
        return self.skip_result("requires real user measurement or Lighthouse")
