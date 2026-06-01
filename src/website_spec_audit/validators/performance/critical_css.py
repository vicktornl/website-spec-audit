from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class CriticalCssValidator(BaseValidator):
    slug = "critical-css"
    title = "Critical CSS and render-blocking resources"
    category = "performance"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/performance/critical-css/"

    MAX_RENDER_BLOCKING = 2

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")

        head = doc.find(".//head")
        if head is None:
            return self.warn_result("No <head> element found in the document.")

        render_blocking: list[str] = []
        non_blocking: list[str] = []

        for link in head.iter("link"):
            rel = (link.get("rel") or "").lower()
            if "stylesheet" not in rel:
                continue

            href = link.get("href", "")
            media = (link.get("media") or "").lower()

            # print-only or disabled stylesheets are not render-blocking
            if media == "print":
                non_blocking.append(href)
                continue

            render_blocking.append(href)

        has_inline_critical = False
        for style in head.iter("style"):
            text = (style.text_content() or "").strip()
            if text:
                has_inline_critical = True
                break

        details: list[str] = []
        if render_blocking:
            details.append(
                f"{len(render_blocking)} render-blocking stylesheet(s) in <head>."
            )
            for href in render_blocking[:5]:
                details.append(f"  - {href}")
        if non_blocking:
            details.append(f"{len(non_blocking)} non-render-blocking stylesheet(s) (print-only).")
        if has_inline_critical:
            details.append("Inline <style> found in <head> (good for critical CSS).")

        if len(render_blocking) == 0:
            return self.pass_result(
                "No render-blocking stylesheets found in <head>."
            )

        if len(render_blocking) <= self.MAX_RENDER_BLOCKING:
            return self.pass_result(
                f"{len(render_blocking)} render-blocking stylesheet(s) found, within acceptable range.",
            )

        return self.warn_result(
            f"{len(render_blocking)} render-blocking stylesheets in <head> may delay first paint.",
            details=details,
        )
