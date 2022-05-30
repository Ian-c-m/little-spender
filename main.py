import disnake, config, tokens, random, sys, logging
from disnake.ext import commands
from datetime import datetime

#updates commands in given guild only, as this is a private bot.
bot = commands.InteractionBot(test_guilds = [config.live_guild_id])


#sets up log using the standard log library.
def setup_log():
    try:
        logging.basicConfig(
            format = "%(asctime)s %(levelname)-8s %(message)s",
            filename='helper-bot.log',
            encoding='utf-8',
            filemode='a',
            level = config.log_level,
            datefmt="%Y-%m-%d %H:%M:%S")
        logging.info("-----------")

    except Exception as e:
        print(f"ERROR - failed to setup log - {e}") 
        sys.exit()



#Logs once the bot is ready to receive commands, and sets the "Playing..." status.
@bot.event
async def on_ready():

    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")

    try:
        game = disnake.Game(config.status)
        await bot.change_presence(status = disnake.Status.online, activity = game)        

    except Exception as e:    
        logging.warning(f"Failed to set status correctly. {e}")

    
    logging.info(f"{config.bot_name} ready.")     



#An example slash command, will respond with a greeting when you use /hello
@bot.slash_command(description = "Says hello to you.")
async def hello(inter):

    
    try:
        greeting = random.choice(config.greetings)
        await inter.send(f"{greeting} {inter.author.mention}!")
        logging.debug(f"Said hello to {inter.author}")
        return
    
    except Exception as e:
        logging.exception(f"Failed to say hello to {inter.author}. {e}")
        await inter.send("This action failed, please try again.", ephemeral = True)
        return
    
    
#adds or removes a role when using the command. Used to access areas of the support server by bot/role.
@bot.slash_command(description = "Adds/removes a role.")
async def roles(
    inter, 
    role: disnake.Role = commands.Param(description="What role you want. You can only pick a 'user' role."), 
    remove: bool = commands.param(default=False, description="Whether to remove the role or not.")
    ):


    if remove == True:
    #the member wants to remove the role

        logging.info(f"{inter.author} tried to remove {role} role.")

        try:
            #remove the role
            await inter.author.remove_roles(role, reason = "Removed via slash command", atomic = False)
            logging.info(f"Succesfully removed {role} role from {inter.author}.")
            await inter.send(f"Succesfully removed {role} role from you.", ephemeral = True)
            return            
        
        except disnake.errors.Forbidden as e:
            #bot didn't have sufficient permissions to remove role.
            #Usually because the user was asking for a non-user role
            logging.info(f"Could not remove {role} from {inter.author}, invalid permissions.")
            await inter.send("Sorry, you're not authorised to remove that role.", ephemeral = True)
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

            #the member tried to add the server starter role but wasn't in the approved users list
            logging.info(f"{inter.author} tried to add the server starter role but wasn't in the approved user list.")
            await inter.send("Sorry, you're not authorised to have that role.", ephemeral = True)
            return


        elif role.name == config.server_starter_name and inter.author.id in config.approved_server_starter_users:

            #the member tried to add the server starter role and WAS in the approved users list
            try:
                #added the role to the member
                await inter.author.add_roles(role, reason = "Added via slash command", atomic = False)
                logging.info(f"Succesfully added {role} role to {inter.author}.")
                await inter.send(f"Succesfully gave you the {role} role.", ephemeral = True)
                return
            
            except disnake.errors.Forbidden as e:
                #bot didn't have sufficient permissions to add role.
                #Usually because the user was asking for a non-user role
                logging.info(f"Could not add {role} to {inter.author}, invalid permissions.")
                await inter.send("Sorry, you're not authorised to have that role.", ephemeral = True)
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
                logging.info(f"Succesfully added {role} role to {inter.author}.")
                await inter.send(f"Succesfully gave you the {role} role.", ephemeral = True)
                return                
            
            except disnake.errors.Forbidden as e:
                #bot didn't have sufficient permissions to add role.
                #Usually because the user was asking for a non-user role
                logging.info(f"Could not add {role} to {inter.author}, invalid permissions.")
                await inter.send("Sorry, you're not authorised to have that role.", ephemeral = True)
                return
            
            except Exception as e:
                #generic error
                logging.exception(f"Could not add {role} to {inter.author}. {e}.")
                await inter.send("This action failed, please try again.", ephemeral = True)
                return


    



if __name__ == "__main__":
    #setup the logger module
    setup_log()
    #run the main bot program
    bot.run(tokens.live_token)
