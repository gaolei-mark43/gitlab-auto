import requests
import json
from GiTee.groupAPI import getGroupID


def create_son_group(son_group_name, baseurl, PRIVATE_TOKEN, father_group_id, description=None, logger=None):
    baseurl = baseurl + "/groups"
    group_path = son_group_name
    visibility = "private"
    headers = {"Private-Token": PRIVATE_TOKEN, "Content-Type": "application/json"}
    data = {
        "name": son_group_name,
        "path": group_path,
        "visibility": visibility,
        "description": description,
        "parent_id": father_group_id
    }
    response = requests.post(baseurl, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        content = response.json()
        if content["message"] == "创建成功":
            logger.info("创建子组{}成功".format(son_group_name))
            # baseurl去掉/groups
            baseurl = baseurl.replace("/groups", "")
            group_ID = getGroupID.get_group_id(son_group_name, baseurl, PRIVATE_TOKEN, logger=logger)
            return group_ID
    else:
        logger.info("创建子组{}失败，报错如下:".format(son_group_name))
        logger.info("content: {}".format(response.content.decode('utf-8')))
        return None