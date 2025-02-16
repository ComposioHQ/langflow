# Third-party imports
from composio.client.collections import AppAuthScheme
from composio.client.exceptions import NoItemsFound
from composio_langchain import Action, App, ComposioToolSet
from langchain_core.tools import Tool
from loguru import logger
from typing import Any

# Local imports
from langflow.base.langchain_utilities.model import LCToolComponent
from langflow.inputs import DropdownInput, LinkInput, MessageTextInput, MultiselectInput, SecretStrInput, StrInput
from langflow.io import Output
from langflow.schema.message import Message


class GmailAPIComponent(LCToolComponent):
    display_name: str = "Gmail"
    description: str = "Use Gmail API to send emails and create drafts"
    name = "GmailAPI"
    icon = "Gmail"
    documentation: str = "https://docs.composio.dev"

    inputs = [
        MessageTextInput(
            name="entity_id",
            display_name="Entity ID",
            value="default",
            advanced=True,
            tool_mode=True,  # Enable tool mode toggle
        ),
        SecretStrInput(
            name="api_key",
            display_name="Composio API Key",
            required=True,
            info="Refer to https://docs.composio.dev/faq/api_key/api_key",
            real_time_refresh=True,
        ),
        LinkInput(
            name="auth_link",
            display_name="Authentication Link",
            value="",
            info="Click to authenticate with OAuth2",
            dynamic=True,
            show=False,
            placeholder="Click to authenticate",
        ),
        StrInput(
            name="auth_status",
            display_name="Auth Status",
            value="Not Connected",
            info="Current authentication status",
            dynamic=True,
            show=False,
            refresh_button=True
        ),
        # Non-tool mode inputs - explicitly set show=True
        DropdownInput(
            name="action",
            display_name="Action",
            # options=["GMAIL_SEND_EMAIL", "GMAIL_CREATE_EMAIL_DRAFT"],
            options=[],
            value="",
            info="Select Gmail action to perform",
            show=True,
            real_time_refresh=True,
        ),
        MessageTextInput(
            name="recipient_email",
            display_name="Recipient Email",
            required=True,
            info="Email address of the recipient",
            show=False,
            tool_mode=True
        ),
        MessageTextInput(
            name="subject",
            display_name="Subject",
            required=True,
            info="Subject of the email",
            show=False,
            tool_mode=True,
        ),
        MessageTextInput(
            name="body",
            display_name="Body",
            required=True,
            info="Content of the email",
            show=False,
            tool_mode=True,
        )
    ]

    outputs = [
        Output(
            name="text",
            display_name="Result",
            method="process_action"
        ),
    ]

    def process_action(self) -> Message:
        """Process Gmail action and return result as Message."""
        toolset = self._build_wrapper()

        if not hasattr(self, 'action') or not hasattr(self, 'recipient_email') or not hasattr(self, 'subject') or not hasattr(self, 'body'):
            msg = "Missing required fields"
            raise ValueError(msg)

        try:
            enum_name = getattr(Action, self.action)
            result = toolset.execute_action(
                action=enum_name,
                params={
                    "recipient_email": self.recipient_email,
                    "subject": self.subject,
                    "body": self.body
                }
            )
            self.status = result
            return Message(text=str(result))
        except Exception as e:
            logger.error(f"Error executing action: {e}")
            msg = f"Failed to execute {self.action}: {str(e)}"
            raise ValueError(msg) from e

    def update_build_config(self, build_config: dict, field_value: Any, field_name: str | None = None) -> dict:
        # Always show auth status
        build_config["auth_status"]["show"] = True
        build_config["auth_status"]["advanced"] = False

        # Handle action selection changes
        if field_name == "action":
            if field_value != "":
                build_config["recipient_email"]["show"] = True
                build_config["subject"]["show"] = True
                build_config["body"]["show"] = True

        # Handle authentication checks if API key is present
        if hasattr(self, "api_key") and self.api_key != "":
            build_config["action"]["options"] = ["GMAIL_SEND_EMAIL", "GMAIL_CREATE_EMAIL_DRAFT"]
            try:
                toolset = self._build_wrapper()
                entity = toolset.client.get_entity(id=self.entity_id)

                try:
                    # Check if already connected
                    entity.get_connection(app="gmail")
                    build_config["auth_status"]["value"] = "✅"
                    build_config["auth_link"]["show"] = False

                except NoItemsFound:
                    # Handle authentication
                    auth_scheme = self._get_auth_scheme("gmail")
                    if auth_scheme.auth_mode == "OAUTH2":
                        build_config["auth_link"]["show"] = True
                        build_config["auth_link"]["advanced"] = False
                        auth_url = self._initiate_default_connection(entity, "gmail")
                        build_config["auth_link"]["value"] = auth_url
                        build_config["auth_status"]["value"] = "Click link to authenticate"

            except Exception as e:
                logger.error(f"Error checking auth status: {e}")
                build_config["auth_status"]["value"] = f"Error: {e!s}"

        return build_config

    def _get_auth_scheme(self, app_name: str) -> AppAuthScheme:
        """Get the primary auth scheme for an app.

        Args:
        app_name (str): The name of the app to get auth scheme for.

        Returns:
        AppAuthScheme: The auth scheme details.
        """
        toolset = self._build_wrapper()
        try:
            return toolset.get_auth_scheme_for_app(app=app_name.lower())
        except Exception: # noqa: BLE001
            logger.exception(f"Error getting auth scheme for {app_name}")
            return None

    def _handle_auth_by_scheme(self, entity: Any, app: str, auth_scheme: AppAuthScheme) -> str:
        """Handle authentication based on the auth scheme.

        Args:
        entity (Any): The entity instance.
        app (str): The app name.
        auth_scheme (AppAuthScheme): The auth scheme details.

        Returns:
        str: The authentication status or URL.
        """
        auth_mode = auth_scheme.auth_mode

        try:
            # First check if already connected
            entity.get_connection(app=app)
        except NoItemsFound:
            # If not connected, handle new connection based on auth mode
            if auth_mode == "API_KEY":
                if hasattr(self, "app_credentials") and self.app_credentials:
                    try:
                        entity.initiate_connection(
                            app_name=app,
                            auth_mode="API_KEY",
                            auth_config={"api_key": self.app_credentials},
                            use_composio_auth=False,
                            force_new_integration=True,
                        )
                    except Exception as e: # noqa: BLE001
                        logger.error(f"Error connecting with API Key: {e}")
                        return "Invalid API Key"
                    else:
                        return f"{app} CONNECTED"
                return "Enter API Key"

            if (
                auth_mode == "BASIC"
                and hasattr(self, "username")
                and hasattr(self, "app_credentials")
                and self.username
                and self.app_credentials
            ):
                try:
                    entity.initiate_connection(
                        app_name=app,
                        auth_mode="BASIC",
                        auth_config={"username": self.username, "password": self.app_credentials},
                        use_composio_auth=False,
                        force_new_integration=True,
                    )
                except Exception as e: # noqa: BLE001
                    logger.error(f"Error connecting with Basic Auth: {e}")
                    return "Invalid credentials"
                else:
                    return f"{app} CONNECTED"
            elif auth_mode == "BASIC":
                return "Enter Username and Password"

            if auth_mode == "OAUTH2":
                try:
                    return self._initiate_default_connection(entity, app)
                except Exception as e: # noqa: BLE001
                    logger.error(f"Error initiating OAuth2: {e}")
                    return "OAuth2 initialization failed"

            return "Unsupported auth mode"
        except Exception as e: # noqa: BLE001
            logger.error(f"Error checking connection status: {e}")
            return f"Error: {e!s}"
        else:
            return f"{app} CONNECTED"

    def _initiate_default_connection(self, entity: Any, app: str) -> str:
        connection = entity.initiate_connection(app_name=app, use_composio_auth=True, force_new_integration=True)
        return connection.redirectUrl

    def _build_wrapper(self) -> ComposioToolSet:
        """Build the Composio toolset wrapper.

        Returns:
        ComposioToolSet: The initialized toolset.

        Raises:
        ValueError: If the API key is not found or invalid.
        """
        try:
            if not self.api_key:
                msg = "Composio API Key is required"
                raise ValueError(msg)
            return ComposioToolSet(api_key=self.api_key)
        except ValueError as e:
            logger.error(f"Error building Composio wrapper: {e}")
            msg = "Please provide a valid Composio API Key in the component settings"
            raise ValueError(msg) from e