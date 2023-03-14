from utils.types import Setup
from discord import Interaction, SelectOption, ui, app_commands, Embed


def getCommandFormattedEmbed(ctx: Interaction, command: app_commands.Command, group_name: str):
    embed: Embed = Embed(title=group_name, url="", description=f"Help for the command `{command.name}`", color=0xff4013)
    embed.set_author(name="Hollitizz", url="https://discordapp.com/users/222008900025581568", icon_url="https://cdn.discordapp.com/avatars/222008900025581568/e4bc396801ccadf364d2907869404844.png")
    embed.add_field(name="Description", value=f"{command.description}", inline=False)
    arguments = ""
    params = ""
    for param in command.parameters:
        params += f"`{param.name}` "
        arguments += f"`{param.name}`: {param.description}{' (Required)' if param.required else ''}\n"
    params = params[:-1]
    if arguments != "":
        embed.add_field(name="Arguments", value=arguments, inline=False)
    embed.add_field(name="Usage", value=f"/{command.name} {params}", inline=False)
    return embed


class drawHelpSelect(ui.Select):
    def __init__(self, items, cog_name):
        self.cogs_options = [SelectOption(label=item.name, value=i) for i, item in enumerate(items)]
        super().__init__(
            placeholder="Choose a command", options=self.cogs_options)
        self.items = items
        self.cog_name = cog_name

    async def callback(self, ctx: Interaction):
        await ctx.response.edit_message(content=f"", embed=getCommandFormattedEmbed(ctx, self.items[int(self.values[0])], self.cog_name), view=None)


class drawHelpView(ui.View):
    def __init__(self, items, cog_name):
        super().__init__()
        self.add_item(drawHelpSelect(items, cog_name))

class drawCogSelect(ui.Select):
    def __init__(self, items):
        self.cogs_options = [SelectOption(label=f"{item_name}", value=item_name) for item_name, item in items.items()]
        super().__init__(
            placeholder="Choose a category", options=self.cogs_options)
        self.items = items

    async def callback(self, ctx: Interaction):
        await ctx.response.edit_message(view=drawHelpView(self.items[self.values[0]].get_app_commands(), self.values[0]))


class drawCogView(ui.View):
    def __init__(self, items):
        super().__init__()
        self.add_item(drawCogSelect(items))


async def help(self: Setup, ctx: Interaction):
    await ctx.response.send_message("Help menu", ephemeral=True, view=drawCogView(self.cogs))
