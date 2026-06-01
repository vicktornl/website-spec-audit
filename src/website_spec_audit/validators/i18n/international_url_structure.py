from urllib.parse import urlparse

from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class InternationalUrlStructureValidator(BaseValidator):
    slug = "international-url-structure"
    title = "International URL structure"
    category = "i18n"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/i18n/international-url-structure/"

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

        # Classify URL patterns
        site_parsed = urlparse(context.url)
        site_domain = site_parsed.netloc.lower()

        patterns: set[str] = set()
        details: list[str] = []

        for link in hreflang_links:
            href = link["href"]
            if not href or href.startswith("#"):
                continue

            parsed = urlparse(href)
            link_domain = parsed.netloc.lower()

            if not link_domain:
                # Relative URL = subdirectory
                patterns.add("subdirectory")
            elif link_domain == site_domain:
                # Same domain with different path = subdirectory
                patterns.add("subdirectory")
            elif link_domain.endswith("." + site_domain.removeprefix("www.")):
                # Subdomain pattern (e.g. fr.example.com)
                patterns.add("subdomain")
            else:
                # Different domain entirely = ccTLD or separate domain
                patterns.add("cctld")

        langs = [link["hreflang"] for link in hreflang_links]
        details.append(f"Hreflang values: {', '.join(langs)}.")

        if len(patterns) > 1:
            details.append(
                f"Mixed URL patterns detected: {', '.join(sorted(patterns))}."
            )
            return self.warn_result(
                "Hreflang links use inconsistent URL patterns.",
                details=details,
            )

        pattern_name = next(iter(patterns)) if patterns else "unknown"
        details.append(f"URL pattern: {pattern_name}.")

        return self.pass_result(
            f"International URLs use consistent {pattern_name} pattern.",
        )
