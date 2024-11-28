from dataclasses import dataclass
from enum import Enum
from typing import Optional

import discord


class MealType(Enum):
    VEGAN = "Veganes Gericht"
    VEGETARIAN = "Vegetarisches Gericht"
    MEAT = "Fleischgericht"
    PASTA = "Pastateller"


@dataclass
class Price:
    value: float

    def __str__(self):
        return f"{f'{self.value:.2f}'.replace('.',',')} €"

    @staticmethod
    def get_from_string(price: str):
        return Price(float(price.split("\xa0")[0].replace(",", ".")))


@dataclass
class Meal:
    mealType: MealType
    mealName: str
    mealComponents: Optional[str]
    mealPrice: Price

    def create_embed(self) -> discord.Embed:
        embed = discord.Embed(title=self.mealName,
                              description=self.mealComponents,
                              color=0x00ff00)
        embed.set_footer(text=str(self.mealPrice))
        embed.set_author(name=self.mealType.value)
        return embed
