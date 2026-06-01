from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus

USEFUL_REL_VALUES = {
    "alternate",
    "canonical",
    "author",
    "license",
    "next",
    "prev",
    "search",
    "api",
    "describedby",
    "service-doc",
    "service-desc",
    "type",
    "preconnect",
    "dns-prefetch",
    "preload",
    "nlweb",
}


class LinkHeadersValidator(BaseValidator):
    slug = "link-headers"
    title = "HTTP Link headers for discovery"
    category = "agent-readiness"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/agent-readiness/link-headers/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/")
        link_header = resource.headers.get("link", "")

        if not link_header:
            return self.fail_result(
                "No Link HTTP header found in the response."
            )

        details: list[str] = []
        parts = link_header.split(",")
        for part in parts:
            part = part.strip()
            # Extract rel values
            part_lower = part.lower()
            for rel in USEFUL_REL_VALUES:
                if f'rel="{rel}"' in part_lower or f"rel={rel}" in part_lower:
                    details.append(f"{part}")
                    break

        if details:
            return self.pass_result(
                f"Link header present with {len(details)} useful rel value(s).",
                details=details,
            )

        return self.warn_result(
            "Link header present but no recognized discovery rel values found.",
            details=[f"Raw Link header: {link_header[:200]}"],
        )
