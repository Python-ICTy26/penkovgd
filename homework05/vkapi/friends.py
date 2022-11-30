import dataclasses
import math
import time
import typing as tp

from tqdm import tqdm
from vkapi import config, session
from vkapi.exceptions import APIError

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
    user_id: int,
    count: int = 5000,
    offset: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).

    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """
    params = {
        "access_token": config.VK_CONFIG["access_token"],
        "user_id": user_id,
        "fields": ",".join(fields) if fields is not None else "",
        "v": config.VK_CONFIG["version"],
        "count": count,
        "offset": offset,
    }
    method = "friends.get"
    response = session.get(method, params=params)
    if "error" in response or not response.ok:
        raise APIError(response["error"]["error_msg"])
    else:
        response = response.json()["response"]
    friends = FriendsResponse(count=response["count"], items=response["items"])
    return friends


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.

    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """

    progress = tqdm
    method = "friends.getMutual"
    if target_uid is not None:
        params = {
            "access_token": config.VK_CONFIG["access_token"],
            "source_uid": source_uid,
            "target_uid": target_uid,
            "order": order,
            "count": count,
            "offset": offset,
            "v": config.VK_CONFIG["version"],
        }
        response = session.get(method, params=params)
        if "error" in response or not response.ok:
            raise APIError(response["error"]["error_msg"])
        response = response.json()["response"]
        return response

    requests_qty = math.ceil(len(target_uids) / 100)
    list_of_mutual_friends = []
    for request_num in progress(range(requests_qty)):
        if request_num % 3 == 0 and request_num != 0:
            time.sleep(1)
        params = {
            "access_token": config.VK_CONFIG["access_token"],
            "target_uids": ",".join([str(i) for i in target_uids]),
            "order": order,
            "count": count if count is not None else "",
            "offset": offset + request_num * 100,
            "v": config.VK_CONFIG["version"],
        }
        response = session.get(method, params=params)
        if "error" in response or not response.ok:
            raise APIError(response["error"]["error_msg"])
        for friend in response.json()["response"]:
            mutual_friends = MutualFriends(
                id=friend["id"],
                common_friends=friend["common_friends"],
                common_count=friend["common_count"],
            )
            list_of_mutual_friends.append(mutual_friends)
    return list_of_mutual_friends
