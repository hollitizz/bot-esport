import logging
from discord import Interaction
from utils.createSelect import createViewForSelect
from utils.getChannelByName import getChannelByName

from utils.types import BotType

SORT_ORDER = {
    'fr-FR': [
        'INTERNATIONAL',
        'EMEA',
        'CORÉE',
        'CHINE',
        'AMÉRIQUE DU NORD',
        'TURQUIE',
        'COMMUNAUTÉ DES ÉTATS INDÉPENDANTS',
        'AMÉRIQUE LATINE',
        'AMÉRIQUE LATINE NORD',
        'AMÉRIQUE LATINE SUD',
        'VIETNAM',
        'OCÉANIE',
        'HONG KONG, MACAO, TAÏWAN',
        'JAPON',
        'BRÉSIL',
    ],
    'en-US': [
        'INTERNATIONAL',
        'EMEA',
        'KOREA',
        'CHINA',
        'NORTH AMERICA',
        'TURKEY',
        'COMMONWEALTH OF INDEPENDENT STATES',
        'LATIN AMERICA',
        'LATIN AMERICA NORTH', 'LATIN AMERICA SOUTH',
        'VIETNAM',
        'OCEANIA',
        'HONG KONG, MACAU, TAIWAN',
        'JAPAN',
        'BRAZIL',
    ]}


async def setupPlanningSender(bot: BotType, ctx: Interaction, channel_id: str):
    if channel_id.isdigit():
        channel = ctx.guild.get_channel(int(channel_id))
    else:
        channel = getChannelByName(bot, ctx.guild.id, channel_id)
    if channel is None:
        await ctx.response.send_message("Channel not found", ephemeral=True)
        return
    bot.db.updateGuildSchedulerChannel(ctx.guild.id, channel.id)
    language = bot.db.getGuildPreferredLanguage(ctx.guild.id)
    leagues: list[dict] = bot.api.getLeagues(
        language
    ).get("data", {}).get("leagues", [])

    leagues.sort(key=lambda x: SORT_ORDER.get(
        language, []
    ).index(x.get("region", "")))
    await ctx.response.send_message(view=createViewForSelect(
        [
            {
                'label': league.get("name", ""),
                'value': league.get("id", ""),
                'description': league.get("region", ""),
            } for league in leagues
        ],
        bot.db.updateGuildFollowedLeagues,
    ), ephemeral=True)
