from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class AriaUsageValidator(BaseValidator):
    slug = "aria-usage"
    title = "ARIA \u2014 first rule of ARIA"
    category = "accessibility"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/accessibility/aria-usage/"

    # Mapping of native elements to their implicit ARIA roles
    REDUNDANT_ROLES: dict[str, set[str]] = {
        "a": {"link"},
        "button": {"button"},
        "nav": {"navigation"},
        "main": {"main"},
        "header": {"banner"},
        "footer": {"contentinfo"},
        "aside": {"complementary"},
        "form": {"form"},
        "article": {"article"},
        "section": {"region"},
        "table": {"table"},
        "img": {"img"},
        "input": {"textbox", "checkbox", "radio", "spinbutton", "slider"},
        "select": {"combobox", "listbox"},
        "textarea": {"textbox"},
        "ul": {"list"},
        "ol": {"list"},
        "li": {"listitem"},
        "h1": {"heading"},
        "h2": {"heading"},
        "h3": {"heading"},
        "h4": {"heading"},
        "h5": {"heading"},
        "h6": {"heading"},
    }

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")

        elements_with_role = doc.cssselect("[role]")

        if not elements_with_role:
            return self.pass_result("No elements with explicit role attribute found.")

        redundant: list[str] = []
        for el in elements_with_role:
            tag = el.tag.lower()
            role = (el.get("role") or "").strip().lower()
            if tag in self.REDUNDANT_ROLES and role in self.REDUNDANT_ROLES[tag]:
                redundant.append(
                    f'<{tag} role="{role}"> is redundant; '
                    f"<{tag}> already implies role \"{role}\"."
                )

        if redundant:
            return self.warn_result(
                f"{len(redundant)} element(s) with redundant ARIA roles.",
                details=redundant,
            )

        return self.pass_result(
            f"{len(elements_with_role)} element(s) with role attribute; none redundant."
        )
