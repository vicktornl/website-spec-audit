from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class McpAndToolDiscoveryValidator(BaseValidator):
    slug = "mcp-and-tool-discovery"
    title = "MCP and tool discovery"
    category = "agent-readiness"
    status = TopicStatus.OPTIONAL
    spec_url = "https://specification.website/spec/agent-readiness/mcp-and-tool-discovery/"

    async def validate(self, context: AuditContext) -> CheckResult:
        return self.skip_result("MCP discovery requires protocol-level inspection")
