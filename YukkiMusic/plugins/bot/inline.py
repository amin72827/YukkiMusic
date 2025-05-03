#
# Copyright (C) 2024-2025 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#
from uuid import uuid4

from telethon import events
from telethon.extensions import markdown
from telethon.tl.types import (
    DocumentAttributeImageSize,
    InputBotInlineMessageMediaAuto,
    InputBotInlineResult,
    InputWebDocument,
    KeyboardButtonUrl,
    ReplyInlineMarkup,
)
from youtubesearchpython.__future__ import VideosSearch

from YukkiMusic import tbot
from YukkiMusic.misc import BANNED_USERS
from YukkiMusic.utils.inlinequery import answer


@tbot.on(events.InlineQuery(users=list(BANNED_USERS), blacklist_users=True))
async def inline_query_handler(event):
    text = event.query.query.strip().lower()
    answers = []
    if text.strip() == "":
        try:
            await event.answer(results=answer(), cache_time=10)
        except Exception:
            return
    else:
        a = VideosSearch(text, limit=20)
        result = (await a.next()).get("result")
        for x in range(15):
            title = (result[x]["title"]).title()
            duration = result[x]["duration"]
            views = result[x]["viewCount"]["short"]
            thumbnail = result[x]["thumbnails"][0]["url"].split("?")[0]
            channellink = result[x]["channel"]["link"]
            channel = result[x]["channel"]["name"]
            link = result[x]["link"]
            published = result[x]["publishedTime"]
            description = f"{views} | {duration} Mins | {channel}  | {published}"
            buttons = ReplyInlineMarkup(
                [
                    [
                        KeyboardButtonUrl(
                            text="🎥 ᴡᴀᴛᴄʜ ᴏɴ ʏᴏᴜᴛᴜʙᴇ",
                            url=link,
                        )
                    ],
                ]
            )
            searched_text = f"""
❇️**ᴛɪᴛʟᴇ:** [{title}]({link})

⏳**ᴅᴜʀᴀᴛɪᴏɴ:** {duration} Mins
👀**ᴠɪᴇᴡs:** `{views}`
⏰**ᴘᴜʙʟɪsʜᴇᴅ ᴛɪᴍᴇ:** {published}
🎥**ᴄʜᴀɴɴᴇʟ ɴᴀᴍᴇ:** {channel}
📎**ᴄʜᴀɴɴᴇʟ ʟɪɴᴋ:** [ᴠɪsɪᴛ ғʀᴏᴍ ʜᴇʀᴇ]({channellink})

__ʀᴇᴘʟʏ ᴡɪᴛʜ /play ᴏɴ ᴛʜɪs sᴇᴀʀᴄʜᴇᴅ ᴍᴇssᴀɢᴇ ᴛᴏ sᴛʀᴇᴀᴍ ɪᴛ ᴏɴ ᴠᴏɪᴄᴇᴄʜᴀᴛ.__

⚡️ ** ɪɴʟɪɴᴇ sᴇᴀʀᴄʜ ʙʏ {tbot.mention} **"""
            photo = InputWebDocument(
                url=thumbnail,
                size=0,
                mime_type="image/jpeg",
                attributes=[DocumentAttributeImageSize(w=0, h=0)],
            )
            msg, entities = markdown.parse(searched_text)

            answers.append(
                InputBotInlineResult(
                    id=str(uuid4()),
                    type="photo",
                    title=title,
                    content=photo,
                    thumb=photo,
                    description=description,
                    send_message=InputBotInlineMessageMediaAuto(
                        message=msg, entities=entities, buttons=buttons
                    ),
                )
            )
        try:
            return await event.answer(results=answers)
        except Exception:
            return
