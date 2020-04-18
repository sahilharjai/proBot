from datetime import datetime

from app import app
from app.services.googlesearch import GoogleSearch
from app.services.psql import DBService
from utilities.logger import LoggerManager

logger = LoggerManager.get_logger()

@app.event
async def on_ready():
    print(f'{app.user.name} has connected to Discord!')

@app.event
async def on_message(message):
    try:
        # check the message is not from Bot.
        if message.author == app.user:
            return


        # reply hey to users 'Hi'
        if message.content == 'hi':
            response = "hey"
        else:
            # split the message.
            contents = message.content.split()

            # size of the message to be greater than 2 words
            if len(contents) > 1:

                # retrieve searched item from message
                searched_item = ' '.join(contents[1:])
                db_conn = DBService()

                # searching from google column.
                if '!google' in contents:
                    logger.info("Google Search for contents: {} from username: {}".format(
                        searched_item, message.author.name))
                    try:
                        # adding searched google query in db.
                        db_conn.add_record(
                            add_record=(
                                searched_item,
                                message.author.name,
                                str(datetime.now()))
                            )
                        # searching through google search api.
                        data = GoogleSearch.search(searched_item)
                        response = "Found Some Links for Your Query:\n" + data
                    except Exception as e:
                        response = "Error Found during Google Search for contents: {} with error_details: {}".format(
                            contents, str(e))
                        logger.error(response)
                elif '!recent' in contents:
                    try:
                        logger.info("Recent Search for contents: {} from username: {}".format(
                            searched_item, message.author.name))

                        # searching in db for searched query.
                        data = db_conn.search_query(query=searched_item)

                        if any(data):
                            response = "Result for your search:\n"
                            count = 1
                            for each in data:
                                response += str(count) + ". Content: {} -- By: {}\n".format(each[0], each[1])
                                count += 1
                        else:
                            response = "No Result Found for your query."
                    except Exception as e:
                        response = "Error Found during Recent Search for contents: {} with error_details: {}".format(
                            contents, str(e))
                        logger.error(response)
                else:
                    response = "Message not found."
            else:
                response = "Message not found."
        await message.channel.send(response)
    except Exception as e:
        msg ="Bot Down: Due to error: {}".format(str(e))
        logger.error(msg)
        await message.channel.send(msg)
