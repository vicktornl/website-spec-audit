from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class SitemapHreflangValidator(BaseValidator):
    slug = "sitemap-hreflang"
    title = "hreflang in XML sitemaps"
    category = "i18n"
    status = TopicStatus.OPTIONAL
    spec_url = "https://specification.website/spec/i18n/sitemap-hreflang/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/sitemap.xml")

        if resource.status_code != 200:
            return self.skip_result(
                f"No sitemap.xml found (status {resource.status_code})."
            )

        text = resource.text

        # Check for xhtml:link hreflang entries in the sitemap
        has_xhtml_ns = "xhtml" in text and "www.w3.org/1999/xhtml" in text
        has_hreflang = "hreflang" in text

        if not has_hreflang:
            return self.skip_result(
                "Sitemap found but does not contain hreflang annotations."
            )

        details: list[str] = []

        if not has_xhtml_ns:
            details.append(
                "Hreflang references found but xhtml namespace may not be properly declared."
            )

        # Count approximate hreflang entries
        hreflang_count = text.lower().count("hreflang=")
        details.append(f"Found approximately {hreflang_count} hreflang reference(s) in sitemap.")

        if not has_xhtml_ns:
            return self.warn_result(
                "Sitemap contains hreflang but xhtml namespace may be missing.",
                details=details,
            )

        return self.pass_result(
            f"Sitemap contains hreflang annotations ({hreflang_count} reference(s)).",
        )
