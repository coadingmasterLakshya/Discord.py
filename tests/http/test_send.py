import pytest

from discord import Route
from discord.types import components, embed, message, sticker

from ..core import client
from .core import (
    channel_id,
    random_allowed_mentions,
    random_embed,
    random_message_reference,
    random_sticker,
    user_id,
)


@pytest.fixture(params=(None, "Hello, World!"))
def content(request) -> str | None:
    return request.param


@pytest.fixture(params=(True, False))
def tts(request) -> bool:
    return request.param


@pytest.fixture(name="embed", params=(None, random_embed()))
def _embed(request) -> embed.Embed | None:
    return request.param


@pytest.fixture(params=(None, [random_embed() for _ in range(10)]))
def embeds(request) -> list[embed.Embed] | None:
    return request.param


@pytest.fixture(params=(None, "..."))  # TODO: Replace string value
def nonce(request) -> str | None:
    return request.param


@pytest.fixture(params=(None, random_allowed_mentions()))
def allowed_mentions(request) -> message.AllowedMentions | None:
    return request.param


@pytest.fixture(params=(None, random_message_reference()))
def message_reference(request) -> message.MessageReference | None:
    return request.param


@pytest.fixture(params=(None, [random_sticker() for _ in range(10)]))
def stickers(request) -> list[sticker.StickerItem] | None:
    return request.param


@pytest.fixture(params=(None,))  # TODO: Add components to send tests
def components(request) -> components.Component | None:
    return request.param


@pytest.fixture(params=(None,))  # TODO: Add flags to send tests
def flags(request) -> int | None:
    return request.param


async def test_send_message(
    client,
    channel_id,
    content,
    tts,
    embed,
    embeds,
    nonce,
    allowed_mentions,
    message_reference,
    stickers,
    components,
    flags,
):
    payload = {
        "content": content,
        "tts": tts,
        "embeds": embeds
        if embeds is not None
        else [embed]
        if embed is not None
        else None,
        "nonce": nonce,
        "allowed_mentions": allowed_mentions,
        "message_reference": message_reference,
        "sticker_ids": stickers,
        "components": components,
        "flags": flags,
    }
    for key, value in list(payload.items()):
        if key == "tts":
            if not value:
                del payload[key]
        else:
            if value is None:
                del payload[key]
    with client.makes_request(
        Route("POST", "/channels/{channel_id}/messages", channel_id=channel_id),
        json=payload,
    ):
        await client.http.send_message(
            channel_id,
            content,
            tts=tts,
            embed=embed,
            embeds=embeds,
            nonce=nonce,
            allowed_mentions=allowed_mentions,
            message_reference=message_reference,
            stickers=stickers,
            components=components,
            flags=flags,
        )


async def test_send_typing(client, channel_id):
    """Test sending typing."""
    with client.makes_request(
        Route("POST", "/channels/{channel_id}/typing", channel_id=channel_id),
    ):
        await client.http.send_typing(channel_id)
