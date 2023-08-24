from arcgis.gis import GIS, Item
from arcgis.features import FeatureSet
from log_config import logger
from typing import Union, Tuple
from pathlib import Path

import pandas as pd


class AgolConnectionError(Exception):
    pass


class FailedToGetItem(Exception):
    pass


class ItemDoesNotExistError(Exception):
    pass


class FailedToGetFeatureSet(Exception):
    pass


def connect_to_agol(url: str, username: str, password: str) -> GIS:
    """
    agol에 연결해서 연결 객체 반환
    """
    try:
        gis = GIS(url=url, username=username, password=password)
        return gis
    except Exception as e:
        print(" ".join([url, username, password]))
        logger.error(f"{e}\t AGOL 연결에 실패했습니다.")
        raise AgolConnectionError("연결에 문제가 있나봐용")


def get_item_by_id(gis: GIS, item_id: str) -> Item:
    try:
        item = gis.content.get(item_id)
        logger.debug(f"{item.title}을(를) 확인했습니다.")
        if not item:
            logger.error("아이템이 없습니다.")
            raise ItemDoesNotExistError("아이템 아이디를 확인해주세용.")
        return item
    except Exception as e:
        logger.error(f"{e}\t아이템을 찾을 수 없습니다.")
        raise FailedToGetItem("아이템을 갖고올 수 없습니당.")


def get_item_content(item: Item, querystring: str) -> Union[FeatureSet, None]:
    try:
        layer = item.layers[0]
        fs = layer.query(querystring)
        if len(fs) == 0:
            return None
        return fs
    except Exception as e:
        logger.error(f"{e}\t피처에 있는 데이터를 가져올 수 없습니다.")
        raise FailedToGetFeatureSet("피처에 있는 데이터를 가져올 수 없습니당.")


def feature_set_to_gdb(
    fs: FeatureSet, gdb_path: Path
) -> Tuple[Union[Path, None], Union[pd.DataFrame, None]]:
    if not fs:
        logger.debug("새로운 피쳐가 없습니다. None을 반환합니다.")
        return (None, None)
    fs_df = fs.sdf
    result_path = fs_df.spatial.to_featureclass(str(gdb_path))
    return (Path(result_path), fs_df)
