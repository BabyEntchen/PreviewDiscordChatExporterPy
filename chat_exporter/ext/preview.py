import discord
from typing import List, Optional
from string_py import Format


def generate_embed(embed: dict):
    try:
        embed = Format.embed(
            title=embed.get("title"),
            description=embed.get("description"),
            footer=embed.get("footer"),
            author=embed.get("author"),
            image=embed.get("image"),
            fields=embed.get("fields")
        )
    except Exception as e:
        embed = f"Error generating embed: {e}\nEmbed data: {embed}"
    return embed


class Preview:
    def __init__(self,
                 channel: discord.TextChannel,
                 limit: Optional[int],
                 pytz_timezone,
                 messages: Optional[List[discord.Message]] = None,
                 ):
        self.channel = channel
        self.messages = messages
        self.limit = int(limit) if limit else None
        self.pytz_timezone = pytz_timezone


    @staticmethod
    async def generate_message(raw_message: discord.Message):
        generated_message = f"{raw_message.author} - {raw_message.created_at.strftime('%a %d %b %Y, %I:%M%p')}:\n"
        if raw_message.content:
            generated_message += f"{raw_message.content}\n"
        if raw_message.embeds:

            generated_message += "Embeds:\n"
            for embed in raw_message.embeds:
                generated_message += generate_embed(embed.to_dict())
                generated_message += "\n"

        if raw_message.attachments:
            generated_message += "Attachments:\n"
            for attachment in raw_message.attachments:
                generated_message += attachment.url + "\n"

        try:
            message = Format.surround(generated_message)
        except Exception as e:
            message = f"Error generating message: {e}\nMessage data: {generated_message}"
        return message

    async def build_preview(self):
        if not self.messages:
            self.messages = reversed(await self.channel.history(limit=self.limit).flatten())
        preview = "<!-- Preview:\n\n"
        for message in self.messages:
            preview += await self.generate_message(message) + "\n"
        return "\n" + preview + "End of Preview -->\n\n"
