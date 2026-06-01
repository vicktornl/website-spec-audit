from website_spec_audit.validators.performance.bfcache import BfcacheValidator
from website_spec_audit.validators.performance.cache_control import (
    CacheControlValidator,
)
from website_spec_audit.validators.performance.compression import (
    CompressionValidator,
)
from website_spec_audit.validators.performance.core_web_vitals import (
    CoreWebVitalsValidator,
)
from website_spec_audit.validators.performance.critical_css import (
    CriticalCssValidator,
)
from website_spec_audit.validators.performance.css_containment import (
    CssContainmentValidator,
)
from website_spec_audit.validators.performance.font_loading import (
    FontLoadingValidator,
)
from website_spec_audit.validators.performance.http3 import Http3Validator
from website_spec_audit.validators.performance.image_optimization import (
    ImageOptimizationValidator,
)
from website_spec_audit.validators.performance.lazy_loading import (
    LazyLoadingValidator,
)
from website_spec_audit.validators.performance.no_vary_search import (
    NoVarySearchValidator,
)
from website_spec_audit.validators.performance.preload_prefetch_preconnect import (
    PreloadPrefetchPreconnectValidator,
)
from website_spec_audit.validators.performance.resource_hints import (
    ResourceHintsValidator,
)
from website_spec_audit.validators.performance.script_loading import (
    ScriptLoadingValidator,
)
from website_spec_audit.validators.performance.scroll_driven_animations import (
    ScrollDrivenAnimationsValidator,
)
from website_spec_audit.validators.performance.scrollbar_gutter import (
    ScrollbarGutterValidator,
)
from website_spec_audit.validators.performance.speculation_rules import (
    SpeculationRulesValidator,
)
from website_spec_audit.validators.performance.view_transitions import (
    ViewTransitionsValidator,
)
from website_spec_audit.validators.performance.visibility_aware_rendering import (
    VisibilityAwareRenderingValidator,
)

ALL_VALIDATORS = [
    CoreWebVitalsValidator(),
    ImageOptimizationValidator(),
    LazyLoadingValidator(),
    PreloadPrefetchPreconnectValidator(),
    CacheControlValidator(),
    NoVarySearchValidator(),
    CompressionValidator(),
    FontLoadingValidator(),
    CriticalCssValidator(),
    ScriptLoadingValidator(),
    Http3Validator(),
    SpeculationRulesValidator(),
    ResourceHintsValidator(),
    ViewTransitionsValidator(),
    BfcacheValidator(),
    VisibilityAwareRenderingValidator(),
    CssContainmentValidator(),
    ScrollDrivenAnimationsValidator(),
    ScrollbarGutterValidator(),
]
