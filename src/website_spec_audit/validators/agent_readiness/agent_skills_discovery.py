from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class AgentSkillsDiscoveryValidator(BaseValidator):
    slug = "agent-skills-discovery"
    title = "Agent Skills discovery"
    category = "agent-readiness"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/agent-readiness/agent-skills-discovery/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/.well-known/agent-skills")

        if resource.status_code == 404:
            return self.skip_result(
                "/.well-known/agent-skills not found (HTTP 404)."
            )

        if resource.status_code != 200:
            return self.fail_result(
                f"/.well-known/agent-skills returned HTTP {resource.status_code}."
            )

        return self.pass_result(
            "/.well-known/agent-skills is present (HTTP 200)."
        )
