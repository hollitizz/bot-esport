
import datetime
from io import BytesIO
import os
from PIL import Image, ImageDraw
import pytz
import requests
from utils.planningConst import *
import logging


_logger = logging.getLogger(__name__)


def splitAmPm(datas: list[dict], tz: pytz.timezone):
    am = []
    pm = []
    for data in datas:
        time = datetime.datetime.fromisoformat(
            data['startTime']).astimezone(tz)
        if time.hour < 12:
            am.append(data)
        else:
            pm.append(data)
    return am, pm


def drawGame(
    x: int,
    y: int,
    timetable: Image,
    teams: tuple[str, str],
):
    for team in teams:
        if os.path.exists(f"assets/teamsIcons/{team['code']}.png"):
            img = Image.open(
                f"assets/teamsIcons/{team['code']}.png").resize(icon_size)
        else:
            img = Image.open(BytesIO(requests.get(team['image']).content))
            img.save(f"assets/teamsIcons/{team['code']}.png")
            _logger.info(f"Saved logo of {team['code']}")
            img = img.resize(icon_size)
        timetable.paste(img, (x, y), img)
        x += icon_b + margin


def drawSeparator(
    x: int,
    y: int,
    img_draw: ImageDraw,
    padding_top: int
):
    img_draw.line(
        (x + margin, y + icon_b + padding_top,
         x + line_len, y + icon_b + padding_top),
        fill=white,
        width=line_width
    )


def drawHour(
    x: int,
    y: int,
    img_draw: ImageDraw,
    padding_top: int,
    time: str,
    tz: pytz.timezone
):
    time = datetime.datetime.fromisoformat(
        time
    ).astimezone(tz).strftime("%H:%M")
    img_draw.text(
        (x + margin, y + icon_b / 2 + padding_top),
        time,
        font=hour_font,
        fill=white
    )


def drawLeadingLeague(
    x: int,
    y: int,
    timetable: Image,
    img_draw: ImageDraw,
    padding_top: int,
    league: dict,
    time: str,
    tz: pytz.timezone
):
    img = Image.open(f"assets/leaguesIcons/{league}.png").resize(icon_size)
    timetable.paste(
        img,
        (int(x + content_x / 2 - icon_b / 2) +
         league_icon_margin, y + padding_top),
        img
    )
    drawHour(x, y, img_draw, padding_top, time, tz)
    drawSeparator(x, y, img_draw, padding_top)


def drawHalfDayMatches(
    data: list[dict],
    week_day: int,
    timetable: Image,
    img_draw: ImageDraw,
    is_am: bool,
    tz: pytz.timezone
):
    last_league = None
    py = 0 if is_am else content_y - (len(data) + 1) * (icon_b + margin)

    for data_index, data in enumerate(data):
        match = data['match']
        x = left + margin + (content_x + margin) * week_day
        y = top + (icon_b + margin) * data_index + py
        if last_league != data['league']:
            last_league = data['league']
            padding_top = 0 if data_index == 0 else title_bot_margin
            py += icon_b + margin + padding_top
            drawLeadingLeague(
                x, y,
                timetable,
                img_draw,
                padding_top,
                last_league['slug'],
                data['startTime'],
                tz
            )
            y += icon_b + margin + padding_top
        if week_day != 0:
            x += 5
        drawGame(
            x, y,
            timetable,
            match['teams']
        )


def getFormattedPlanning(language, timezone, schedules):
    timetable = Image.open(f'assets/{language}_timetable.png')
    tz = pytz.timezone(timezone)
    img_draw: ImageDraw = ImageDraw.Draw(timetable)
    for date, datas in schedules.items():
        week_day = datetime.date.fromisoformat(date).weekday()
        am, pm = splitAmPm(datas, tz)
        drawHalfDayMatches(am, week_day, timetable, img_draw, True, tz)
        drawHalfDayMatches(pm, week_day, timetable, img_draw, False, tz)
    return timetable
