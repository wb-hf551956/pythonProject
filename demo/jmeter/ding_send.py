# 获取jenkins构建信息和本次报告地址
import os
import jenkins #安装pip install python-jenkins
import json
import urllib3


# jenkins登录地址
jenkins_url = "http://localhost:8080/"
# 获取jenkins对象
server = jenkins.Jenkins(jenkins_url, username='admin', password='016c69a0a6994e24aad8753629e8f3fd') #Jenkins登录名 ，密码x`
# job名称
job_name = "httpbin_api_test" #Jenkins运行任务名称
# job的url地址
job_url = jenkins_url + job_name
# 获取最后一次构建
job_last_build_url = server.get_info(job_name)['lastBuild']['url']
# 报告地址
report_url = job_last_build_url + 'allure-report' #'allure'为我的Jenkins全局工具配置中allure别名

'''
钉钉推送方法：
读取report文件中"prometheusData.txt"，循环遍历获取需要的值。
使用钉钉机器人的接口，拼接后推送text
'''

def DingTalkSend():
    d = {}
    # 获取项目绝对路径
    path = os.path.abspath(os.path.dirname((__file__)))
    # 打开prometheusData 获取需要发送的信息
    f = open(path + r'/allure-report/export/prometheusData.txt', 'r')
    for lines in f:
        for c in lines:
            launch_name = lines.strip('\n').split(' ')[0]
            num = lines.strip('\n').split(' ')[1]
            d.update({launch_name: num})
    print(d)
    f.close()
    retries_run = d.get('launch_retries_run')  # 运行总数
    print('运行总数:{}'.format(retries_run))
    status_passed = d.get('launch_status_passed')  # 通过数量
    print('通过数量：{}'.format(status_passed))
    status_failed = d.get('launch_status_failed')  # 不通过数量
    print('通过数量：{}'.format(status_failed))

    # 钉钉推送
    url = 'https://oapi.dingtalk.com/robot/send?access_token=16b9062955e54ede6c15322f884aeb80181b8ac592ff18197166e450de1fa965'  # webhook
    con = {"msgtype": "text",
           "text": {
               "content": "Pytest_Allure_Demo自动化脚本执行完成。"
                          "\n测试概述:"
                          "\n运行总数:" + retries_run +
                          "\n通过数量:" + status_passed +
                          "\n失败数量:" + status_failed +
                          "\n构建地址：\n" + job_url +
                          "\n报告地址：\n" + report_url
           }
           }
    urllib3.disable_warnings()
    http = urllib3.PoolManager()
    jd = json.dumps(con)
    jd = bytes(jd, 'utf-8')
    http.request('POST', url, body=jd, headers={'Content-Type': 'application/json'})


if __name__ == '__main__':
    DingTalkSend()