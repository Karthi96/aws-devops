import json
import base64
import boto3
import email

from PDFNetPython3.PDFNetPython import PDFNet, PDFDoc, SDFDoc

def lambda_handler(event, context):
    s3 = boto3.client("s3")
    PDFNet.Initialize()
    print("hi")
    post_data = base64.b64decode(event['body'])

    content_type = event["headers"]['content-type']

    ct = "Content-Type: "+content_type+"\n"
    print(ct)

    # parsing message from bytes
    msg = email.message_from_bytes(ct.encode()+post_data)
    
    # checking if the message is multipart
    print("Multipart check : ", msg.is_multipart())
    
    PDFNet.Initialize()
    
    doc = PDFDoc(post_data)
    doc.InitSecurityHandler()
    
    itr = doc.GetFieldIterator()
    while itr.HasNext():
        print("Field name: " + itr.Current().GetName())
        print("Field Value: " + itr.Current().GetValueAsString())
        print("Field partial name: " + itr.Current().GetPartialName())
        
        sys.stdout.write("Field type: ")
        type = itr.Current().GetType()
        if type == Field.e_button:
            print("Button")
        elif type == Field.e_text:
            print("Text")
        elif type == Field.e_choice:
            print("Choice")
        elif type == Field.e_signature:
            print("Signiture")
            
        print("------------------------------")
        itr.Next()
    
    doc.Close()
    print("Done.")
    
    # if message is multipart
    if msg.is_multipart():
        multipart_content = {}
        # retrieving form-data
        for part in msg.get_payload():
            # checking if filename exist as a part of content-disposition header
            if part.get_filename():
                # fetching the filename
                file_name = part.get_filename()
            print("Multipart_function",part.get_param('name', header='content-disposition') )

            multipart_content[part.get_param('name', header='content-disposition')] = part.get_payload(decode=True)

        
        #uploading file to S3
        s3_upload = s3.put_object(Bucket="breville-lambda-function-bucket-test", Key=file_name, Body=multipart_content["file"])

        # on upload success
        return {
            'statusCode': 200,
            'body': json.dumps('File uploaded successfully!')
        }
    else:
        # on upload failure
        return {
            'statusCode': 500,
            'body': json.dumps('Upload failed!')
        }

