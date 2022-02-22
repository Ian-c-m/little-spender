import logging, disnake, config, tokens, random
from disnake.ext import commands
from datetime import datetime

bot = commands.Bot(test_guilds = [config.test_guild_id, config.live_guild_id])


#sets up logging using the standard logging library. Configure the level in the config.py file.
def setup_logging():
    try:
        logging.basicConfig(
            format = "%(asctime)s %(levelname)-8s %(message)s",
            filename='bot.log',
            encoding='utf-8',
            filemode='a',
            level = config.logging_level,
            datefmt="%Y-%m-%d %H:%M:%S")
        logging.info("-----------")
        #print('Setup logging correctly.')

    except Exception as e:
        print(f"ERROR - failed to setup logging - {e}") 



#Alerts once the bot is ready to receive commands, and sets the "Playing..." status.
@bot.event
async def on_ready():
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")

    try:
        game = disnake.Game(config.status)
        await bot.change_presence(status = disnake.Status.online, activity = game)        

    except Exception as e:
        print(f"{now} WARNING     failed to set status correctly.")    

    print(f"{now} INFO     {config.bot_name} ready")     


#An example slash command, will respond World when you use /hello
@bot.slash_command(description = "Says hello to you.")
async def hello(inter):

    try:
        greeting = random.choice(config.greetings)
        await inter.send(f"{greeting} {inter.author.mention}!")
        logging.info(f"Said hello to {inter.author}")
        return
    
    except Exception as e:
        logging.exception(f"Failed to say hello to {inter.author}. {e}")
        await inter.send("This action failed, please try again.", ephemeral = True)
        return
    
    

@bot.slash_command(description = "Adds/removes a role.")
async def roles(inter, role: disnake.Role, remove: bool):

    if remove == True:
    #the member wants to remove the role

        logging.info(f"{inter.author} tried to remove {role} role.")
        #TODO: do we care if the user was not approved for limited roles and tried to remove it?
        try:
            await inter.author.remove_roles(role, reason = "Removed via slash command", atomic = False)
            logging.info(f"Succesfully removed {role} role from {inter.author}.")
            await inter.send(f"Succesfully removed {role} role from you.", ephemeral = True)
            return
            
        
        except disnake.errors.Forbidden as e:
            #bot didn't have sufficient permissions to remove role.
            logging.exception(f"Could not remove {role} from {inter.author}, invalid permissions.")
            await inter.send("This action failed, please try again.", ephemeral = True)
            return
        
        except Exception as e:
            #generic error
            logging.exception(f"Could not remove {role} from {inter.author}. {e}")
            await inter.send("This action failed, please try again.", ephemeral = True)
            return



    elif remove == False:
    #the member wants to add the role
    
        logging.info(f"{inter.author} tried to add {role} role.")



        #only approved users can have the server starter role
        if role.name == config.server_starter_name and inter.author.id not in config.approved_server_starter_users:
            #if we're here, then the member tried to add the server starter role but wasn't in the approved users list
            logging.warning(f"{inter.author} tried to add the server starter role but wasn't authorised.")
            await inter.send("Sorry, you're not authorised to have that role.", ephemeral = True)
            return


        elif role.name == config.server_starter_name and inter.author.id in config.approved_server_starter_users:
            #if we're here then the member tried to add the server starter role and WAS in the approved users list
            try:
                await inter.author.add_roles(role, reason = "Added via slash command", atomic = False)
                logging.info(f"Succesfully added {role} role from {inter.author}.")
                await inter.send(f"Succesfully gave you the {role} role.", ephemeral = True)
                return
            
            except disnake.errors.Forbidden as e:
                #bot didn't have sufficient permissions to add role.
                logging.exception(f"Could not add {role} to {inter.author}, invalid permissions.")
                await inter.send("This action failed, please try again.", ephemeral = True)
                return
        
            except Exception as e:
                #generic error
                logging.exception(f"Could not add {role} to {inter.author}. {e}.")
                await inter.send("This action failed, please try again.", ephemeral = True)
                return


        else:
            #adding other generic roles.
            try:
                await inter.author.add_roles(role, reason = "Added via slash command", atomic = False)
                logging.info(f"Succesfully added {role} role from {inter.author}.")
                await inter.send(f"Succesfully gave you the {role} role.", ephemeral = True)
                return
                
            
            except disnake.errors.Forbidden as e:
                #bot didn't have sufficient permissions to add role.
                logging.exception(f"Could not add {role} to {inter.author}, invalid permissions.")
                await inter.send("This action failed, please try again.", ephemeral = True)
                return
            
            except Exception as e:
                #generic error
                logging.exception(f"Could not add {role} to {inter.author}. {e}.")
                await inter.send("This action failed, please try again.", ephemeral = True)
                return


    



if __name__ == "__main__":
    setup_logging()
    bot.run(tokens.live_token)
