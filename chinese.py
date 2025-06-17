import docx
import re
import requests
import json
from typing import List, Dict, Optional
import time

class ChineseWordProcessor:
    def __init__(self, api_key: str = None):
        """
        Initialize the processor with optional API key for translation service.
        You can use free services like Google Translate API or paid services like Baidu Translate.
        """
        self.api_key = api_key
        # Using Google Translate API (free tier available)
        self.translate_url = "https://translation.googleapis.com/language/translate/v2"
    
    def read_doc_file(self, file_path: str) -> str:
        """Read content from a .doc or .docx file."""
        try:
            doc = docx.Document(file_path)
            content = []
            for paragraph in doc.paragraphs:
                content.append(paragraph.text)
            return '\n'.join(content)
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
                
                # Extract Chinese characters separated by commas
                chinese_words = re.findall(r'[\u4e00-\u9fff]+', line)
                for word in chinese_words:
                    if len(word) >= 1:  # At least one character
                        words.append(word)
        
        return words
    
    def get_translation_and_pinyin(self, word: str) -> Dict[str, str]:
        """Get translation and pinyin for a Chinese word using translation service."""
        try:
            # For demonstration, using a free translation service
            # You can replace this with Google Translate API, Baidu Translate, etc.
            
            # Method 1: Using Google Translate (requires API key)
            if self.api_key:
                return self._google_translate(word)
            
            # Method 2: Using a free online service (for demonstration)
            return self._free_translate_service(word)
            
        except Exception as e:
            print(f"Error translating {word}: {e}")
            return {"pinyin": "N/A", "meaning": "Translation error"}
    
    def _google_translate(self, word: str) -> Dict[str, str]:
        """Use Google Translate API (requires API key)."""
        params = {
            'q': word,
            'source': 'zh',
            'target': 'en',
            'key': self.api_key
        }
        
        response = requests.get(self.translate_url, params=params)
        if response.status_code == 200:
            data = response.json()
            meaning = data['data']['translations'][0]['translatedText']
            
            # For pinyin, you might need a separate service or library
            # For now, we'll use a simple approach
            pinyin = self._get_pinyin_simple(word)
            
            return {"pinyin": pinyin, "meaning": meaning}
        else:
            return {"pinyin": "N/A", "meaning": "API error"}
    
    def _free_translate_service(self, word: str) -> Dict[str, str]:
        """Use a free translation service (for demonstration purposes)."""
        # This is a simplified version - in practice, you'd use a real API
        # For now, we'll simulate the response
        
        # Simple pinyin mapping for common characters (this is just for demo)
        pinyin_map = {
            '生': 'shēng', '词': 'cí', '学': 'xué', '习': 'xí', '中': 'zhōng', '文': 'wén',
            '汉': 'hàn', '字': 'zì', '读': 'dú', '写': 'xiě', '说': 'shuō', '话': 'huà'
        }
        
        pinyin = ""
        for char in word:
            pinyin += pinyin_map.get(char, char) + " "
        pinyin = pinyin.strip()
        
        # Simple meaning mapping (this is just for demo)
        meaning_map = {
            '生词': 'new word', '学习': 'study', '中文': 'Chinese', '汉字': 'Chinese character',
            '读写': 'read and write', '说话': 'speak'
        }
        
        meaning = meaning_map.get(word, f"Meaning for '{word}' (use real translation service)")
        
        return {"pinyin": pinyin, "meaning": meaning}
    
    def _get_pinyin_simple(self, word: str) -> str:
        """Simple pinyin conversion (you should use a proper library like pypinyin)."""
        # This is a very basic implementation
        # In practice, use: pip install pypinyin
        # Then: from pypinyin import pinyin, Style
        # pinyin(word, style=Style.TONE)
        
        pinyin_map = {
            '生': 'shēng', '词': 'cí', '学': 'xué', '习': 'xí', '中': 'zhōng', '文': 'wén',
            '汉': 'hàn', '字': 'zì', '读': 'dú', '写': 'xiě', '说': 'shuō', '话': 'huà',
            '你': 'nǐ', '我': 'wǒ', '他': 'tā', '她': 'tā', '它': 'tā', '们': 'men',
            '好': 'hǎo', '坏': 'huài', '大': 'dà', '小': 'xiǎo', '高': 'gāo', '低': 'dī'
        }
        
        result = ""
        for char in word:
            result += pinyin_map.get(char, char) + " "
        return result.strip()
    
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
        print("-" * 50)
        
        for i, word in enumerate(words, 1):
            print(f"{i}. 汉字: {word}")
            
            translation = self.get_translation_and_pinyin(word)
            print(f"   拼音: {translation['pinyin']}")
            print(f"   意思: {translation['meaning']}")
            print()
            
            # Add a small delay to avoid overwhelming the API
            time.sleep(0.5)

def main():
    """Main function to run the script."""
    print("Chinese Word Processor")
    print("=" * 50)
    
    # Initialize the processor
    # If you have an API key, pass it here: processor = ChineseWordProcessor("your_api_key")
    processor = ChineseWordProcessor()
    
    # Get the file path from user
    file_path = input("Enter the path to your .doc/.docx file: ").strip()
    
    if not file_path:
        print("No file path provided.")
        return
    
    # Process the file
    processor.process_file(file_path)

if __name__ == "__main__":
    main()
