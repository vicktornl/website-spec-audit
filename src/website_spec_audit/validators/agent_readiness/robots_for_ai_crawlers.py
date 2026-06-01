from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus

AI_USER_AGENTS = [
    "GPTBot",
    "ChatGPT-User",
    "Google-Extended",
    "Anthropic",
    "ClaudeBot",
    "Claude-Web",
    "CCBot",
    "Bytespider",
    "Amazonbot",
    "FacebookBot",
    "Applebot-Extended",
    "PerplexityBot",
    "Cohere-ai",
]


class RobotsForAiCrawlersValidator(BaseValidator):
    slug = "robots-for-ai-crawlers"
    title = "robots.txt for AI crawlers"
    category = "agent-readiness"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/agent-readiness/robots-for-ai-crawlers/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/robots.txt")

        if resource.status_code != 200:
            return self.fail_result(
                f"/robots.txt returned HTTP {resource.status_code}."
            )

        text = resource.text.lower()
        found_agents: list[str] = []

        for agent in AI_USER_AGENTS:
            if agent.lower() in text:
                found_agents.append(agent)

        if found_agents:
            return self.pass_result(
                f"robots.txt addresses {len(found_agents)} AI crawler(s).",
                details=[f"Found: {', '.join(found_agents)}"],
            )

        return self.warn_result(
            "robots.txt does not mention any known AI crawler user-agents.",
            details=[
                "Consider adding directives for: "
                + ", ".join(AI_USER_AGENTS[:5])
                + ", etc."
            ],
        )
