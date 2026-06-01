from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class SpeculationRulesValidator(BaseValidator):
    slug = "speculation-rules"
    title = "Speculation Rules"
    category = "performance"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/performance/speculation-rules/"

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")

        for script in doc.iter("script"):
            script_type = (script.get("type") or "").lower()
            if script_type == "speculationrules":
                return self.pass_result(
                    "Speculation Rules found (<script type=\"speculationrules\">)."
                )

        return self.warn_result(
            "No <script type=\"speculationrules\"> found. "
            "Consider adding speculation rules for faster navigations."
        )
