import { Button } from "@/components/ui/button";
import { useRef } from "react";

interface FileUploadProps {
  onFileSelect: (file: File) => void;
}

const FileUpload = ({ onFileSelect }: FileUploadProps) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      onFileSelect(file);
    }
  };

  return (
    <div className="text-center">
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleChange}
        accept=".txt,.epub,.pdf"
        className="hidden"
      />
      <Button 
        onClick={handleClick}
        className="bg-blue-500 hover:bg-blue-600 text-white"
      >
        Upload Ebook
      </Button>
      <p className="mt-2 text-sm text-slate-600">
        Supported formats: .txt, .epub, .pdf
      </p>
    </div>
  );
};

export default FileUpload;