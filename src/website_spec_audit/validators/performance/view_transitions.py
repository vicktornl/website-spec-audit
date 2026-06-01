from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class ViewTransitionsValidator(BaseValidator):
    slug = "view-transitions"
    title = "View Transitions"
    category = "performance"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/performance/view-transitions/"

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")

        # Check for <meta name="view-transition">
        for meta in doc.iter("meta"):
            name = (meta.get("name") or "").lower()
            if name == "view-transition":
                content = meta.get("content", "")
                return self.pass_result(
                    f"View Transition meta tag found: <meta name=\"view-transition\" content=\"{content}\">."
                )

        # Check for view-transition in inline styles
        for style in doc.iter("style"):
            text = (style.text_content() or "").lower()
            if "view-transition" in text:
                return self.pass_result(
                    "View Transition CSS detected in inline styles."
                )

        return self.skip_result(
            "No View Transition meta tag or CSS detected. "
            "This feature may be implemented via JavaScript or external CSS."
        )
