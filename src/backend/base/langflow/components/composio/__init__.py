from __future__ import annotations

from typing import TYPE_CHECKING, Any

from langflow.components._importing import import_mod

if TYPE_CHECKING:
	from .airtable_composio import ComposioAirtableAPIComponent
	from .asana_composio import ComposioAsanaAPIComponent
	from .attio_composio import ComposioAttioAPIComponent
	from .calendly_composio import ComposioCalendlyAPIComponent
	from .composio_api import ComposioAPIComponent
	from .contentful_composio import ComposioContentfulAPIComponent
	from .discord_composio import ComposioDiscordAPIComponent
	from .figma_composio import ComposioFigmaAPIComponent
	from .github_composio import ComposioGitHubAPIComponent
	from .gmail_composio import ComposioGmailAPIComponent
	from .google_analytics_composio import ComposioGoogleAnalyticsAPIComponent
	from .googlecalendar_composio import ComposioGoogleCalendarAPIComponent
	from .googlemaps_composio import ComposioGoogleMapsAPIComponent
	from .googlemeet_composio import ComposioGooglemeetAPIComponent
	from .googlesheets_composio import ComposioGoogleSheetsAPIComponent
	from .googletasks_composio import ComposioGoogleTasksAPIComponent
	from .linear_composio import ComposioLinearAPIComponent
	from .miro_composio import ComposioMiroAPIComponent
	from .outlook_composio import ComposioOutlookAPIComponent
	from .reddit_composio import ComposioRedditAPIComponent
	from .slack_composio import ComposioSlackAPIComponent
	from .slackbot_composio import ComposioSlackbotAPIComponent
	from .supabase_composio import ComposioSupabaseAPIComponent
	from .todoist_composio import ComposioTodoistAPIComponent
	from .wrike_composio import ComposioWrikeAPIComponent
	from .youtube_composio import ComposioYoutubeAPIComponent
	from .dropbox_compnent import ComposioDropboxAPIComponent

_dynamic_imports = {
	"ComposioAirtableAPIComponent": "airtable_composio",
	"ComposioAsanaAPIComponent": "asana_composio",
	"ComposioAttioAPIComponent": "attio_composio",
	"ComposioCalendlyAPIComponent": "calendly_composio",
	"ComposioAPIComponent": "composio_api",
	"ComposioContentfulAPIComponent": "contentful_composio",
	"ComposioDiscordAPIComponent": "discord_composio",
	"ComposioFigmaAPIComponent": "figma_composio",
	"ComposioGitHubAPIComponent": "github_composio",
	"ComposioGmailAPIComponent": "gmail_composio",
	"ComposioGoogleAnalyticsAPIComponent": "google_analytics_composio",
	"ComposioGoogleCalendarAPIComponent": "googlecalendar_composio",
	"ComposioGoogleMapsAPIComponent": "googlemaps_composio",
	"ComposioGooglemeetAPIComponent": "googlemeet_composio",
	"ComposioGoogleSheetsAPIComponent": "googlesheets_composio",
	"ComposioGoogleTasksAPIComponent": "googletasks_composio",
	"ComposioLinearAPIComponent": "linear_composio",
	"ComposioMiroAPIComponent": "miro_composio",
	"ComposioOutlookAPIComponent": "outlook_composio",
	"ComposioRedditAPIComponent": "reddit_composio",
	"ComposioSlackAPIComponent": "slack_composio",
	"ComposioSlackbotAPIComponent": "slackbot_composio",
	"ComposioSupabaseAPIComponent": "supabase_composio",
	"ComposioTodoistAPIComponent": "todoist_composio",
	"ComposioWrikeAPIComponent": "wrike_composio",
	"ComposioYoutubeAPIComponent": "youtube_composio",
	"ComposioDropboxAPIComponent": "dropbox_compnent",
}

__all__ = [
	"ComposioAPIComponent",
	"ComposioAirtableAPIComponent",
	"ComposioAsanaAPIComponent",
	"ComposioAttioAPIComponent",
	"ComposioCalendlyAPIComponent",
	"ComposioContentfulAPIComponent",
	"ComposioDiscordAPIComponent",
	"ComposioFigmaAPIComponent",
	"ComposioGitHubAPIComponent",
	"ComposioGmailAPIComponent",
	"ComposioGoogleAnalyticsAPIComponent",
	"ComposioGoogleCalendarAPIComponent",
	"ComposioGoogleMapsAPIComponent",
	"ComposioGoogleTasksAPIComponent",
	"ComposioGooglemeetAPIComponent",
	"ComposioGoogleSheetsAPIComponent",
	"ComposioLinearAPIComponent",
	"ComposioMiroAPIComponent",
	"ComposioOutlookAPIComponent",
	"ComposioRedditAPIComponent",
	"ComposioSlackAPIComponent",
	"ComposioSlackbotAPIComponent",
	"ComposioSupabaseAPIComponent",
	"ComposioTodoistAPIComponent",
	"ComposioWrikeAPIComponent",
	"ComposioYoutubeAPIComponent",
	"ComposioDropboxAPIComponent",
]


def __getattr__(attr_name: str) -> Any:
	if attr_name not in _dynamic_imports:
		msg = f"module '{__name__}' has no attribute '{attr_name}'"
		raise AttributeError(msg)
	try:
		result = import_mod(attr_name, _dynamic_imports[attr_name], __spec__.parent)
	except (ModuleNotFoundError, ImportError, AttributeError) as e:
		msg = f"Could not import '{attr_name}' from '{__name__}': {e}"
		raise AttributeError(msg) from e
	globals()[attr_name] = result
	return result


def __dir__() -> list[str]:
	return list(__all__)
