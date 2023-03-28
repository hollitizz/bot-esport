import discord

class createSelect(discord.ui.Select):
    def __init__(
        self,
        options: list[dict],
        update_function,
        selected_leagues: list[str],
        allow_multiple_selection: bool = False,
        timeout: int = 60
    ):
        self.update_function = update_function
        self.selected_leagues = selected_leagues
        super().__init__(
            placeholder="Select a league",
            min_values=0,
            max_values=len(options) if allow_multiple_selection else 1,
            options=[
                discord.SelectOption(
                    label=option.get("label", ""),
                    value=option.get("value", ""),
                    description=option.get("description", ""),
                ) for option in options
            ],
        )

    async def callback(self, ctx: discord.Interaction):
        self.selected_leagues.extend(self.values)
        self.selected_leagues = list(set(self.selected_leagues))
        self.update_function(ctx.guild.id, self.selected_leagues)
        await ctx.response.defer()

class createViewForSelect(discord.ui.View):
    def __init__(self, in_options: list[dict], update_function, allow_multiple_selection: bool = True, timeout: int = 60):
        super().__init__()
        split_options = [in_options[i:i + 25] for i in range(0, len(in_options), 25)]
        self.selected_leagues = []
        for options in split_options:
            self.add_item(createSelect(
                options,
                update_function,
                self.selected_leagues,
                allow_multiple_selection=allow_multiple_selection,
                timeout=timeout
            ))
