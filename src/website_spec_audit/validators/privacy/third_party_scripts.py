from urllib.parse import urlparse

from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class ThirdPartyScriptsValidator(BaseValidator):
    slug = "third-party-scripts"
    title = "Third-party scripts and privacy"
    category = "privacy"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/privacy/third-party-scripts/"

    THIRD_PARTY_THRESHOLD = 10

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")
        site_domain = urlparse(context.url).netloc.lower()

        third_party_domains: dict[str, int] = {}

        for script in doc.iter("script"):
            src = script.get("src")
            if not src:
                continue

            parsed = urlparse(src)
            domain = parsed.netloc.lower()

            # Skip relative URLs (same origin)
            if not domain:
                continue

            # Strip www. for comparison
            site_base = site_domain.removeprefix("www.")
            script_base = domain.removeprefix("www.")

            if script_base != site_base:
                third_party_domains[domain] = (
                    third_party_domains.get(domain, 0) + 1
                )

        if not third_party_domains:
            return self.pass_result("No third-party scripts detected.")

        total_scripts = sum(third_party_domains.values())
        domain_list = [
            f"{domain} ({count})" for domain, count in sorted(third_party_domains.items())
        ]

        details = [f"Third-party script domains: {', '.join(domain_list)}."]

        if total_scripts >= self.THIRD_PARTY_THRESHOLD:
            return self.warn_result(
                f"{total_scripts} third-party scripts from {len(third_party_domains)} domain(s) detected.",
                details=details,
            )

        return self.pass_result(
            f"{total_scripts} third-party script(s) from {len(third_party_domains)} domain(s).",
        )
