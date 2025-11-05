import Loading from "@/CustomHooks/loading";
import { Loader2Icon } from "lucide-react";
import { useState } from "react";
import { Document, Page, pdfjs } from "react-pdf";

pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  "pdfjs-dist/build/pdf.worker.min.mjs",
  import.meta.url
).toString();

interface OpenPdfProps {
  fileUrl: string;
}

function PdfComp({ fileUrl }: OpenPdfProps) {
  const [numPages, setNumPages] = useState<number>(0);
  const [pageNumber, setPageNumber] = useState<number>(1);

  function onDocumentLoadSuccess({ numPages }: { numPages: number }): void {
    setNumPages(numPages);
  }

  return (
    <div className="pdf-div">
      <p>
        Page {pageNumber} of {numPages}
      </p>

      <Document
        file={fileUrl}
        onLoadSuccess={onDocumentLoadSuccess}
        loading={<Loading />}
        error={
          <p className="text-red-500 text-center mt-4 font-semibold">
            Failed to load PDF.
          </p>
        }
      >
        {Array.from(new Array(numPages), (_, index) => (
          <Page
            key={`page_${index + 1}`}
            pageNumber={index + 1}
            renderTextLayer={false}
            renderAnnotationLayer={false}
          />
        ))}
      </Document>
    </div>
  );
}

export default PdfComp;
