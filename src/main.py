import logging
from typing import Annotated

from fastmcp import FastMCP

from telegram import Bot
from telegram.error import TelegramError


import envs

logger = logging.getLogger(__name__)


mcp_server = FastMCP(name="telegram-mcp-server")


@mcp_server.tool
async def send_message_to_user(
    chat_id: Annotated[int, "Telegram chat/user id to send the message to"],
    message: Annotated[str, "Text content to send"],
) -> str:
    """Send a message to a specific Telegram user."""
    logger.info(f"Sending message to user {chat_id}: {message}")
    bot = Bot(token=envs.TELEGRAM_BOT_TOKEN)

    try:
        await bot.send_message(chat_id=chat_id, text=message)
    except TelegramError as exc:
        return f"Failed to send message: {exc}"

    return "Message sent successfully"


def main():
    mcp_server.run(
        transport="http",
        host=envs.MCP_HOST,
        port=envs.MCP_PORT,
    )


if __name__ == "__main__":
    main()
