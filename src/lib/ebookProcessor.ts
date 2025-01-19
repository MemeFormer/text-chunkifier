import { Chapter } from "@/types/book";
import * as epub from "epub";

export const processEbook = async (file: File): Promise<Chapter[]> => {
  const text = await file.text();
  
  if (file.name.endsWith('.txt')) {
    return processTxtFile(text);
  } else if (file.name.endsWith('.epub')) {
    return processEpubFile(file);
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
  // This is a placeholder for epub processing
  // You would need to implement the actual epub parsing logic here
  // using the epub library
  return processTxtFile(await file.text());
};