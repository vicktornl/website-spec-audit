import json

from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class StructuredDataValidator(BaseValidator):
    slug = "structured-data"
    title = "Structured data (JSON-LD)"
    category = "seo"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/seo/structured-data/"

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")
        scripts = doc.cssselect('script[type="application/ld+json"]')

        if not scripts:
            return self.fail_result("No JSON-LD structured data found on the page.")

        details: list[str] = []
        valid_count = 0

        for i, script in enumerate(scripts):
            text = script.text_content().strip()
            if not text:
                details.append(f"JSON-LD block {i + 1}: empty content.")
                continue

            try:
                data = json.loads(text)
            except json.JSONDecodeError as exc:
                details.append(f"JSON-LD block {i + 1}: invalid JSON ({exc}).")
                continue

            # Handle both single objects and arrays
            items = data if isinstance(data, list) else [data]
            for item in items:
                if not isinstance(item, dict):
                    continue
                context_val = item.get("@context", "")
                type_val = item.get("@type", "")
                if context_val and type_val:
                    details.append(f"@type: {type_val}")
                    valid_count += 1
                elif not context_val:
                    details.append(f"JSON-LD block {i + 1}: missing @context.")
                elif not type_val:
                    details.append(f"JSON-LD block {i + 1}: missing @type.")

        if valid_count == 0:
            return self.fail_result(
                "JSON-LD blocks found but none contain valid @context and @type.",
                details=details,
            )

        return self.pass_result(
            f"{valid_count} valid JSON-LD structured data block(s) found. {'; '.join(details)}"
        )
