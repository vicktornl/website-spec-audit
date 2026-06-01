from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class HreflangValidator(BaseValidator):
    slug = "hreflang"
    title = "hreflang for language and regional URLs"
    category = "i18n"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/i18n/hreflang/"

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")

        hreflang_links: list[dict[str, str]] = []
        for link in doc.iter("link"):
            rel = (link.get("rel") or "").lower()
            if "alternate" in rel and link.get("hreflang"):
                href = link.get("href") or ""
                hreflang = link.get("hreflang") or ""
                hreflang_links.append({"href": href, "hreflang": hreflang})

        if not hreflang_links:
            return self.skip_result(
                "No hreflang links found; site may be single-language."
            )

        details: list[str] = []
        hreflang_values = [link["hreflang"] for link in hreflang_links]
        details.append(f"Found {len(hreflang_links)} hreflang link(s): {', '.join(hreflang_values)}.")

        # Check for x-default
        has_x_default = any(
            link["hreflang"].lower() == "x-default" for link in hreflang_links
        )
        if not has_x_default:
            details.append("Missing x-default hreflang value.")

        # Check for self-referencing hreflang
        current_url = context.url.rstrip("/")
        has_self_reference = any(
            link["href"].rstrip("/") == current_url for link in hreflang_links
        )
        if not has_self_reference:
            details.append(
                "No self-referencing hreflang found for the current URL."
            )

        if not has_x_default:
            return self.warn_result(
                "Hreflang links found but missing x-default.",
                details=details,
            )

        if not has_self_reference:
            return self.warn_result(
                "Hreflang links found but no self-referencing entry detected.",
                details=details,
            )

        return self.pass_result(
            f"Hreflang correctly configured with {len(hreflang_links)} alternate(s) including x-default.",
        )
