from discord import Interaction

async def ping(ctx: Interaction):
    await ctx.response.send_message("Pong !", ephemeral=True)
