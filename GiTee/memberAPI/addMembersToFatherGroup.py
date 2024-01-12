import requests
import json


# 用户增加到组
def add_member_to_group(member_id, group_id, baseurl, PRIVATE_TOKEN, logger=None):
    if member_id is None:
        logger.error("成员ID为空,无法增加到组,请检查成员是否存在")
        return None
    if group_id is None:
        logger.error("组ID为空,无法增加到组,请检查组是否存在")
        return None
    baseurl = baseurl + "/groups/" + str(group_id) + "/members"
    headers = {"Private-Token": PRIVATE_TOKEN}
    access_level = 6
    data = {"user_id": member_id, "access_level": access_level}
    response = requests.post(baseurl, headers=headers, data=json.dumps(data))
    content = response.content.decode('utf-8')
    if response.status_code == 200:
        logger.info("用户{}增加到组{}成功".format(member_id, group_id))
        return True
    else:
        logger.error("用户{}增加到组{}失败,报错如下:".format(member_id, group_id))
        logger.error("status_code: {}".format(response.status_code))
        logger.error("content: {}".format(content))
        return False