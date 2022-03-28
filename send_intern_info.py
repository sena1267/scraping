import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from selenium.webdriver.common.by import By
from selenium import webdriver
import os 
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), 'email.env')
load_dotenv(dotenv_path)
# 送信元,送信先
MAIL_FROM = os.environ.get('MAIL_FROM')
MAIL_TO = os.environ.get('MAIL_TO')
# ログインするためのメアド,パスワード
LOGIN_MAIL = os.environ.get('LOGIN_MAIL')
LOGIN_PASS = os.environ.get('LOGIN_PASS')

#インターン情報の取得
browser = webdriver.Chrome()
url = 'https://01intern.com/job/list.html?jobTypes=2&stickingConditions=23'
browser.get(url)
job_elems = browser.find_elements(by=By.CLASS_NAME, value='i-job-item')
jobs = []
for job in job_elems:
    # 募集しているかの確認
    suspend_check = job.text.split('\n')[0]
    if suspend_check != '募集停止中':
        job_title_element = job.find_element(by=By.CLASS_NAME, value='i-job-title')
        job_url = job.find_element(by=By.TAG_NAME, value='a').get_attribute('href')
        jobs.append([job_title_element.text, job_url])
browser.quit()

#本文の作成
text = ''
for job in jobs:
    text += job[0] + ' : ' + job[1] + '\n'
    text += '===============================\n'

#SMTPのオブジェクト作成（GmailのSMTPポート：587）
smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
#メールサーバに対する応答
smtpobj.ehlo()
#暗号化通信開始
smtpobj.starttls()
smtpobj.ehlo()
#ログイン
smtpobj.login(LOGIN_MAIL, LOGIN_PASS)

#メッセージのオブジェクト
msg = MIMEText(text)
msg['Subject'] = '【自動送信】インターン情報'
msg['From'] = MAIL_FROM
msg['To'] = MAIL_TO
msg['Date'] = formatdate(localtime=True)

#メール送信
smtpobj.sendmail(MAIL_FROM, MAIL_TO, msg.as_string())