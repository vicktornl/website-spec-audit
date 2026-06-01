from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class NativeInteractiveElementsValidator(BaseValidator):
    slug = "native-interactive-elements"
    title = "Native interactive elements"
    category = "accessibility"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/accessibility/native-interactive-elements/"

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")

        issues: list[str] = []

        # Find non-interactive elements with onclick handlers
        for tag in ("div", "span"):
            elements = doc.cssselect(f"{tag}[onclick]")
            for el in elements:
                text = (el.text_content() or "").strip()[:50]
                issues.append(
                    f'<{tag} onclick="..."> found (text: "{text}"). '
                    f"Use <button> or <a> instead."
                )

        # Find divs/spans with role="button" or role="link"
        for role in ("button", "link"):
            for tag in ("div", "span"):
                elements = doc.cssselect(f'{tag}[role="{role}"]')
                for el in elements:
                    text = (el.text_content() or "").strip()[:50]
                    issues.append(
                        f'<{tag} role="{role}"> found (text: "{text}"). '
                        f"Use <{role if role != 'link' else 'a'}> instead."
                    )

        if issues:
            return self.warn_result(
                f"{len(issues)} non-native interactive element(s) found.",
                details=issues,
            )

        return self.pass_result(
            "No non-native interactive elements detected."
        )
