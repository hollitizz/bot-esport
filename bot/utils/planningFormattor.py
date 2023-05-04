import datetime
from io import BytesIO
import os
from PIL import Image, ImageDraw
from PIL.Image import Image as ImageType
from PIL.ImageDraw import ImageDraw as ImageDrawType
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


def drawSeparator(
    x: int,
    y: int,
    img_draw: ImageDrawType,
    padding_top: int
):
    img_draw.line(
        (x + margin, y + icon_b + padding_top,
         x + separator_len, y + icon_b + padding_top),
        fill=white,
        width=line_width
    )


def drawHour(
    x: int,
    y: int,
    img_draw: ImageDrawType,
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
    timetable: ImageType,
    img_draw: ImageDrawType,
    img: ImageType,
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
    timetable: ImageType,
    img_draw: ImageDrawType,
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
    img_draw: ImageDrawType,
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


def howManyBoNot1(datas: dict[list[dict]]):
    count = 0
    for data in datas.values():
        if data[0]['match']['strategy']['count'] > 1:
            count += 1
    return count


def howManyLeaguesAndBo(datas: dict[list[dict]]):
    leagues_count = 0
    not_bo_1_count = 0
    last_league = None
    for data in datas.values():
        if last_league != data[0]['league']:
            if data[0]['match']['strategy']['count'] > 1:
                not_bo_1_count += 1
            leagues_count += 1
            last_league = data[0]['league']
    return leagues_count, not_bo_1_count


def drawGame(
    x: int,
    y: int,
    timetable: ImageType,
    img_draw: ImageDrawType,
    is_completed: bool,
    teams: tuple[str, str],
    size: tuple[int, int] = icon_size
):
    for team in teams:
        if os.path.exists(f"assets/teamsIcons/{team['code']}.png"):
            img = Image.open(
                f"assets/teamsIcons/{team['code']}.png")
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
                img.save(f"assets/teamsIcons/{team['code']}.png", "PNG")
        else:
            img = Image.open(BytesIO(requests.get(team['image']).content))
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            img.save(f"assets/teamsIcons/{team['code']}.png", "PNG")
        if is_completed and team['result']['outcome'] == 'loss':
            A = img.getchannel('A')
            newA = A.point(lambda i: 128 if i > 100 else 0)
            img.putalpha(newA)
        _pasteImg(timetable, img_draw, img.resize(size), x, y, team['name'])
        if size == icon_size:
            x += icon_b + margin
        else:
            x += size[0] + margin / 2


def drawMultipleGames(
    x: int,
    y: int,
    timetable: ImageType,
    img_draw: ImageDrawType,
    datas: dict,
):
    tmp_x = x
    img_draw.line((x + 74, y + 5, x + 74, y + 60), fill=white, width=line_width)
    if len(datas) == 2:
        y += 10 + margin
    for i, game in enumerate(datas):
        if game['state'] == 'completed':
            is_completed = True
        else:
            is_completed = False
        drawGame(
            tmp_x,
            y,
            timetable,
            img_draw,
            is_completed,
            (game['match']['teams'][0], game['match']['teams'][1]),
            (30, 30)
        )
        if i % 2 == 0:
            tmp_x += 70 + margin
        else:
            y += 30 + margin / 2
            tmp_x = x


def drawHalfDayMatches(
    datas: dict[list[dict]],
    week_day: int,
    timetable: ImageType,
    img_draw: ImageDrawType,
    is_am: bool,
    tz: pytz.timezone
):
    last_league = None
    bo_size = 1
    how_many_leagues, how_many_bo_not_1 = howManyLeaguesAndBo(datas)
    if is_am:
        py = 0
    else:
        py = content_y - (
            len(datas) * (icon_b + margin) + bo_text_height *
            how_many_bo_not_1 + how_many_leagues * (icon_b + margin)
        )

    for data_index, data in enumerate(datas.values()):
        match = data[0]['match']
        x = left + margin + (content_x + margin) * week_day
        y = top + (icon_b + margin) * data_index + py
        if last_league != data[0]['league']:
            if bo_size > 1:
                drawFooterLeague(
                    x, y - icon_b / 2 - margin,
                    img_draw,
                    bo_size
                )
            last_league = data[0]['league']
            bo_size = match['strategy']['count']
            padding_top = 0 if data_index == 0 else title_bot_margin
            py += icon_b + margin + padding_top
            drawLeadingLeague(
                x, y,
                timetable,
                img_draw,
                padding_top,
                last_league['slug'],
                data[0]['startTime'],
                tz
            )
            y += icon_b + margin + padding_top
        if len(data) == 1:
            drawGame(
                x, y,
                timetable,
                img_draw,
                data[0]['state'] == 'completed',
                match['teams']
            )
        else:
            drawMultipleGames(
                x, y,
                timetable,
                img_draw,
                data
            )
    if bo_size > 1:
        y = top + (icon_b + margin) * (data_index) + py + icon_b / 2
        drawFooterLeague(
            x, y,
            img_draw,
            bo_size
        )


_tz = pytz.timezone('Europe/Paris')


def formatSchedules(data: list[dict]):
    today = datetime.date.today()
    startOfWeek = today - datetime.timedelta(days=today.weekday())
    weekSchedules = [startOfWeek]
    weekSchedules.extend([
        startOfWeek + datetime.timedelta(days=i)
        for i in range(1, 7)
    ])
    weekGames: dict[str, dict[str, dict[str, list[dict]]]] = {}
    for schedule in data:
        if schedule['type'] == 'show':
            continue
        Datetime = datetime.datetime.fromisoformat(
            schedule.get('startTime', '')).astimezone(_tz)
        date = Datetime.date()
        hour = Datetime.time()
        if hour.hour < 12:
            day_part = 'am'
        else:
            day_part = 'pm'
        if date in weekSchedules:
            weekGames.setdefault(
                date.isoformat(), {}).setdefault(
                    day_part, {}).setdefault(hour.isoformat(), []).append(schedule)
    return weekGames


def getFormattedPlanning(language: str, timezone: pytz.timezone, schedules: dict):
    schedules = formatSchedules(schedules)
    timetable = Image.open(f'assets/{language}_timetable.png')
    tz = pytz.timezone(timezone)
    img_draw: ImageDrawType = ImageDraw.Draw(timetable)
    for date, datas in schedules.items():
        week_day = datetime.date.fromisoformat(date).weekday()
        _logger.info(f"Drawing {date} ({week_day})")
        am, pm = datas.get('am', {}), datas.get('pm', {})
        drawHalfDayMatches(am, week_day, timetable, img_draw, True, tz)
        drawHalfDayMatches(pm, week_day, timetable, img_draw, False, tz)
    return timetable
