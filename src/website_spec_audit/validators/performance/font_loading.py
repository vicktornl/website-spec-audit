from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class FontLoadingValidator(BaseValidator):
    slug = "font-loading"
    title = "Web font loading"
    category = "performance"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/performance/font-loading/"

    EXTERNAL_FONT_CDNS = [
        "fonts.googleapis.com",
        "fonts.gstatic.com",
        "use.typekit.net",
        "fast.fonts.net",
        "cloud.typography.com",
    ]

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")

        details: list[str] = []
        has_font_preload = False
        has_font_display = False
        external_font_links: list[str] = []

        # Check for <link rel="preload" as="font">
        for link in doc.iter("link"):
            rel = (link.get("rel") or "").lower()
            as_attr = (link.get("as") or "").lower()
            href = link.get("href", "")

            if "preload" in rel and as_attr == "font":
                has_font_preload = True

            # Check for external font CDN stylesheets
            if "stylesheet" in rel:
                for cdn in self.EXTERNAL_FONT_CDNS:
                    if cdn in href:
                        external_font_links.append(href)
                        break

        # Check for font-display in inline <style> tags
        for style in doc.iter("style"):
            text = style.text_content() or ""
            if "font-display" in text.lower():
                has_font_display = True
                break

        if has_font_preload:
            details.append("Font preloading detected (<link rel=\"preload\" as=\"font\">).")
        if has_font_display:
            details.append("font-display property found in inline styles.")
        if external_font_links:
            details.append(
                f"External font CDN(s) detected: {', '.join(external_font_links[:5])}"
            )

        if not has_font_preload and not has_font_display and not external_font_links:
            return self.pass_result(
                "No web font loading issues detected (no external fonts or preloads found)."
            )

        issues: list[str] = []
        if external_font_links and not has_font_preload:
            issues.append(
                "External fonts loaded without preload hints. "
                "Consider adding <link rel=\"preload\" as=\"font\"> for critical fonts."
            )

        if issues:
            return self.warn_result(
                "Web font loading could be improved.",
                details=issues + details,
            )

        return self.pass_result(
            "Web font loading is well-configured.",
        )
