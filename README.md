# QR and Barcode Generator API Integration

This project provides functionality for generating QR codes and various types of barcodes, saving them as image files, uploading them to an API using form data, and updating records in a table with the uploaded file's information.

## Features:

1. **QR Code Generation**: Generate QR codes with customizable error correction levels and versions.
2. **Barcode Generation**: Generate barcodes of various types such as Code128, EAN13, UPC, Code39, ITF, and Codabar.
3. **File Upload to API**: Upload generated files (QR codes or barcodes) to a specified API endpoint, attaching the file to a record.
4. **Record Update**: Update the record in a table with the URL of the uploaded file and a response message.

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

   - The `ATTACHMENT_FIELD_NAME` should correspond to a field in your Caspio table that is specifically set to the **Attachment** data type. This is necessary to ensure that files can be uploaded to the correct field.

   - The `FILE_FIELD_NAME` should correspond to a field in your Caspio table that is specifically set to the **File** data type. This is necessary to ensure that files can be uploaded to the correct field.

   Make sure to replace the placeholder values (such as `your_account_id`, `your_table_name_here`, etc.) with your actual Integration URL, table name, attachment field, file field, response field, record ID, and Access Token.

5. **Run the Script:**

   After setting up the environment and installing dependencies, run the Python script:

   ```bash
   python app.py
   ```

   The script will:

   - Generate a QR code (or barcode, based on your input).
   - Upload the generated image file via a **POST** request to the specified API endpoint.
   - Once the file is uploaded, the record will be updated via a **PUT** request with the URL of the uploaded file and a response message.

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

After generating the QR code or barcode, the image file is uploaded to the API using a **POST** request with the file as form data. The `requests` library is used for making the API call, and the `python-dotenv` library loads environment variables securely.

### 4. **Record Update**:

Once the file is uploaded successfully, a **PUT** request is made to update the record in the table with the URL of the uploaded file and a response message. This allows the record to be updated with the new file's data.

### 4. **Environment Variables**:

The script uses the `.env` file to store configuration values like:

- Base URL (`BASE_URL`)
- Table Name (`TABLE_NAME`)
- Attachment Field Name (`ATTACHMENT_FIELD_NAME`)
- File Field Name (`FILE_FIELD_NAME`)
- Response Field Name (`RESPONSE_FIELD_NAME`)
- Record Primary Key (`RECORD_PK_ID`)
- API Access Token (`ACCESS_TOKEN`)

This approach makes it easy to securely store sensitive information, such as the API Access Token.

## Example Usage:

Here is an example of how the QR code and Barcode generation, file upload, and record update work:

1. **Generate a QR code** with custom error correction and version:

   ```python
   qr_stream = generate_code("https://example.com", code_type="qr", error_correction="H", version=10)
   ```

2. **Upload the generated QR code** to the API via a **POST** request:

   ```python
   qr_file_url = upload_file_to_api(qr_stream, BASE_URL, ACCESS_TOKEN)
   ```

3. **Update the record** with the uploaded QR code file URL via a **PUT** request:

   ```python
   update_record(BASE_URL, TABLE_NAME, FILE_FIELD_NAME, RESPONSE_FIELD_NAME, RECORD_PK_ID, ACCESS_TOKEN, qr_file_url)
   ```

4. **Generate a Code128 barcode**:

   ```python
   barcode_stream = generate_code("123456789012", code_type="barcode", barcode_type="code128")
   ```

5. **Upload the generated barcode** to the API via a **POST** request:

   ```python
   barcode_file_url = upload_file_to_api(barcode_stream, BASE_URL, ACCESS_TOKEN)
   ```

6. **Update the record** with the uploaded barcode file URL via a **PUT** request:

   ```python
   update_record(BASE_URL, TABLE_NAME, FILE_FIELD_NAME, RESPONSE_FIELD_NAME, RECORD_PK_ID, ACCESS_TOKEN, barcode_file_url)
   ```

### Note:

- The `generate_code` function generates either a QR code or a barcode and returns it as a byte stream.

  - Arguments:

    - **data** (`str`): The data to encode in the QR code or barcode.

    - **code_type** (`str`): The type of code to generate. Can be one of the following:
    - `'qr'`: To generate a QR code.
    - `'barcode'`: To generate a barcode.

    - **barcode_type** (`str`): The type of barcode to generate. This argument is relevant when `code_type` is set to `'barcode'`. Valid options are:
    - `'code128'`
    - `'ean13'`
    - `'upc'`
    - `'code39'`
    - `'itf'`
    - `'codabar'`

    - **error_correction** (`str`): The error correction level for the QR code. This argument is relevant when `code_type` is set to `'qr'`. Valid options are:
    - `'L'`: 7% of error correction.
    - `'M'`: 15% of error correction.
    - `'Q'`: 25% of error correction.
    - `'H'`: 30% of error correction.

    - **version** (`int`): The version of the QR code. This argument is only relevant when `code_type` is set to `'qr'`. Valid values range from 1 to 40, where higher values represent more complex QR codes.

    - **box_size** (`int`): The size of each box in the QR code. This controls how large each square element in the QR code appears. Default is 10.

    - **border** (`int`): The border size (in boxes) for the QR code. Default is 4.

  - Returns:
    - **bytes**: The generated image as a byte stream, which can be saved to a file or uploaded directly to an API.

- The `upload_file_to_api` function uses a **POST** request to upload the file (QR code or barcode) as form data and returns the file URL.
- The `update_record` function uses a **PUT** request to update the record with the uploaded file URL and response message.
- The `BASE_URL`, `TABLE_NAME`, `ATTACHMENT_FIELD_NAME`, `FILE_FIELD_NAME`, `RESPONSE_FIELD_NAME`, `RECORD_PK_ID`, and `ACCESS_TOKEN` values are read from environment variables.

## Troubleshooting:

- **Missing Environment Variables**: Ensure the `.env` file exists and contains the correct values.
- **API Response Issues**: If the API does not return a valid JSON response, check the status code and response text for more information.
- **Barcode Generation Errors**: Make sure the input data meets the requirements for each barcode type. For example, EAN13 requires 12 digits, and UPCA requires 11 digits.
