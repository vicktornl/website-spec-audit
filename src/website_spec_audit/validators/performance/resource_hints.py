from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class ResourceHintsValidator(BaseValidator):
    slug = "resource-hints"
    title = "Resource hints overview"
    category = "performance"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/performance/resource-hints/"

    HINT_TYPES = {"dns-prefetch", "preconnect", "preload", "modulepreload", "prefetch"}

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")

        found: dict[str, int] = {}

        for link in doc.iter("link"):
            rel = (link.get("rel") or "").lower()
            for hint_type in self.HINT_TYPES:
                if hint_type in rel:
                    found[hint_type] = found.get(hint_type, 0) + 1

        if not found:
            return self.warn_result(
                "No resource hints found (dns-prefetch, preconnect, preload, modulepreload, prefetch)."
            )

        details = [
            f"{hint_type}: {count}"
            for hint_type, count in sorted(found.items())
        ]

        total = sum(found.values())
        return self.pass_result(
            f"Found {total} resource hint(s): {', '.join(details)}."
        )
