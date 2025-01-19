import { useState } from "react";
import { Button } from "@/components/ui/button";
import { useToast } from "@/components/ui/use-toast";
import ChapterList from "@/components/ChapterList";
import FileUpload from "@/components/FileUpload";
import { processEbook } from "@/lib/ebookProcessor";
import { Chapter } from "@/types/book";

const Index = () => {
  const [chapters, setChapters] = useState<Chapter[]>([]);
  const [processedChapters, setProcessedChapters] = useState<Set<number>>(new Set());
  const { toast } = useToast();

  const handleFileUpload = async (file: File) => {
    try {
      const extractedChapters = await processEbook(file);
      setChapters(extractedChapters);
      toast({
        title: "Success",
        description: `Found ${extractedChapters.length} chapters in your ebook`,
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to process the ebook. Please try a different file.",
        variant: "destructive",
      });
    }
  };

  const handleChapterDownload = (chapter: Chapter) => {
    const blob = new Blob([chapter.content], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `chapter_${chapter.number}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    setProcessedChapters(prev => new Set([...prev, chapter.number]));
    toast({
      title: "Chapter Downloaded",
      description: `Chapter ${chapter.number} is ready for processing`,
    });
  };

  return (
    <div className="min-h-screen bg-slate-50 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-serif font-bold text-slate-900 mb-8 text-center">
          Ebook Chapter Splitter
        </h1>
        
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <FileUpload onFileSelect={handleFileUpload} />
        </div>

        {chapters.length > 0 && (
          <ChapterList 
            chapters={chapters} 
            processedChapters={processedChapters}
            onDownload={handleChapterDownload}
          />
        )}
      </div>
    </div>
  );
};

export default Index;