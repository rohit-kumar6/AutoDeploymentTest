import pdfkit
import base64
import os
from os import chdir, environ as env, makedirs
import subprocess
import boto3

def getImageFromS3(imageName):
    s3 = boto3.resource('s3')
    s3.meta.client.download_file(os.getenv('S3BUCKET_NAME'), imageName, '/tmp/' + imageName)
    
    data = open('/tmp/' + imageName, 'rb').read() # read bytes from file
    data_base64 = base64.b64encode(data)  # encode to base64 (bytes)
    data_base64 = data_base64.decode()    # convert bytes to string
    return "data:image/jpeg;base64," + data_base64 + "\""

def lambda_handler(e, context):
    print(e)
    tmp_dir = "/tmp/invoice"
    if not os.path.exists(tmp_dir):
        makedirs(tmp_dir)
    pdf_path = os.path.join(tmp_dir, 'invoice.pdf')
    subprocess.run(["chmod", "775", str(tmp_dir)])
    try :
        f = open("invoice.html", 'r', encoding='utf-8')
        source_code = f.read() 
        f.close()
        f = open("css.txt", 'r', encoding='utf-8')
        cssData = f.read() 
        f.close()
        f = open("product.html", 'r', encoding='utf-8')
        productData = f.read() 
        f.close()

        productDataFinal = ""
        for data in e["items"] :
            partImage = data["part_thumbnail_image"]
            if (not data["part_thumbnail_url"] == None):
                partImage = getImageFromS3(data["part_thumbnail_url"])

            productDataFinal += productData.format(
                data["part_number"],
                data["part_name"],
                data["part_quantity"],
                data["part_unit_cost"],
                data["part_total_cost"],
                partImage,
                data["part_description"]
            )
        
        companyImage = e["company_logo_image"]
        if (not e["company_logo_url"] == None):
            companyImage = getImageFromS3(e["company_logo_url"])

        htmlUpdateData = source_code.format(
            companyImage,
            e["buyerDetails"]["buyer_name"],
            e["po_number"],
            e["buyerDetails"]["buyer_address_line"],
            e["order_date"],
            e["buyerDetails"]["buyer_contact"],
            e["ship_date"],
            e["buyerDetails"]["buyer_email"],
            e["buyerDetails"]["buyer_phone"],
            e["supplierDetails"]["supplier_name"],
            e["shipToDetails"]["shipToDetails_name"],
            e["supplierDetails"]["supplier_address_line"],
            e["shipToDetails"]["shipToDetails_address_line"],
            e["supplierDetails"]["supplier_contact"],
            e["shipToDetails"]["shipToDetails_contact"],
            e["supplierDetails"]["supplier_email"],
            e["shipToDetails"]["shipToDetails_phone"],
            e["supplierDetails"]["supplier_phone"],
            e["export_terms"],
            e["ship_method"],
            e["payment_terms"],
            productDataFinal,
            e["sub_total"],
            e["discount"],
            e["net_amount"],
            e["currency"],
            e["initial_payment"],
            e["balance_payment"],
            cssData
        )

        config = pdfkit.configuration(wkhtmltopdf=bytes('/opt/bin/wkhtmltopdf', 'utf-8'))
        pdfkit.from_string(htmlUpdateData, pdf_path, configuration=config)
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