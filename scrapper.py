import warnings
from dataclasses import dataclass, field
from typing import List, Optional

import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub


@dataclass
class TextSection:
    title: Optional[str] = None
    subtitle: Optional[str] = None
    paragraphs: List[str] = field(default_factory=list)
    side_notes: List[str] = field(default_factory=list)
    order_number: int = 0


@dataclass
class Scrapper:
    def __init__(self, file_path):
        self.file_path = file_path
        self.book = None
        self.author = None
        self.title = None
        self.subtitle = None
        self.side_notes = []
        self.sections: List[TextSection] = []
        self.special_classes = ['Tekst_TUSSENKOP', 'Kop-groot', '_idGenObjectStyleOverride-1']

        self._load_book()
        self._extract_metadata()
        self._extract_text()

    def _load_book(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning)
            warnings.filterwarnings("ignore", category=FutureWarning)
            self.book = epub.read_epub(self.file_path)

    def _extract_metadata(self):
        def get_meta(name):
            value = self.book.get_metadata('DC', name)
            return value[0][0] if value else None

        self.title = get_meta('title')
        self.subtitle = get_meta('description')
        self.author = get_meta('creator')

    def print_metadata(self):
        print(f"Title: {self.title}")
        print(f"Subtitle: {self.subtitle}")
        print(f"Author: {self.author}")


    def get_text(self):
        item_document = [item for item in self.book.get_items() if item.get_type() == ebooklib.ITEM_DOCUMENT][0]
        text = item_document.get_content().decode('utf-8')
        bs_text = BeautifulSoup(text, 'html.parser')
        bs_text = self.decompose(bs_text)
        text = bs_text.get_text()
        text = "\n".join([line for line in text.split("\n") if line.strip()])
        return text

    def _extract_text(self):
        section_number = 0

        item_document = [item for item in self.book.get_items() if item.get_type() == ebooklib.ITEM_DOCUMENT][0]
        text = item_document.get_content().decode('utf-8')
        bs_text = BeautifulSoup(text, 'html.parser')
        bs_text = self.decompose(bs_text)

        for div in bs_text.find_all('div'):
            current_section = TextSection(order_number=section_number)
            current_paragraph = []
            current_class = None

            if div.get('class') and any(c in div.get('class') for c in self.special_classes):
                section_class = div.get('class')[0]
                match section_class:
                    case 'Tekst_TUSSENK':
                        pass
                    case 'Kop-groot':
                        pass
                    case '_idGenObjectStyleOverride-1':
                        pass
                    case _:
                        pass

            elements = div.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'table', 'ul', 'ol'])
            for element in elements:
                text_content = element.get_text(strip=True)
                if text_content:
                    if element.name.startswith('h'):
                        self._flush_paragraph(current_paragraph, current_section)
                        current_paragraph = []
                        current_class = None

                        if not current_section.title:
                            current_section.title = text_content
                        elif not current_section.subtitle:
                            current_section.subtitle = text_content
                        continue

                    element_class = tuple(element.get('class', []))

                    if element_class and any(c in element_class for c in ['Tekst_TUSSENKOP']):
                        self._flush_paragraph(current_paragraph, current_section)
                        current_section.subtitle = text_content
                        current_paragraph = []
                        current_class = None

                    else:
                        # Regular paragraph handling
                        if current_class != element_class:
                            self._flush_paragraph(current_paragraph, current_section)
                            current_paragraph = []
                            current_class = element_class
                        current_paragraph.append(text_content)

            # Flush any remaining paragraph at the end of the div
            self._flush_paragraph(current_paragraph, current_section)

            # Only add sections that have content
            if (current_section.title or current_section.paragraphs
                    or current_section.side_notes):
                self.sections.append(current_section)
                section_number += 1

    def _flush_paragraph(self, current_paragraph: List[str], section: TextSection):
        if current_paragraph:
            combined_text = ' '.join(current_paragraph)
            section.paragraphs.append(combined_text)

    def decompose(self, bs_text):
        for element in bs_text(["script", "style"]):
            element.decompose()
        return bs_text


if __name__ == "__main__":
    file_path = r"C:\Users\user\PycharmProjects\pythonProject8\Krzysztof\Beijenberg\000-000_Bleijenberg.epub"
    reader = Scrapper(file_path)
    # reader.print_metadata()
    # print(reader.get_text())

    # Print all sections with their content
    for i, section in enumerate(reader.sections, 1):
        print(f"\n{'=' * 50}")
        print(f"SECTION {i}")
        print(f"{'=' * 50}")

        if section.title:
            print(f"\nTITLE: {section.title}")

        if section.subtitle:
            print(f"\nSUBTITLE: {section.subtitle}")

        if section.paragraphs:
            print(f"\nPARAGRAPHS ({len(section.paragraphs)}):")
            for j, para in enumerate(section.paragraphs, 1):
                # Print first 100 characters of each paragraph
                preview = para[:100] + "..." if len(para) > 100 else para
                print(f"\n{j}. {preview}")

        if section.side_notes:
            print(f"\nSIDE NOTES ({len(section.side_notes)}):")
            for j, note in enumerate(section.side_notes, 1):
                preview = note[:50] + "..." if len(note) > 50 else note
                print(f"{j}. {preview}")

        print("\n" + "-" * 50)
