import datetime as dt
import statistics
import typing as tp

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    data = get_friends(user_id, fields=["bdate"])
    ages = []
    for friend in data.items:
        try:
            day, month, year = [int(i) for i in friend["bdate"].split(".")]
            bdate = dt.date(year, month, day)
            age = dt.date.today().year - bdate.year
            ages.append(age)
        except:
            pass
    if ages:
        return statistics.median(ages)
    else:
        return None

# print(age_predict(364603977))
