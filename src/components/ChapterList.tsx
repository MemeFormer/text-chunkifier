import { Button } from "@/components/ui/button";
import { Chapter } from "@/types/book";
import { Check } from "lucide-react";

interface ChapterListProps {
  chapters: Chapter[];
  processedChapters: Set<number>;
  onDownload: (chapter: Chapter) => void;
}

const ChapterList = ({ chapters, processedChapters, onDownload }: ChapterListProps) => {
  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-serif font-semibold text-slate-900 mb-4">
        Chapters
      </h2>
      <div className="grid gap-4">
        {chapters.map((chapter) => (
          <div
            key={chapter.number}
            className="bg-white rounded-lg shadow-sm p-4 flex items-center justify-between"
          >
            <div>
              <h3 className="font-medium text-slate-900">
                Chapter {chapter.number}
              </h3>
              <p className="text-sm text-slate-600">
                {chapter.content.slice(0, 100)}...
              </p>
            </div>
            <div className="flex items-center gap-2">
              {processedChapters.has(chapter.number) && (
                <Check className="text-green-500 w-5 h-5" />
              )}
              <Button
                onClick={() => onDownload(chapter)}
                variant="outline"
                className="ml-4"
              >
                Download
              </Button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ChapterList;