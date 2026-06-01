from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class PreloadPrefetchPreconnectValidator(BaseValidator):
    slug = "preload-prefetch-preconnect"
    title = "Preload, prefetch, preconnect"
    category = "performance"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/performance/preload-prefetch-preconnect/"

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")

        head = doc.find(".//head")
        if head is None:
            return self.warn_result("No <head> element found in the document.")

        found: dict[str, int] = {
            "preload": 0,
            "prefetch": 0,
            "preconnect": 0,
        }

        for link in head.iter("link"):
            rel = (link.get("rel") or "").lower()
            for hint_type in found:
                if hint_type in rel:
                    found[hint_type] += 1

        total = sum(found.values())
        if total == 0:
            return self.warn_result(
                "No preload, prefetch, or preconnect hints found in <head>."
            )

        details = [
            f"{hint_type}: {count} found"
            for hint_type, count in found.items()
            if count > 0
        ]

        return self.pass_result(
            f"Found {total} resource hint(s) in <head>: {', '.join(details)}."
        )
