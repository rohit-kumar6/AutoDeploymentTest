import sys
from reportlab.lib.colors import fade
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch, cm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping
from reportlab.pdfbase import pdfmetrics
import os.path as path
from os import chdir, environ as env, makedirs
import subprocess
import base64
import reportlab
import os


def createPdf(canvas, inputDic):
    for _ in range(1, int(inputDic['cartons']) + 1) :
        if inputDic['isFirstPage']:
            inputDic['isFirstPage'] = False
        else:
            canvas.showPage()

        inputDic['cartoonsLabelCreatedCount'] += 1
        canvas.roundRect(0.125*inch, 0.25*inch, 5.75*inch, 3.625*inch, 20, stroke=1, fill=0)
        canvas.roundRect(1.375*inch, 0.875*inch, 3.5*inch, 1.125*inch, 10, stroke=1, fill=0)
        canvas.setFont("Arial", 35)
        canvas.drawString(33, 223, inputDic['companyName'])

        canvas.setFont("Arial", 28)
        canvas.drawString(33, 188, "SKU")
        canvas.drawString(141, 188, ": " + inputDic['skuNumber'])
        canvas.drawString(106, 112, "Lot#")
        canvas.drawString(214, 112, ": " + inputDic['lotNumber'])
        canvas.drawString(106, 79, "Carton#")
        canvas.drawString(214, 79, ": ")
        canvas.drawString(124, 25, "Made In " + inputDic['madeInCountry'])
        strCartoonCount = str(inputDic['cartoonsLabelCreatedCount'])
        canvas.drawString(235, 79, strCartoonCount)

        canvas.setFont("Arial", 14)
        canvas.drawString(235 + strCartoonCount.__len__()*18, 79, "of " + str(inputDic['totalCartoonNumber']))

        canvas.setFont("Arial", 20)
        canvas.drawString(33, 162, "Color")
        canvas.drawString(141, 162, ": " + inputDic['color'])

def lambda_handler(event, context):
    print(event)
    inputDic = {}
    try :
        reportlab.rl_config.TTFSearchPath.append(os.getcwd())
        pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
        tmp_dir = "/tmp/cartoons"
        if not os.path.exists(tmp_dir):
            makedirs(tmp_dir)
        pdf_path = path.join(tmp_dir, 'Carton_Labels.pdf')
        subprocess.run(["chmod", "775", str(tmp_dir)])
        chdir(tmp_dir)
        canvas = Canvas(pdf_path, pagesize=(6*inch, 4*inch))

        inputDic["companyName"] = event['company'].strip()
        inputDic["madeInCountry"] = event["made_in"].strip()
        inputDic["lotNumber"] = event["lot_number"].strip()

        totalCartoonNumber = 0
        for count in range(0, event['cartons'].__len__()):
            noOfCartoons = int(event['cartons'][count]['no_of_cartons'].strip())
            totalCartoonNumber += noOfCartoons
        
        inputDic["totalCartoonNumber"] = totalCartoonNumber
        inputDic["isFirstPage"] = True
        inputDic["cartoonsLabelCreatedCount"] = 0
        for count in range(0, event['cartons'].__len__()):
            inputDic["skuNumber"] = event['cartons'][count]['sku'].strip()
            inputDic["color"] = event['cartons'][count]['color'].strip()
            inputDic["cartons"] = event['cartons'][count]['no_of_cartons']
            createPdf(canvas, inputDic)

        canvas.save()
        with open(pdf_path, "rb") as f:
            body = base64.b64encode(f.read()).decode("utf-8")
        
        response = {
            "statusCode": 200,
            "headers": {
                'Content-type' : 'application/pdf'
            },
            "body": body,
            "isBase64Encoded": True
        }

        print(response)
        return response
    except Exception as e:
        print(e)
        raise e