from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class LanguageSwitcherValidator(BaseValidator):
    slug = "language-switcher"
    title = "Language switcher"
    category = "i18n"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/i18n/language-switcher/"

    LANGUAGE_KEYWORDS = [
        "language",
        "lang-switch",
        "language-selector",
        "language-switcher",
        "locale-switch",
        "lang-select",
        "language-nav",
        "language-menu",
        "language-picker",
    ]

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")

        # Check for hreflang alternate links (indicates multilingual site)
        hreflang_links = []
        for link in doc.iter("link"):
            rel = (link.get("rel") or "").lower()
            if "alternate" in rel and link.get("hreflang"):
                hreflang_links.append(link.get("hreflang"))

        if not hreflang_links:
            return self.skip_result(
                "No hreflang links found; site may be single-language."
            )

        # Look for language switcher elements by hreflang on anchors
        anchor_hreflangs = []
        for anchor in doc.iter("a"):
            hreflang = anchor.get("hreflang")
            if hreflang:
                anchor_hreflangs.append(hreflang)

        if anchor_hreflangs:
            return self.pass_result(
                f"Language switcher links found with hreflang attributes: {', '.join(anchor_hreflangs)}.",
            )

        # Heuristic: look for elements with language-related class/id names
        resource = await context.fetch("/")
        html_lower = resource.text.lower()

        for keyword in self.LANGUAGE_KEYWORDS:
            if keyword in html_lower:
                return self.pass_result(
                    f"Possible language switcher detected (keyword: '{keyword}').",
                )

        return self.warn_result(
            "Multilingual site detected (hreflang present) but no language switcher found.",
            details=[
                f"Hreflang values: {', '.join(hreflang_links)}.",
                "A visible language switcher helps users choose their preferred language.",
            ],
        )
