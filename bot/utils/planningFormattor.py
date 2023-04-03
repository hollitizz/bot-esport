
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
        if data.get('type') == 'show':
            continue
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
    img_draw: ImageDraw,
    is_completed: bool,
    teams: tuple[str, str],
):
    for team in teams:
        if os.path.exists(f"assets/teamsIcons/{team['code']}.png"):
            img = Image.open(
                f"assets/teamsIcons/{team['code']}.png").resize(icon_size)
        else:
            img = Image.open(BytesIO(requests.get(team['image']).content))
            img.save(f"assets/teamsIcons/{team['code']}.png", "PNG")
            img = img.resize(icon_size)
        if is_completed and team['result']['outcome'] == 'loss':
            A = img.getchannel('A')
            newA = A.point(lambda i: 128 if i > 100 else 0)
            img.putalpha(newA)
        _pasteImg(timetable, img_draw, img, x, y, team['name'])
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


def _pasteImg(
    timetable: Image,
    img_draw: ImageDraw,
    img: Image,
    x: int,
    y: int,
    replacement_text: str
):
    try:
        timetable.paste(img, (int(x), int(y)), img)
    except ValueError:
        _logger.error(f"Error while pasting {img}")
        img_draw.text(
            (int(x), int(y)),
            replacement_text,
            font=font,
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
    _pasteImg(
        timetable,
        img_draw,
        img,
        x + content_x / 2 - icon_b / 2 + league_icon_margin,
        y + padding_top,
        league
    )
    drawHour(x, y, img_draw, padding_top, time, tz)
    drawSeparator(x, y, img_draw, padding_top)


def drawFooterLeague(
    x: int,
    y: int,
    img_draw: ImageDraw,
    bo_size: int
):
    x -= left
    text = f"BO {bo_size}"
    _, _, w, _ = img_draw.textbbox((0, 0), text, font=hour_font)
    img_draw.text(
        (
            x + content_x / 2 - w / 2,
            y + icon_b / 2
        ),
        text,
        font=hour_font,
        fill=white
    )


def howManyBoNot1(data: list[dict]):
    count = 0
    for data in data:
        if data['match']['strategy']['count'] > 1:
            count += 1
    return count

def howManyLeagues(data: list[dict]):
    count = 0
    last_league = None
    for data in data:
        if last_league != data['league']:
            count += 1
            last_league = data['league']
    return count

def drawHalfDayMatches(
    data: list[dict],
    week_day: int,
    timetable: Image,
    img_draw: ImageDraw,
    is_am: bool,
    tz: pytz.timezone
):
    last_league = None
    bo_size = 1
    how_many_leagues = howManyLeagues(data)
    if is_am:
        py = 0
    else:
        py = content_y - (
            len(data) * (icon_b + margin) + bo_text_height * howManyBoNot1(data) + how_many_leagues * (icon_b - 15)
        )

    for data_index, data in enumerate(data):
        match = data['match']
        x = left + margin + (content_x + margin) * week_day
        y = top + (icon_b + margin) * data_index + py
        if last_league != data['league']:
            if bo_size > 1:
                drawFooterLeague(
                    x, y - icon_b / 2 - margin,
                    img_draw,
                    bo_size
                )
            last_league = data['league']
            bo_size = match['strategy']['count']
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
            img_draw,
            data['state'] == 'completed',
            match['teams']
        )
    if bo_size > 1:
        y = top + (icon_b + margin) * (data_index) + py + icon_b / 2
        drawFooterLeague(
            x, y,
            img_draw,
            bo_size
        )


def getFormattedPlanning(language: str, timezone: pytz.timezone, schedules: dict):
    timetable = Image.open(f'assets/{language}_timetable.png')
    tz = pytz.timezone(timezone)
    img_draw: ImageDraw = ImageDraw.Draw(timetable)
    for date, datas in schedules.items():
        week_day = datetime.date.fromisoformat(date).weekday()
        am, pm = splitAmPm(datas, tz)
        drawHalfDayMatches(am, week_day, timetable, img_draw, True, tz)
        drawHalfDayMatches(pm, week_day, timetable, img_draw, False, tz)
    return timetable
