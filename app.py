import os
import io
import qrcode
import requests
from barcode import Code128, EAN13, UPCA, Code39, ITF, codabar 
from barcode.writer import ImageWriter
from PIL import Image
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Retrieve values from environment variables
BASE_URL = os.getenv('BASE_URL')
TABLE_NAME = os.getenv('TABLE_NAME')
ATTACHMENT_FIELD_NAME = os.getenv('ATTACHMENT_FIELD_NAME')
RECORD_PK_ID = os.getenv('RECORD_PK_ID')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

# Function to generate either a barcode or a QR code and return it as a byte stream
def generate_code(data, code_type="qr", barcode_type="code128", error_correction="L", version=1, box_size=10, border=4):
    """
    Generates a QR code or Barcode and returns the image as a byte stream.

    Args:
        data (str): Data to encode in the QR Code/Barcode.
        code_type (str): Type of code to generate ('qr' or 'barcode').
        barcode_type (str): Type of barcode to generate ('code128', 'ean13', 'upc', 'code39', 'itf', 'codabar').
        error_correction (str): Error correction level for QR code ('L', 'M', 'Q', 'H').
        version (int): Version of the QR code (1 to 40).
        box_size (int): Size of each box in the QR code.
        border (int): Border size of the QR code.

    Returns:
        bytes: The image as a byte stream.
    """
    # Generate QR Code
    if code_type.lower() == "qr":
        qr = qrcode.QRCode(
            version=version, 
            error_correction=getattr(qrcode.constants, f"ERROR_CORRECT_{error_correction.upper()}"),
            box_size=box_size, 
            border=border
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to a byte stream and return it
        byte_io = io.BytesIO()
        img.save(byte_io, format="PNG")
        byte_io.seek(0)
        return byte_io

    # Generate Barcode
    elif code_type.lower() == "barcode":
        # Choose barcode type
        if barcode_type.lower() == "code128":
            barcode = Code128(data, writer=ImageWriter())
        elif barcode_type.lower() == "ean13":
            if len(data) != 12:
                raise ValueError("EAN13 barcode requires exactly 12 digits.")
            barcode = EAN13(data, writer=ImageWriter())
        elif barcode_type.lower() == "upc":
            if len(data) != 11:
                raise ValueError("UPC barcode requires exactly 11 digits.")
            barcode = UPCA(data, writer=ImageWriter())
        elif barcode_type.lower() == "code39":
            barcode = Code39(data, writer=ImageWriter())
        elif barcode_type.lower() == "itf":
            if len(data) % 2 != 0:
                raise ValueError("ITF barcode requires an even number of digits.")
            barcode = ITF(data, writer=ImageWriter())
        elif barcode_type.lower() == "codabar":
            barcode = codabar(data, writer=ImageWriter()) 
        else:
            raise ValueError(f"Invalid barcode type '{barcode_type}'. Supported types are: 'code128', 'ean13', 'upc', 'code39', 'itf', 'codabar'.")
        
        # Save to a byte stream and return it
        byte_io = io.BytesIO()
        barcode.write(byte_io)
        byte_io.seek(0)
        return byte_io

    else:
        raise ValueError(f"Invalid code type '{code_type}'. Supported types are: 'qr' and 'barcode'.")

# Function to send the generated file via API request using PUT method (with form data)
def send_file_to_api(file_stream, base_url, table_name, attachment_field_name, record_pk_id, access_token):
    """
    Sends the generated file (as a byte stream) to the API using a PUT request with form data.

    Args:
        file_stream (BytesIO): The file as a byte stream to upload.
        base_url (str): The base URL for the API endpoint.
        table_name (str): The name of the table to update.
        attachment_field_name (str): The name of the field to attach the file.
        record_pk_id (str): The primary key ID of the record to update.
        api_key (str): The API key for authentication.
    """
    url = f"{base_url}/v2/tables/{table_name}/attachments/{attachment_field_name}/{record_pk_id}"

    # Prepare the file as part of form data
    files = {
        'file': ('image.png', file_stream, 'image/png')  # 'file' is the form field name expected by the API
    }

    # Set the authorization header with the API key
    headers = {
        "Authorization": f"Bearer {access_token}"  # Authorization header
    }

    # Using PUT method for uploading the file as form data
    response = requests.put(url, files=files, headers=headers)

    # Debugging: print the status code and response content
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")

    # Handle the response
    if response.status_code == 200:
        print(f"File uploaded successfully")
    else:
        print(f"Failed to upload file. Status code: {response.status_code}")


# Example Usage:

# Generate a QR code with custom error correction and version
qr_stream = generate_code("https://example.com", code_type="qr", error_correction="H", version=10)
print("QR Code generated in memory.")

# Generate a Code128 barcode
# barcode_stream = generate_code("123456789012", code_type="barcode", barcode_type="code128")
# print("Barcode generated in memory.")

# Send the QR code to the API using PUT method
send_file_to_api(qr_stream, BASE_URL, TABLE_NAME, ATTACHMENT_FIELD_NAME, RECORD_PK_ID, ACCESS_TOKEN)

# Send the Barcode to the API using PUT method
# send_file_to_api(barcode_stream, BASE_URL, TABLE_NAME, ATTACHMENT_FIELD_NAME, RECORD_PK_ID, ACCESS_TOKEN)
