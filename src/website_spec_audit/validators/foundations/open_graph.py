from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus

REQUIRED_OG_PROPERTIES = ["og:title", "og:description", "og:image", "og:url", "og:type"]


class OpenGraphValidator(BaseValidator):
    slug = "open-graph"
    title = "Open Graph protocol"
    category = "foundations"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/foundations/open-graph/"

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")

        found: dict[str, str] = {}
        for meta in doc.cssselect("meta[property]"):
            prop = meta.get("property", "")
            content = meta.get("content", "").strip()
            if prop.startswith("og:") and content:
                found[prop] = content

        missing = [p for p in REQUIRED_OG_PROPERTIES if p not in found]

        if not found:
            return self.fail_result("No Open Graph meta tags found.")

        if missing:
            return self.warn_result(
                f"Missing Open Graph properties: {', '.join(missing)}.",
                details=[f"Found: {', '.join(sorted(found.keys()))}"],
            )

        return self.pass_result("All required Open Graph properties found.")
