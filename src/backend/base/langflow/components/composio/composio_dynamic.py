from langflow.base.composio.composio_base import ComposioBaseComponent


class ComposioDynamicComponent(ComposioBaseComponent):
    """Dynamic base component for auto-generated Composio app components."""

    app_name: str = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.app_name:
            class_name = self.__class__.__name__
            if class_name.startswith("Composio") and class_name.endswith("Component"):
                self.app_name = class_name[8:-9].lower()  # Remove "Composio" and "Component"


COMPOSIO_APP_METADATA = {
    "gmail": {
        "display_name": "Gmail",
        "icon": "Mail",
        "description": "Interact with Gmail to send, read, and manage emails",
        "documentation": "https://docs.composio.dev/apps/gmail",
        "primary_color": "#EA4335",
    },
    "slack": {
        "display_name": "Slack",
        "icon": "MessageSquare",
        "description": "Send messages, manage channels, and interact with Slack workspaces",
        "documentation": "https://docs.composio.dev/apps/slack",
        "primary_color": "#4A154B",
    },
    "github": {
        "display_name": "GitHub",
        "icon": "Github",
        "description": "Manage repositories, issues, and pull requests on GitHub",
        "documentation": "https://docs.composio.dev/apps/github",
        "primary_color": "#181717",
    },
    "googlecalendar": {
        "display_name": "Google Calendar",
        "icon": "Calendar",
        "description": "Create, update, and manage Google Calendar events",
        "documentation": "https://docs.composio.dev/apps/googlecalendar",
        "primary_color": "#4285F4",
    },
    "outlook": {
        "display_name": "Outlook",
        "icon": "Mail",
        "description": "Manage Outlook emails, calendar, and contacts",
        "documentation": "https://docs.composio.dev/apps/outlook",
        "primary_color": "#0078D4",
    },
    "notion": {
        "display_name": "Notion",
        "icon": "FileText",
        "description": "Create and manage Notion pages, databases, and content",
        "documentation": "https://docs.composio.dev/apps/notion",
        "primary_color": "#000000",
    },
    "discord": {
        "display_name": "Discord",
        "icon": "MessageCircle",
        "description": "Send messages and manage Discord servers",
        "documentation": "https://docs.composio.dev/apps/discord",
        "primary_color": "#5865F2",
    },
    "linkedin": {
        "display_name": "LinkedIn",
        "icon": "Linkedin",
        "description": "Manage LinkedIn posts, connections, and professional network",
        "documentation": "https://docs.composio.dev/apps/linkedin",
        "primary_color": "#0A66C2",
    },
    "youtube": {
        "display_name": "YouTube",
        "icon": "Youtube",
        "description": "Upload, manage, and interact with YouTube videos and channels",
        "documentation": "https://docs.composio.dev/apps/youtube",
        "primary_color": "#FF0000",
    },
    "dropbox": {
        "display_name": "Dropbox",
        "icon": "Cloud",
        "description": "Upload, download, and manage files in Dropbox",
        "documentation": "https://docs.composio.dev/apps/dropbox",
        "primary_color": "#0061FF",
    },
    "confluence": {
        "display_name": "Confluence",
        "icon": "FileText",
        "description": "Create and manage Confluence pages and spaces",
        "documentation": "https://docs.composio.dev/apps/confluence",
        "primary_color": "#172B4D",
    },
}
