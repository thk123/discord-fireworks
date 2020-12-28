
import os
import sys
import threading

import discord
import pyglet
from dotenv import load_dotenv

from firework_parsing import firework_parsing


def extract_message(message_body, prefix):
    if message_body.lower().startswith(prefix.lower()):
        return str.strip(message_body[len(prefix):])
    return None

def main():
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    client = discord.Client()

    from window import window
    draw_thread = threading.Thread(target=lambda: window.run(None))
    draw_thread.start()


    @client.event
    async def on_ready():
        print(f'{client.user} has connected to Discord!')
        for guild in client.guilds:
            print('The following guilds are using the server: ' + str(guild))

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        # We're only interested in messages in the #fireworks channels (allow for
        # #fireworks-testing
        if 'fireworks' not in message.channel.name:
            return

        if client.user not in message.mentions:
            return
        no_exclaimations = message.content.replace('!', '')
        command = extract_message(no_exclaimations, client.user.mention)

        firework = firework_parsing.parse_firework(command)
        if firework is None:
            print(f'Unrecognised command: {command}', file=sys.stderr)
            await message.add_reaction('❌')
        else:
            pyglet.clock.schedule_once(firework, 0)
            await message.add_reaction('🎇')

    client.run(TOKEN)


if __name__ == "__main__":
    main()