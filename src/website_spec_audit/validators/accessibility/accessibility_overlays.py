from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class AccessibilityOverlaysValidator(BaseValidator):
    slug = "accessibility-overlays"
    title = "Accessibility overlays"
    category = "accessibility"
    status = TopicStatus.AVOID
    spec_url = "https://specification.website/spec/accessibility/accessibility-overlays/"

    OVERLAY_PATTERNS = [
        "accessibe",
        "audioeye",
        "equalweb",
        "userway",
        "accessibly",
        "truely-accessible",
        "maxaccess",
        "adally",
        "enable-javascript.com",
        "accessibilitywidget",
    ]

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")

        scripts = doc.cssselect("script[src]")

        found: list[str] = []
        for script in scripts:
            src = (script.get("src") or "").lower()
            for pattern in self.OVERLAY_PATTERNS:
                if pattern in src:
                    found.append(
                        f'Script src contains "{pattern}": {script.get("src")}'
                    )
                    break

        if found:
            return self.fail_result(
                f"{len(found)} accessibility overlay script(s) detected.",
                details=found,
            )

        return self.pass_result("No accessibility overlay scripts detected.")
