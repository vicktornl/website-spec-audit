from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class FormLabelsValidator(BaseValidator):
    slug = "form-labels"
    title = "Form labels"
    category = "accessibility"
    status = TopicStatus.REQUIRED
    spec_url = "https://specification.website/spec/accessibility/form-labels/"

    SKIP_TYPES = {"hidden", "submit", "button", "image", "reset"}

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")

        controls = doc.cssselect("input, select, textarea")

        # Filter out input types that don't need labels
        labelable = []
        for ctrl in controls:
            if ctrl.tag == "input":
                input_type = (ctrl.get("type") or "text").lower()
                if input_type in self.SKIP_TYPES:
                    continue
            labelable.append(ctrl)

        if not labelable:
            return self.pass_result("No labelable form controls found.")

        # Collect all label for= targets and all element ids
        labels_by_for = set()
        for label in doc.cssselect("label[for]"):
            labels_by_for.add(label.get("for"))

        unlabelled: list[str] = []
        for ctrl in labelable:
            ctrl_id = ctrl.get("id", "")

            # Check explicit label via for/id
            if ctrl_id and ctrl_id in labels_by_for:
                continue

            # Check wrapping label
            parent = ctrl.getparent()
            wrapped = False
            while parent is not None:
                if parent.tag == "label":
                    wrapped = True
                    break
                parent = parent.getparent()
            if wrapped:
                continue

            # Check aria-label or aria-labelledby
            if ctrl.get("aria-label") or ctrl.get("aria-labelledby"):
                continue

            # Check title attribute as fallback
            if ctrl.get("title"):
                continue

            tag = ctrl.tag
            ctrl_type = ctrl.get("type", "")
            name = ctrl.get("name", "")
            desc = f"<{tag}"
            if ctrl_type:
                desc += f' type="{ctrl_type}"'
            if name:
                desc += f' name="{name}"'
            desc += ">"
            unlabelled.append(f"{desc} has no associated label.")

        if unlabelled:
            return self.fail_result(
                f"{len(unlabelled)} form control(s) missing an associated label.",
                details=unlabelled,
            )

        return self.pass_result(
            f"All {len(labelable)} form control(s) have associated labels."
        )
