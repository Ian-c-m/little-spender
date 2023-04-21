import disnake, config, tokens, sys, logging
from disnake.ext import commands
from datetime import datetime

#updates commands in given guild only, as this is a private bot.
bot = commands.InteractionBot(test_guilds = [config.test_guild_id], intents=disnake.Intents.all())


#########################################################################################
#    STARTUP FUNCTIONS BELOW

#sets up logging using the standard logging library. Configure the level in the config.py file.
def setup_logging():
    try:
        logging.basicConfig(
            format = "%(asctime)s %(levelname)-8s %(message)s",
            filename=config.log_file,
            encoding="utf-8",
            filemode=config.logging_filemode,
            level = config.logging_level,
            datefmt="%Y-%m-%d %H:%M:%S")
        logging.info("-----------")
        

    except Exception as e:
        print(f"ERROR - failed to setup logging - {e}")
        sys.exit()

#Alerts once the bot is ready to receive commands
@bot.event
async def on_ready():
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    try:
        
        game = disnake.Game(config.status)
        await bot.change_presence(status = disnake.Status.online, activity = game)
        logging.info(f"{config.bot_name} ready.")
        #print(f"{config.bot_name} ready.")
        

    except Exception as e:
        logging.warning(f"Failed to set status correctly. {e}")





#########################################################################################
#    MAIN FUNCTIONS BELOW

#Use the new UI buttons to assign roles
@bot.event
async def on_message(message: disnake.Message):

    if message.content == "!role" and message.author.id == 195617048569708545:
        space = disnake.ui.Button(label=config.spacebot_role, emoji="🚀")
        confession = disnake.ui.Button(label=config.confession_role, emoji="💭")
        detective = disnake.ui.Button(label=config.alt_text_role, emoji="🔍")

        role_view = disnake.ui.View()
        role_view.add_item(space)
        role_view.add_item(confession)
        role_view.add_item(detective)

        await message.channel.send("Please select a role to gain access to the channels for that bot.", view = role_view)
        logging.info(f"Added a role selection message to {message.channel}")


@bot.event
async def on_message_interaction(inter: disnake.MessageInteraction):

    for role in inter.guild.roles:
        if role.name == config.spacebot_role:
            spacebot_role = role

        if role.name == config.confession_role:
            confession_role = role

        if role.name == config.alt_text_role:
            alt_text_role = role



    if inter.component.label == config.spacebot_role:     
        if spacebot_role in inter.author.roles:
            await inter.author.remove_roles(spacebot_role, reason="Self assigned from role select options.")
            await inter.send(f"Removed {spacebot_role.name} from you", ephemeral=True)
            logging.info(f"Removed {spacebot_role.name} from {inter.author}")
        else:
            await inter.author.add_roles(spacebot_role, reason="Self assigned from role select options.")
            await inter.send(f"Added {spacebot_role.name} to you", ephemeral=True)
            logging.info(f"Removed {spacebot_role.name} from {inter.author}")

    if inter.component.label == config.confession_role:
        if confession_role in inter.author.roles:
            await inter.author.remove_roles(confession_role, reason="Self assigned from role select options.")
            await inter.send(f"Removed {confession_role.name} from you", ephemeral=True)
            logging.info(f"Removed {confession_role.name} from {inter.author}")
        else:
            await inter.author.add_roles(confession_role, reason="Self assigned from role select options.")
            await inter.send(f"Added {confession_role.name} to you", ephemeral=True)
            logging.info(f"Removed {confession_role.name} from {inter.author}")

    if inter.component.label == config.alt_text_role:
        if alt_text_role in inter.author.roles:
            await inter.author.remove_roles(alt_text_role, reason="Self assigned from role select options.")
            await inter.send(f"Removed {alt_text_role.name} from you", ephemeral=True)
            logging.info(f"Removed {alt_text_role.name} from {inter.author}")
        else:
            await inter.author.add_roles(alt_text_role, reason="Self assigned from role select options.")
            await inter.send(f"Added {alt_text_role.name} to you", ephemeral=True)
            logging.info(f"Removed {alt_text_role.name} from {inter.author}")




if __name__ == "__main__":
    #setup the logger module
    setup_logging()
    #run the main bot program
    bot.run(tokens.discord_test_token)
