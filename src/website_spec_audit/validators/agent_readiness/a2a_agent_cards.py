import json

from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class A2aAgentCardsValidator(BaseValidator):
    slug = "a2a-agent-cards"
    title = "A2A agent cards"
    category = "agent-readiness"
    status = TopicStatus.OPTIONAL
    spec_url = "https://specification.website/spec/agent-readiness/a2a-agent-cards/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/.well-known/agent-card.json")

        if resource.status_code == 404:
            return self.skip_result(
                "/.well-known/agent-card.json not found (HTTP 404)."
            )

        if resource.status_code != 200:
            return self.fail_result(
                f"/.well-known/agent-card.json returned HTTP {resource.status_code}."
            )

        try:
            json.loads(resource.text)
        except (json.JSONDecodeError, ValueError):
            return self.fail_result(
                "/.well-known/agent-card.json is not valid JSON."
            )

        return self.pass_result(
            "/.well-known/agent-card.json is present and valid JSON."
        )
