import requests


# 获取成员ID
def get_member_id(member_name, baseurl, PRIVATE_TOKEN, logger=None):
    if member_name is None:
        logger.error("成员名称为空")
        return None
    baseurl = baseurl + "/users?username=" + member_name
    headers = {"Private-Token": PRIVATE_TOKEN}
    response = requests.get(baseurl, headers=headers)
    content = response.json()
    if response.status_code == 200 and len(content) > 0:
        member_ID = content[0]["id"]
        return member_ID
    else:
        logger.error("获取成员ID失败，报错如下:")
        logger.error("status_code: {}".format(response.status_code))
        logger.error("content: {}".format(response.content.decode('utf-8')))
        return None