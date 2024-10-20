from datetime import datetime, timedelta
from email.policy import default

import discord

from models.mensa.mensaModels import Meal, MealType, Price

import requests
from bs4 import BeautifulSoup

from utils.cacheUtils import timed_cache
from utils.constants import Constants

@timed_cache(30)
def get_mensa_plan(date: datetime) -> list[Meal]:
    """
    Fetches the mensa plan for a given date.

    Args:
        date (datetime): The date for which to fetch the mensa plan.

    Returns:
        list[Meal]: A list of Meal objects representing the meals available on the given date.
    """
    page = requests.get(f"{Constants.URLS.MENSAPLAN}{date.strftime('%Y-%m-%d')}")
    soup = BeautifulSoup(page.content, 'html.parser')

    meals = []

    for meal in soup.select(".type--meal"):
        meal_type = MealType(meal.select_one(".meal-tags span").text)
        meal_name = meal.select_one("h4").text
        meal_components = meal.select_one(".meal-components").text if meal.select_one(".meal-components") else None
        meal_price = Price.get_from_string(meal.select_one(".meal-prices span").text.strip())

        meals.append(Meal(meal_type, meal_name, meal_components, meal_price))

    return meals


def get_next_mensa_day(current_date: datetime) -> datetime:
    """
    Calculates the next open mensa day based on the current date.

    Args:
        current_date (datetime): The current date.

    Returns:
        datetime: The next open mensa day.
    """
    # Mensa is closed on weekends
    if current_date.weekday() == 4:
        return current_date + timedelta(days=3)
    elif current_date.weekday() == 5:
        return current_date + timedelta(days=2)
    else:
        return current_date + timedelta(days=1)


def get_last_mensa_day(current_date: datetime) -> datetime:
    """
    Calculates the last open mensa day based on the current date.

    Args:
        current_date (datetime): The current date.

    Returns:
        datetime: The last open mensa day.
    """
    # Mensa is closed on weekends
    if current_date.weekday() == 0:
        return current_date - timedelta(days=3)
    elif current_date.weekday() == 6:
        return current_date - timedelta(days=2)
    else:
        return current_date - timedelta(days=1)


def check_if_mensa_is_open(current_date: datetime) -> bool:
    """
    Checks if the mensa is open on the given date.

    Args:
        current_date (datetime): The date to check.

    Returns:
        bool: True if the mensa is open, False otherwise.
    """
    if current_date.weekday() >= 5:
        return False
    
    if current_date.date() < datetime.now().date():
        return False

    if current_date.date() > (datetime.now() + timedelta(days=7)).date():
        return False

    return True

def get_mensa_open_days() -> list[str]:
    """
    Returns a list of all open mensa days for the next week.

    Returns:
        list[str]: A list of all open mensa days for the next week.
    """
    current_date = datetime.now()
    open_days = []

    for i in range(7):
        if check_if_mensa_is_open(current_date):
            open_days.append(current_date.strftime('%d.%m.%Y'))
        current_date += timedelta(days=1)

    return open_days

async def mensa_day_autocomplete(ctx: discord.AutocompleteContext) -> list[str]:
    """
    Autocompletes the mensa days for the mensa command.

    Args:
        ctx (discord.AutocompleteContext): The context of the autocomplete.

    Returns:
        list[str]: A list of all open mensa days for the next week.
    """
    return [day for day in get_mensa_open_days() if day.startswith(ctx.value)]
