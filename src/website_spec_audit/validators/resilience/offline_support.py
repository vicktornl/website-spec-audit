from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class OfflineSupportValidator(BaseValidator):
    slug = "offline-support"
    title = "Offline support and service workers"
    category = "resilience"
    status = TopicStatus.OPTIONAL
    spec_url = "https://specification.website/spec/resilience/offline-support/"

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")
        resource = await context.fetch("/")

        details: list[str] = []
        has_service_worker = False
        has_manifest = False

        # Check for service worker registration in inline scripts
        html_text = resource.text
        if "navigator.serviceWorker.register" in html_text:
            has_service_worker = True
            details.append("Service worker registration found in page source.")

        # Check for <link rel="manifest">
        for link in doc.iter("link"):
            rel = (link.get("rel") or "").lower()
            if "manifest" in rel:
                has_manifest = True
                href = link.get("href") or ""
                details.append(f"Web app manifest link found: {href}.")
                break

        if has_service_worker and has_manifest:
            return self.pass_result(
                "Service worker and web app manifest detected.",
            )

        if has_service_worker:
            return self.pass_result(
                "Service worker registration detected.",
            )

        if has_manifest:
            return self.warn_result(
                "Web app manifest found but no service worker registration detected.",
                details=details,
            )

        return self.fail_result(
            "No service worker registration or manifest link found.",
        )
