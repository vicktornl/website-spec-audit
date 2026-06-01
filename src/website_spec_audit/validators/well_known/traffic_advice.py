import json

from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class TrafficAdviceValidator(BaseValidator):
    slug = "traffic-advice"
    title = "/.well-known/traffic-advice"
    category = "well-known"
    status = TopicStatus.OPTIONAL
    spec_url = "https://specification.website/spec/well-known/traffic-advice/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/.well-known/traffic-advice")

        if resource.status_code == 404:
            return self.skip_result(
                "/.well-known/traffic-advice not found (HTTP 404)."
            )

        if resource.status_code != 200:
            return self.fail_result(
                f"/.well-known/traffic-advice returned HTTP {resource.status_code}."
            )

        try:
            json.loads(resource.text)
        except (json.JSONDecodeError, ValueError):
            return self.fail_result(
                "/.well-known/traffic-advice is not valid JSON."
            )

        return self.pass_result(
            "/.well-known/traffic-advice is present and valid JSON."
        )
