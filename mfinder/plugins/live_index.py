from pyrogram import Client, filters
from mfinder import DB_CHANNELS, LOGGER
from mfinder.db.files_sql import save_file
from mfinder.utils.helpers import edit_caption
from mfinder.plugins.start_cmd import START_INDEX_AFTER  # import the global variable

media_filter = filters.document | filters.video | filters.audio


@Client.on_message(filters.chat(DB_CHANNELS) & media_filter)
async def live_index(bot, message):
    try:
        # Skip messages before START_INDEX_AFTER
        if message.message_id <= START_INDEX_AFTER:
            return

        for file_type in ("document", "video", "audio"):
            media = getattr(message, file_type, None)
            if not media:
                continue  # changed from break to continue to check other types

            file_name = media.file_name
            file_name = edit_caption(file_name)
            media.file_type = file_type
            media.caption = file_name
            await save_file(media)

    except Exception as e:
        LOGGER.warning("Error occurred while saving file: %s", str(e))
