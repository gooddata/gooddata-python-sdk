---
title: "Dashboard Export"
linkTitle: "Dashboard Export"
weight: 23
no_list: true
---

Create dashboard exports or automate your pipelines. Can be for [example](#example) be used to report .pdf via e-mail each week.

## Methods

* [export_pdf](./export_pdf/)
* [export_tabular](./export_tabular/)
* [export_tabular_by_visualization_id](./export_tabular_by_visualization_id/)


## Example

```python
from gooddata_sdk import GoodDataSdk
import schedule
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate


# GoodData base URL, e.g. "https://www.example.com"
host = "https://www.example.com"
token = "<your_personal_access_token>"
sdk = GoodDataSdk.create(host, token)


def send_mail(send_from, send_to, subject, text, files, server):
   msg = MIMEMultipart()
   msg["From"] = send_from
   msg["To"] = send_to
   msg["Date"] = formatdate(localtime=True)
   msg["Subject"] = subject

   msg.attach(MIMEText(text))

   # Open CSV / XLSX file(s) and add it to email attachment
   for f in files or []:
       with open(f, "rb") as fil:
           part = MIMEApplication(
               fil.read(),
               Name=basename(f)
           )
       part["Content-Disposition"] = "attachment; filename=\"%s\"" % basename(f)
       msg.attach(part)

   smtp = smtplib.SMTP(server)
   smtp.sendmail(send_from, send_to, msg.as_string())
   smtp.close()


def export_tabular():
    # Export a particular visualization in the desired format (CSV / XLSX)
    sdk.export.export_tabular_by_visualization_id(
        workspace_id = "demo",
        visualization_id = "revenue",
        file_format = "CSV",
        file_name = "revenue_export.csv"
    )

    send_mail(
        send_from = "your@email.com",
        send_to = "to@email.com",
        subject = "Scheduled export",
        text = "Scheduled export of dashboard 'dashboard_overview'",
        # Name of exported file from the method call 'export_pdf'
        files = "revenue_export.csv",
        server = "<your_smtp_server>"
    )


# Schedule call to export visualization in CSV and sent via e-email every morning at 8:00.
schedule.every().day.at("8:00").do(export_tabular)
```
