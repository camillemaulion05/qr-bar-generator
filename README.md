# QR and Barcode Generator API Integration

This project allows you to generate QR codes and various types of barcodes, upload them as images, and send them via a PUT API request to an external server.
The app uses environment variables to store API credentials and other configuration settings, allowing for a more flexible and secure deployment.

## Prerequisites

Before running the app, ensure you have the following tools and dependencies installed:

### Software:

- Python 3.6 or higher
- `pip` for installing Python packages

### Python Libraries:

1. `requests` – to send the API request.
2. `python-dotenv` – to load environment variables from a `.env` file.
3. `Pillow` – for handling image files (used for the QR Code).
4. `qrcode` – to generate QR codes.
5. `barcode` – to generate various types of barcodes.

### Installation Steps:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/camillemaulion05/qr-bar-generator
   cd qr-bar-generator
   ```

2. **Set up a Virtual Environment (Optional but Recommended):**

   Create a virtual environment to isolate the dependencies:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**

   Install all the required libraries using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

   Or install them individually:

   ```bash
   pip install requests python-dotenv Pillow qrcode barcode
   ```

4. **Set up Environment Variables:**

   Create a `.env` file in the root of the project directory and add the following configuration values:

   ```dotenv
    BASE_URL=https://your_integration_url/rest  # Replace with your actual base URL
    TABLE_NAME=your_table_name_here  # Replace with the target table name
    ATTACHMENT_FIELD_NAME=your_attachment_field_name_here  # Replace with the target attachment field name
    FILE_FIELD_NAME=your_file_field_name_here  # Replace with the target file field name
    RESPONSE_FIELD_NAME=your_response_field_name_here  # Replace with the target response field name
    RECORD_PK_ID=your_record_primary_key_id_here  # Replace with the target record primary key ID
    ACCESS_TOKEN=your_access_token_here  # Replace with your actual API Access Token
   ```

   Note:
   The ATTACHMENT_FIELD_NAME should correspond to a field in your Caspio table that is specifically set to the Attachment data type. This is necessary to ensure that files can be uploaded to the correct field.

   The FILE_FIELD_NAME should correspond to a field in your Caspio table that is specifically set to the File data type. This is necessary to ensure that files can be uploaded to the correct field.

   Make sure to replace the placeholder values (your_account_id, your_table_name_here, your_attachment_field_name_here, your_file_field_name_here, your_response_field_name_here, your_record_primary_key_id_here, and your_access_token_here) with your actual Integration URL, table name, attachment field, file field, response field, record ID, and Access Token.

5. **Run the Script:**

   After setting up the environment and installing dependencies, run the Python script:

   ```bash
   python app.py
   ```

   The script will:

   - Generate a QR code (or barcode, based on your input).
   - Send the generated file as part of a PUT request to the specified API endpoint.

## How It Works:

### 1. **QR Code Generation**:

The app generates a QR code using the `qrcode` library. You can customize the error correction, version, box size, and border size.

### 2. **Barcode Generation**:

The app supports multiple types of barcodes including:

- Code128
- EAN13
- UPCA
- Code39
- ITF
- Codabar

### 3. **File Upload**:

After generating the QR code or barcode, the image file is uploaded to the API using a PUT request with the file as form data. The `requests` library is used for making the API call, and the `python-dotenv` library loads environment variables securely.

### 4. **Environment Variables**:

The script uses the `.env` file to store configuration values like:

- Base URL (`BASE_URL`)
- Table Name (`TABLE_NAME`)
- Attachment Field Name (`ATTACHMENT_FIELD_NAME`)
- File Field Name (`FILE_FIELD_NAME`)
- Response Field Name (`RESPONSE_FIELD_NAME`)
- Record Primary Key (`RECORD_PK_ID`)
- API Access Token (`ACCESS_TOKEN`)

This approach makes it easy to securely store Token and other sensitive information.

## Example Usage:

Here is an example of how the QR code generation and file upload work:

1. **Generate a QR code** with custom error correction and version:

   ```python
   qr_stream = generate_code("https://example.com", code_type="qr", error_correction="H", version=10)
   ```

2. **Send the generated QR code** to the API:

   ```python
   send_file_to_api(qr_stream, BASE_URL, TABLE_NAME, ATTACHMENT_FIELD_NAME, RECORD_PK_ID, ACCESS_TOKEN)
   ```

3. **Generate a Code128 barcode**:

   ```python
   barcode_stream = generate_code("123456789012", code_type="barcode", barcode_type="code128")
   ```

4. **Send the generated barcode** to the API:

   ```python
   send_file_to_api(barcode_stream, BASE_URL, TABLE_NAME, ATTACHMENT_FIELD_NAME, RECORD_PK_ID, ACCESS_TOKEN)
   ```

### Note:

- The `send_file_to_api` function uses a PUT request to upload the file as form data.
- The `BASE_URL`, `TABLE_NAME`, `ATTACHMENT_FIELD_NAME`, `FILE_FIELD_NAME`, `RESPONSE_FIELD_NAME`, `RECORD_PK_ID`, and `ACCESS_TOKEN` values are read from environment variables.

## Troubleshooting:

- **Missing Environment Variables**: Ensure the `.env` file exists and contains the correct values.
- **API Response Issues**: If the API does not return a valid JSON response, check the status code and response text for more information.
- **Barcode Generation Errors**: Make sure the input data meets the requirements for each barcode type. For example, EAN13 requires 12 digits, and UPCA requires 11 digits.
