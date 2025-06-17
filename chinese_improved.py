import docx
import re
import requests
import json
from typing import List, Dict, Optional
import time
from pypinyin import pinyin, Style
import os

class ChineseWordProcessor:
    def __init__(self, api_key: str = None, translation_service: str = "google"):
        """
        Initialize the processor with optional API key for translation service.
        
        Args:
            api_key: API key for translation service
            translation_service: "google", "baidu", or "free"
        """
        self.api_key = ""
        self.translation_service = "google"
        
        # API endpoints
        self.google_translate_url = "https://translation.googleapis.com/language/translate/v2"
        self.baidu_translate_url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
    
    def read_doc_file(self, file_path: str) -> str:
        """Read content from a .doc or .docx file."""
        try:
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension == '.docx':
                # Use python-docx for .docx files
                doc = docx.Document(file_path)
                content = []
                for paragraph in doc.paragraphs:
                    content.append(paragraph.text)
                return '\n'.join(content)
            
            elif file_extension == '.doc':
                print("Error: .doc files are not supported due to their complex binary format.")
                print("Please convert your .doc file to .docx format:")
                print("1. Open the file in Microsoft Word")
                print("2. Go to File > Save As")
                print("3. Choose 'Word Document (.docx)' as the format")
                print("4. Save the file with a .docx extension")
                print("5. Run this script again with the .docx file")
                return ""
            
            else:
                print(f"Unsupported file format: {file_extension}. Please use .docx files.")
                return ""
                
        except Exception as e:
            print(f"Error reading file: {e}")
            return ""
    
    def extract_words_under_shengci(self, content: str) -> List[str]:
        """Extract Chinese words that appear under '生词' section."""
        words = []
        
        # Find the section starting with "生词"
        lines = content.split('\n')
        in_shengci_section = False
        
        for line in lines:
            line = line.strip()
            
            # Check if we're entering the 生词 section
            if '生词' in line:
                in_shengci_section = True
                continue
            
            # If we're in the 生词 section, extract words
            if in_shengci_section and line:
                # Skip if we hit another major section (like a new heading)
                if re.match(r'^[一二三四五六七八九十\d]+[、.]', line):
                    break
                if re.match(r'语法', line):
                    break
                
                # Extract Chinese characters separated by commas, spaces, or other delimiters
                chinese_words = re.findall(r'[\u4e00-\u9fff]+', line)
                for word in chinese_words:
                    if len(word) >= 1:  # At least one character
                        words.append(word)
        
        return words
    
    def get_pinyin(self, word: str) -> str:
        """Get pinyin for a Chinese word using pypinyin library."""
        try:
            # Get pinyin with tone marks
            pinyin_list = pinyin(word, style=Style.TONE)
            return ' '.join([p[0] for p in pinyin_list])
        except Exception as e:
            print(f"Error getting pinyin for {word}: {e}")
            return "N/A"
    
    def get_translation(self, word: str) -> str:
        """Get translation for a Chinese word using the specified translation service."""
        try:
            if self.translation_service == "google" and self.api_key:
                return self._google_translate(word)
            elif self.translation_service == "baidu" and self.api_key:
                return self._baidu_translate(word)
            else:
                return self._free_translate_service(word)
        except Exception as e:
            print(f"Error translating {word}: {e}")
            return "Translation error"
    
    def _google_translate(self, word: str) -> str:
        """Use Google Translate API."""
        params = {
            'q': word,
            'source': 'zh',
            'target': 'en',
            'key': self.api_key
        }
        
        response = requests.get(self.google_translate_url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data['data']['translations'][0]['translatedText']
        else:
            return "API error"
    
    def _baidu_translate(self, word: str) -> str:
        """Use Baidu Translate API."""
        import hashlib
        import random
        
        appid = self.api_key.split(':')[0] if ':' in self.api_key else self.api_key
        secret_key = self.api_key.split(':')[1] if ':' in self.api_key else ""
        
        salt = random.randint(32768, 65536)
        sign = appid + word + str(salt) + secret_key
        sign = hashlib.md5(sign.encode()).hexdigest()
        
        params = {
            'q': word,
            'from': 'zh',
            'to': 'en',
            'appid': appid,
            'salt': salt,
            'sign': sign
        }
        
        response = requests.get(self.baidu_translate_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'trans_result' in data:
                return data['trans_result'][0]['dst']
        
        return "API error"
    
    def _free_translate_service(self, word: str) -> str:
        """Use a free translation service (for demonstration purposes)."""
        # This is a simplified version - in practice, you'd use a real API
        # You can replace this with actual free translation services
        
        # Simple meaning mapping for common words
        meaning_map = {
            '生词': 'new word', '学习': 'study', '中文': 'Chinese', '汉字': 'Chinese character',
            '读写': 'read and write', '说话': 'speak', '你好': 'hello', '谢谢': 'thank you',
            '再见': 'goodbye', '对不起': 'sorry', '没关系': "it's okay", '请': 'please',
            '老师': 'teacher', '学生': 'student', '朋友': 'friend', '家人': 'family',
            '工作': 'work', '生活': 'life', '时间': 'time', '地方': 'place'
        }
        
        return meaning_map.get(word, f"Meaning for '{word}' (use real translation service)")
    
    def process_file(self, file_path: str) -> None:
        """Main method to process the .doc file and print results."""
        print(f"Reading file: {file_path}")
        content = self.read_doc_file(file_path)
        
        if not content:
            print("No content found in file.")
            return
        
        print("Extracting words under '生词'...")
        words = self.extract_words_under_shengci(content)
        
        if not words:
            print("No words found under '生词' section.")
            return
        
        print(f"Found {len(words)} words. Processing translations...")
        print("-" * 60)
        
        for i, word in enumerate(words, 1):
            print(f"{i}. 汉字: {word}")
            
            # Get pinyin
            pinyin_result = self.get_pinyin(word)
            print(f"   拼音: {pinyin_result}")
            
            # Get translation
            meaning = self.get_translation(word)
            print(f"   意思: {meaning}")
            print()
            
            # Add a small delay to avoid overwhelming the API
            time.sleep(0.5)

def main():
    """Main function to run the script."""
    print("Chinese Word Processor")
    print("=" * 60)
    
    # Configuration
    print("Translation Service Options:")
    print("1. Google Translate (requires API key)")
    print("2. Baidu Translate (requires API key)")
    print("3. Free service (limited dictionary)")
    
    choice = input("Choose translation service (1-3): ").strip()
    
    api_key = None
    translation_service = "free"
    
    if choice == "1":
        api_key = input("Enter Google Translate API key: ").strip()
        translation_service = "google"
    elif choice == "2":
        api_key = input("Enter Baidu Translate API key (format: appid:secret_key): ").strip()
        translation_service = "baidu"
    
    # Initialize the processor
    processor = ChineseWordProcessor(api_key, translation_service)
    
    # Get the file path from user
    file_path = input("Enter the path to your .doc/.docx file: ").strip()
    
    if not file_path:
        print("No file path provided.")
        return
    
    # Process the file
    processor.process_file(file_path)

if __name__ == "__main__":
    main() 