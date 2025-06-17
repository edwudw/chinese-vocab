# Chinese Word Processor

A Python script that reads .docx files, extracts Chinese words under the "生词" (new words) section, and provides their pinyin and English translations using translation services.

## Features

- Reads .docx files (Word 2007+ format)
- Extracts Chinese words under "生词" section
- Provides accurate pinyin using the pypinyin library
- Supports multiple translation services:
  - Google Translate API
  - Baidu Translate API
  - Free service (limited dictionary)
- Handles comma-separated word lists
- Clean, formatted output

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. The script uses:
   - `python-docx` for .docx files
   - `pypinyin` for accurate pinyin conversion

## Usage

### Basic Usage

Run the script and follow the prompts:

```bash
python chinese_improved.py
```

### Translation Service Options

1. **Google Translate API** (Recommended)
   - Requires Google Cloud API key
   - Most accurate translations
   - Free tier available (500,000 characters/month)

2. **Baidu Translate API**
   - Requires Baidu API credentials
   - Good for Chinese-specific translations
   - Free tier available

3. **Free Service**
   - No API key required
   - Limited dictionary of common words
   - Good for testing

### Getting API Keys

#### Google Translate API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Cloud Translation API
4. Create credentials (API key)
5. Copy the API key

#### Baidu Translate API
1. Go to [Baidu Translate Open Platform](http://api.fanyi.baidu.com/)
2. Register an account
3. Create an application
4. Get your App ID and Secret Key
5. Use format: `appid:secret_key`

## File Format

The script expects your .docx file to have a section marked with "生词" (new words). For example:

```
课文内容...

生词
学习, 中文, 汉字, 读写, 说话

练习...
```

**Note:** Only .docx files (Word 2007+ format) are supported. If you have a .doc file, please convert it to .docx format first.

## Output Format

The script will output each word with its pinyin and meaning:

```
1. 汉字: 学习
   拼音: xué xí
   意思: study

2. 汉字: 中文
   拼音: zhōng wén
   意思: Chinese
```

## Example Usage

```python
from chinese_improved import ChineseWordProcessor

# Initialize with Google Translate API
processor = ChineseWordProcessor("your_google_api_key", "google")

# Process a file
processor.process_file("path/to/your/document.docx")
```

## Troubleshooting

### Common Issues

1. **"No words found under '生词' section"**
   - Make sure your document contains the text "生词"
   - Check that Chinese characters are properly encoded

2. **"API error"**
   - Verify your API key is correct
   - Check your internet connection
   - Ensure you haven't exceeded API limits

3. **"Error reading file"**
   - Make sure the file path is correct
   - Ensure the file is a valid .doc or .docx format
   - Check file permissions

### File Encoding

If you encounter encoding issues:
- Save your .doc file as .docx format
- Ensure the file uses UTF-8 encoding
- Avoid special characters in the file path

## Dependencies

- `python-docx`: For reading .docx files
- `requests`: For API calls
- `pypinyin`: For accurate pinyin conversion
- `typing`: For type hints (Python 3.5+)

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues and enhancement requests! 