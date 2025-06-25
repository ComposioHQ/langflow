from .composio_api import ComposioAPIComponent
from .composio_dynamic import COMPOSIO_APP_METADATA, ComposioDynamicComponent
from .github_composio import ComposioGitHubAPIComponent
from .gmail_composio import ComposioGmailAPIComponent
from .googlecalendar_composio import ComposioGoogleCalendarAPIComponent
from .outlook_composio import ComposioOutlookAPIComponent
from .slack_composio import ComposioSlackAPIComponent

_generated_components = []
_all_exports = [
    "ComposioAPIComponent",
    "ComposioGitHubAPIComponent",
    "ComposioGmailAPIComponent",
    "ComposioGoogleCalendarAPIComponent",
    "ComposioOutlookAPIComponent",
    "ComposioSlackAPIComponent",
]


def _create_app_component(app_name: str, metadata: dict):
    """Create a Langflow component class for a specific Composio app."""
    class_name = f"Composio{metadata['display_name'].replace(' ', '')}Component"

    attrs = {
        "display_name": metadata["display_name"],
        "name": f"{metadata['display_name'].replace(' ', '')}API",
        "icon": metadata["icon"],
        "documentation": metadata["documentation"],
        "app_name": app_name,
        "description": metadata["description"],
    }

    if "primary_color" in metadata:
        attrs["primary_color"] = metadata["primary_color"]

    return type(class_name, (ComposioDynamicComponent,), attrs)


for app_name, metadata in COMPOSIO_APP_METADATA.items():
    component_class = _create_app_component(app_name, metadata)

    globals()[component_class.__name__] = component_class
    _generated_components.append(component_class)
    _all_exports.append(component_class.__name__)

__all__ = [
    "ComposioAPIComponent",
    "ComposioGitHubAPIComponent",
    "ComposioGmailAPIComponent",
    "ComposioGoogleCalendarAPIComponent",
    "ComposioOutlookAPIComponent",
    "ComposioSlackAPIComponent",
] + [component_class.__name__ for component_class in _generated_components]
