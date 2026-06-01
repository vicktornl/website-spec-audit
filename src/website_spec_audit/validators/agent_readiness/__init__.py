from website_spec_audit.validators.agent_readiness.a2a_agent_cards import (
    A2aAgentCardsValidator,
)
from website_spec_audit.validators.agent_readiness.agent_readiness_overview import (
    AgentReadinessOverviewValidator,
)
from website_spec_audit.validators.agent_readiness.agent_skills_discovery import (
    AgentSkillsDiscoveryValidator,
)
from website_spec_audit.validators.agent_readiness.content_signals import (
    ContentSignalsValidator,
)
from website_spec_audit.validators.agent_readiness.dns_aid import DnsAidValidator
from website_spec_audit.validators.agent_readiness.link_headers import (
    LinkHeadersValidator,
)
from website_spec_audit.validators.agent_readiness.llms_full_txt import (
    LlmsFullTxtValidator,
)
from website_spec_audit.validators.agent_readiness.llms_txt import LlmsTxtValidator
from website_spec_audit.validators.agent_readiness.machine_readable_formats import (
    MachineReadableFormatsValidator,
)
from website_spec_audit.validators.agent_readiness.markdown_source_endpoints import (
    MarkdownSourceEndpointsValidator,
)
from website_spec_audit.validators.agent_readiness.mcp_and_tool_discovery import (
    McpAndToolDiscoveryValidator,
)
from website_spec_audit.validators.agent_readiness.nlweb import NlwebValidator
from website_spec_audit.validators.agent_readiness.robots_for_ai_crawlers import (
    RobotsForAiCrawlersValidator,
)
from website_spec_audit.validators.agent_readiness.schemamap import SchemamapValidator
from website_spec_audit.validators.agent_readiness.stable_urls import (
    StableUrlsValidator,
)
from website_spec_audit.validators.agent_readiness.structured_data_for_agents import (
    StructuredDataForAgentsValidator,
)
from website_spec_audit.validators.agent_readiness.web_bot_auth import (
    WebBotAuthValidator,
)
from website_spec_audit.validators.agent_readiness.webmcp import WebmcpValidator

ALL_VALIDATORS = [
    AgentReadinessOverviewValidator(),
    LlmsTxtValidator(),
    LlmsFullTxtValidator(),
    MarkdownSourceEndpointsValidator(),
    RobotsForAiCrawlersValidator(),
    ContentSignalsValidator(),
    WebBotAuthValidator(),
    StableUrlsValidator(),
    StructuredDataForAgentsValidator(),
    MachineReadableFormatsValidator(),
    LinkHeadersValidator(),
    McpAndToolDiscoveryValidator(),
    A2aAgentCardsValidator(),
    AgentSkillsDiscoveryValidator(),
    DnsAidValidator(),
    NlwebValidator(),
    WebmcpValidator(),
    SchemamapValidator(),
]
