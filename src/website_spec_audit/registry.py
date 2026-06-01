from website_spec_audit.base import BaseValidator
from website_spec_audit.models import TopicStatus


class ValidatorRegistry:
    def __init__(self) -> None:
        self._validators: list[BaseValidator] = []

    def register(self, validator: BaseValidator) -> None:
        self._validators.append(validator)

    def all(self) -> list[BaseValidator]:
        return list(self._validators)

    def by_category(self, category: str) -> list[BaseValidator]:
        return [v for v in self._validators if v.category == category]

    def by_status(self, status: TopicStatus) -> list[BaseValidator]:
        return [v for v in self._validators if v.status == status]

    def filter(
        self,
        categories: list[str] | None = None,
        statuses: list[TopicStatus] | None = None,
        slugs: list[str] | None = None,
    ) -> list[BaseValidator]:
        result = self._validators
        if categories:
            result = [v for v in result if v.category in categories]
        if statuses:
            result = [v for v in result if v.status in statuses]
        if slugs:
            result = [v for v in result if v.slug in slugs]
        return result


registry = ValidatorRegistry()
