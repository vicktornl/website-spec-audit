from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class ScriptLoadingValidator(BaseValidator):
    slug = "script-loading"
    title = "Script loading \u2014 defer, async, module"
    category = "performance"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/performance/script-loading/"

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")

        head = doc.find(".//head")
        if head is None:
            return self.warn_result("No <head> element found in the document.")

        blocking_scripts: list[str] = []
        optimized_scripts: list[str] = []

        for script in head.iter("script"):
            src = script.get("src")
            if not src:
                continue

            has_defer = script.get("defer") is not None
            has_async = script.get("async") is not None
            script_type = (script.get("type") or "").lower()
            is_module = script_type == "module"

            if has_defer or has_async or is_module:
                optimized_scripts.append(src)
            else:
                blocking_scripts.append(src)

        if not blocking_scripts and not optimized_scripts:
            return self.pass_result("No external scripts found in <head>.")

        if not blocking_scripts:
            return self.pass_result(
                f"All {len(optimized_scripts)} script(s) in <head> use defer, async, or type=\"module\"."
            )

        details = [
            f"{len(blocking_scripts)} render-blocking script(s) in <head> without defer/async/module:"
        ]
        for src in blocking_scripts[:5]:
            details.append(f"  - {src}")

        if len(blocking_scripts) > 5:
            details.append(f"  ... and {len(blocking_scripts) - 5} more.")

        return self.warn_result(
            f"{len(blocking_scripts)} script(s) in <head> may block rendering.",
            details=details,
        )
