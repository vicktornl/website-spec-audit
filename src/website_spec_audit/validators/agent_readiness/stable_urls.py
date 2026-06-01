import re
from urllib.parse import parse_qs, urlparse

from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus

TRACKING_PARAMS = {
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_term",
    "utm_content",
    "fbclid",
    "gclid",
    "msclkid",
    "mc_cid",
    "mc_eid",
}

SESSION_PATTERNS = [
    re.compile(r"[;?&]jsessionid=", re.IGNORECASE),
    re.compile(r"[;?&]phpsessid=", re.IGNORECASE),
    re.compile(r"[;?&]sid=", re.IGNORECASE),
    re.compile(r"[;?&]session_id=", re.IGNORECASE),
    re.compile(r"[;?&]sessionid=", re.IGNORECASE),
]


class StableUrlsValidator(BaseValidator):
    slug = "stable-urls"
    title = "Stable URLs"
    category = "agent-readiness"
    status = TopicStatus.REQUIRED
    spec_url = "https://specification.website/spec/agent-readiness/stable-urls/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/")
        issues: list[str] = []

        # Check for redirect chains
        final_url = resource.url
        if resource.is_redirect:
            # The context.fetch follows redirects; check if the final URL
            # differs significantly (suggesting a redirect chain).
            original_parsed = urlparse(context.url)
            final_parsed = urlparse(final_url)
            if original_parsed.netloc == final_parsed.netloc and original_parsed.path != final_parsed.path:
                issues.append(
                    f"URL redirects from {original_parsed.path} to {final_parsed.path}."
                )

        # Check for session IDs in the final URL
        for pattern in SESSION_PATTERNS:
            if pattern.search(final_url):
                issues.append(f"URL appears to contain a session ID: {final_url}")
                break

        # Check for tracking parameters
        parsed = urlparse(final_url)
        query_params = parse_qs(parsed.query)
        found_tracking = [
            p for p in query_params if p.lower() in TRACKING_PARAMS
        ]
        if found_tracking:
            issues.append(
                f"URL contains tracking parameters: {', '.join(found_tracking)}."
            )

        if issues:
            return self.fail_result("URL stability issues detected.", details=issues)

        return self.pass_result("URL is stable with no session IDs or tracking parameters.")
