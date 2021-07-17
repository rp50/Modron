from dotenv import load_dotenv
import discord, logging, os, re, datetime

logging.basicConfig(level=logging.INFO)
load_dotenv()
bot_token = os.getenv('DISCORD_BOT_TOKEN')

botClient = discord.Client()

async def quest_command(message, args):
    quest = {}
    quest['title'] = args[1]
    dateOf = datetime.date(datetime.datetime.now().year, int(args[3]), int(args[4]))
    timeOf = datetime.time(int(args[6]), int(args[7]))
    quest['time'] = timeOf
    if dateOf < datetime.datetime.now().date():
        dateOf = datetime.date(datetime.datetime.now().year+1, dateOf.month, dateOf.day)
    quest['date'] = dateOf
    quest['creator'] = message.author

    questResponse = discord.Embed(title = quest['title'])
    questResponse.add_field(name='Creator', value=quest['creator'].mention)
    questResponse.add_field(name='Scheduled For:', value=quest['date'].strftime('%A, %m/%d')+ ' @ '+quest['time'].strftime('%H:%S'))
    questResponse.set_footer(text='React with a %s to join.' % u'\U00002705')
    
    await message.channel.send(embed = questResponse)

#reads commands in and directs to the correct command
async def cmd_reader(message):
    msg = message.content
    if msg.startswith('$quest '):
        questRegex = re.compile(r'("(.{1,})") (([0-1]\d)\/(\d{2})) (([0-1]\d)\:(\d{2}))')
        questArgs = re.match(questRegex, msg[7:])
        if questArgs:
            await quest_command(message, questArgs.groups())
        else:
            await message.channel.send('Incorrect format for the $quest command')


@botClient.event
async def on_ready():
    print('Logged in as {}'.format(botClient.user))

@botClient.event
async def on_message(message):
    if message.author != botClient.user and message.content.startswith('$'):
        await cmd_reader(message)

botClient.run(bot_token)