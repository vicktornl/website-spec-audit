from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class PrivacyPolicyValidator(BaseValidator):
    slug = "privacy-policy"
    title = "Privacy policy"
    category = "privacy"
    status = TopicStatus.REQUIRED
    spec_url = "https://specification.website/spec/privacy/privacy-policy/"

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")

        privacy_keywords = ["privacy", "privacybeleid", "datenschutz"]

        # Check all anchor elements for privacy-related links
        for link in doc.iter("a"):
            href = (link.get("href") or "").lower()
            text = (link.text_content() or "").lower().strip()

            for keyword in privacy_keywords:
                if keyword in href or keyword in text:
                    return self.pass_result(
                        f"Found privacy policy link: '{link.text_content().strip()}'."
                    )

        return self.fail_result(
            "No privacy policy link found on the page.",
            details=[
                "Expected a link containing 'privacy' in its href or text.",
            ],
        )
