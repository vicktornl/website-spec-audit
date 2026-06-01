from website_spec_audit.validators.accessibility.accessibility_overlays import AccessibilityOverlaysValidator
from website_spec_audit.validators.accessibility.aria_usage import AriaUsageValidator
from website_spec_audit.validators.accessibility.captions_and_transcripts import CaptionsAndTranscriptsValidator
from website_spec_audit.validators.accessibility.color_contrast import ColorContrastValidator
from website_spec_audit.validators.accessibility.css_state_selectors import CssStateSelectorsValidator
from website_spec_audit.validators.accessibility.data_tables import DataTablesValidator
from website_spec_audit.validators.accessibility.document_language import DocumentLanguageValidator
from website_spec_audit.validators.accessibility.empty_links_buttons import EmptyLinksButtonsValidator
from website_spec_audit.validators.accessibility.focus_indicators import FocusIndicatorsValidator
from website_spec_audit.validators.accessibility.form_errors import FormErrorsValidator
from website_spec_audit.validators.accessibility.form_labels import FormLabelsValidator
from website_spec_audit.validators.accessibility.hidden_until_found import HiddenUntilFoundValidator
from website_spec_audit.validators.accessibility.image_alt_text import ImageAltTextValidator
from website_spec_audit.validators.accessibility.keyboard_navigation import KeyboardNavigationValidator
from website_spec_audit.validators.accessibility.link_text import LinkTextValidator
from website_spec_audit.validators.accessibility.native_interactive_elements import NativeInteractiveElementsValidator
from website_spec_audit.validators.accessibility.reduced_motion import ReducedMotionValidator
from website_spec_audit.validators.accessibility.semantic_html import SemanticHtmlValidator
from website_spec_audit.validators.accessibility.skip_links import SkipLinksValidator
from website_spec_audit.validators.accessibility.touch_target_size import TouchTargetSizeValidator

ALL_VALIDATORS = [
    ColorContrastValidator(),
    ImageAltTextValidator(),
    FormLabelsValidator(),
    KeyboardNavigationValidator(),
    FocusIndicatorsValidator(),
    SkipLinksValidator(),
    SemanticHtmlValidator(),
    AriaUsageValidator(),
    LinkTextValidator(),
    EmptyLinksButtonsValidator(),
    FormErrorsValidator(),
    DocumentLanguageValidator(),
    ReducedMotionValidator(),
    AccessibilityOverlaysValidator(),
    CaptionsAndTranscriptsValidator(),
    DataTablesValidator(),
    TouchTargetSizeValidator(),
    HiddenUntilFoundValidator(),
    NativeInteractiveElementsValidator(),
    CssStateSelectorsValidator(),
]
