from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class KeyboardNavigationValidator(BaseValidator):
    slug = "keyboard-navigation"
    title = "Keyboard navigation"
    category = "accessibility"
    status = TopicStatus.REQUIRED
    spec_url = "https://specification.website/spec/accessibility/keyboard-navigation/"

    async def validate(self, context: AuditContext) -> CheckResult:
        return self.skip_result("requires interactive browser testing")
