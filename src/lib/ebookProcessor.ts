import EPub from "epub";
import { Chapter } from "@/types/book";

export const processEbook = async (file: File): Promise<Chapter[]> => {
  if (file.name.endsWith('.txt')) {
    const text = await file.text();
    return processTxtFile(text);
  } else if (file.name.endsWith('.epub')) {
    return processEpubFile(file);
  } else if (file.name.endsWith('.pdf')) {
    throw new Error('PDF processing is not yet implemented. Please convert your PDF to EPUB or TXT format.');
  }
  
  throw new Error('Unsupported file format');
};

const processTxtFile = (text: string): Chapter[] => {
  // Simple chapter detection based on "Chapter" keyword
  const chapterRegex = /Chapter\s+\d+/gi;
  const splits = text.split(chapterRegex);
  const chapters: Chapter[] = [];
  
  // Skip the first split if it's empty (before first chapter)
  let startIndex = splits[0].trim().length === 0 ? 1 : 0;
  
  for (let i = startIndex; i < splits.length; i++) {
    chapters.push({
      number: i,
      content: splits[i].trim(),
    });
  }
  
  return chapters;
};

const processEpubFile = async (file: File): Promise<Chapter[]> => {
  return new Promise((resolve, reject) => {
    // Convert File to Buffer
    file.arrayBuffer().then(buffer => {
      const epubBook = new EPub(Buffer.from(buffer));
      
      epubBook.on('end', () => {
        // Get the table of contents
        const chapters: Chapter[] = [];
        let chapterNumber = 1;

        // Process each chapter from the spine
        epubBook.spine.contents.forEach((item: any) => {
          epubBook.getChapter(item.id, (error: Error | null, text: string) => {
            if (error) {
              console.error('Error processing chapter:', error);
              return;
            }

            // Remove HTML tags and clean up the text
            const cleanText = text.replace(/<[^>]*>/g, ' ')
                                .replace(/\s+/g, ' ')
                                .trim();

            chapters.push({
              number: chapterNumber++,
              content: cleanText,
            });

            // Resolve when all chapters are processed
            if (chapters.length === epubBook.spine.contents.length) {
              resolve(chapters.sort((a, b) => a.number - b.number));
            }
          });
        });
      });

      epubBook.on('error', reject);
      epubBook.parse();
    });
  });
};