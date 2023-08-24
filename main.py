from agol_utils import *
from log_config import logger
from settings import *

from arcgis.gis import GIS
from arcgis.features import GeoAccessor, GeoSeriesAccessor
from dotenv import load_dotenv
from pathlib import Path
from typing import Union

import os

import pandas as pd

load_dotenv()


def get_new_disasters(
    gis: GIS, workspace: Path, item_id: str, querystring: str, result_name: str
) -> Union[Path, None]:
    """
    새로운 피처가 있는지 확인하고, 만약 확인해야 할 만한
    피처가 있다면 gdb에 저장한다.
    """
    new_item = get_item_by_id(gis, item_id)
    new_fs = get_item_content(new_item, querystring)
    result_path = feature_set_to_gdb(new_fs, workspace / result_name)
    if result_path:
        logger.debug(f"{result_name}이 성공적으로 GDB에 생성되었습니다.")
        return result_path
    logger.debug(f"{result_name}에 새로운 피처가 없어서 나머지 작업을 수행하지 않습니다.")
    return None


def get_history_disasters(history_workspace: Path, item_name: str) -> pd.DataFrame:
    df = pd.DataFrame.spatial.from_featureclass(str(history_workspace / item_name))
    logger.debug(f"{item_name}을(를) 데이터프레임으로 내보냈습니다.")
    print(df.columns)
    return df


def compare_disasters(
    new_df: pd.DataFrame,
    hist_df: pd.DataFrame,
    history_key: str,
    new_key: str,
    handler: function = None,
):
    if handler:
        new_df[new_key] = new_df[new_key].apply(handler)
    new_df["in_history"] = new_df[new_key].isin(hist_df[history_key])
    needs_update = new_df[new_df["in_history"] == True]
    is_new = new_df[new_df["in_history"] == False]

    

if __name__ == "__main__":
    gis = connect_to_agol(url=agol_url, username=agol_username, password=agol_password)

    new_eq_path, new_eq_df = get_new_disasters(
        gis,
        main_workspace,
        "9e2f2b544c954fda9cd13b7f3e6eebce",
        "(updated >= (current_timestamp-interval '30' minute)) AND (mag IS NOT NULL)",
        "EQ_LA_FC",
    )
    # new_wf_path, new_wf_df = get_new_disasters(
    #     gis, main_workspace, "82bedbcf0a5a478897ce9830e16bb35a", "1=1", "WF_LA_FC"
    # )
    # new_vc_path, new_vc_df = get_new_disasters(
    #     gis, main_workspace, "afe8efa5a3234fe18f6418b677184491", "1=1", "VC_LA_FC"
    # )

    eq_hist_df = get_history_disasters(history_workspace, "HIST_EQ")
    print(new_eq_df.columns)
