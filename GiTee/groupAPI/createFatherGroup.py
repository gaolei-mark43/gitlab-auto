import requests
import json
from GiTee.groupAPI import getGroupID


# 创建父组
def create_father_group(group_name, baseurl, PRIVATE_TOKEN, description=None, logger=None):
    baseurl = baseurl + "/groups"
    group_path = group_name
    visibility = "private"
    headers = {"Private-Token": PRIVATE_TOKEN, "Content-Type": "application/json"}
    data = {
        "name": group_name,
        "path": group_path,
        "visibility": visibility,
        "description": description
    }
    response = requests.post(baseurl, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        content = response.json()
        if content["message"] == "创建成功":
            logger.info("创建父组{}成功".format(group_name))
            # baseurl去掉/groups
            baseurl = baseurl.replace("/groups", "")
            group_ID = getGroupID.get_group_id(group_name, baseurl, PRIVATE_TOKEN, logger=logger)
            return group_ID
    else:
        logger.info("创建父组{}失败，报错如下:".format(group_name))
        logger.info("content: {}".format(response.content.decode('utf-8')))
        return None

