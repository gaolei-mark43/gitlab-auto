import requests


# 获取组ID
def get_group_id(group_name, baseurl, PRIVATE_TOKEN, logger=None):
    baseurl = baseurl + "/groups/" + group_name
    headers = {"Private-Token": PRIVATE_TOKEN }
    response = requests.get(baseurl, headers=headers)
    content = response.json()
    if response.status_code == 200 and len(content) > 0:
        group_ID = content["id"]
        return group_ID
    else:
        logger.error("获取组ID失败，报错如下:")
        logger.error("status_code: {}".format(response.status_code))
        logger.error("content: {}".format(response.content.decode('utf-8')))
        return None
