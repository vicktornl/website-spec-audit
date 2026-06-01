import json

from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class StructuredDataForAgentsValidator(BaseValidator):
    slug = "structured-data-for-agents"
    title = "Structured data for agents"
    category = "agent-readiness"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/agent-readiness/structured-data-for-agents/"

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")
        scripts = doc.cssselect('script[type="application/ld+json"]')

        if not scripts:
            return self.fail_result(
                "No JSON-LD structured data found (<script type=\"application/ld+json\">)."
            )

        details: list[str] = []
        has_schema_org = False

        for i, script in enumerate(scripts):
            text = script.text_content().strip()
            if not text:
                continue
            try:
                data = json.loads(text)
                # data can be a dict or a list
                items = data if isinstance(data, list) else [data]
                for item in items:
                    if isinstance(item, dict):
                        ctx = item.get("@context", "")
                        type_ = item.get("@type", "unknown")
                        if "schema.org" in str(ctx):
                            has_schema_org = True
                            details.append(f"JSON-LD block {i + 1}: @type={type_}")
            except (json.JSONDecodeError, ValueError):
                details.append(f"JSON-LD block {i + 1}: invalid JSON.")

        if has_schema_org:
            return self.pass_result(
                f"Found {len(scripts)} JSON-LD block(s) with schema.org context.",
                details=details,
            )

        return self.warn_result(
            "JSON-LD blocks found but none reference schema.org @context.",
            details=details,
        )
