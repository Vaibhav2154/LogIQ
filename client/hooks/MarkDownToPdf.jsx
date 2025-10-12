'use client';

import html2pdf from "html2pdf.js";
import { marked } from "marked";

// Function to export markdown to PDF
export const exportMarkdownToPdf = (markdownContent) => {
  // 1. Create a temporary container
  const container = document.createElement("div");
  container.style.padding = "20px";
  container.style.background = "white";
  container.style.color = "black";
  container.style.fontFamily = "system-ui, sans-serif";

  // 2. Convert markdown to HTML
  container.innerHTML = marked.parse(markdownContent);

  // 3. Add some simple styling for neat formatting
  const style = document.createElement("style");
  style.innerHTML = `
    h1 { font-size: 24px; font-weight: bold; margin-bottom: 10px; }
    h2 { font-size: 20px; font-weight: bold; margin-bottom: 8px; }
    h3 { font-size: 18px; font-weight: bold; margin-bottom: 6px; }
    p { margin-bottom: 6px; line-height: 1.5; }
    li { margin-bottom: 4px; }
    code { font-family: monospace; background: #f6f8fa; padding: 2px 4px; border-radius: 4px; font-size: 0.9em; }
    pre { background: #f6f8fa; padding: 10px; border-radius: 6px; overflow-x: auto; }
    blockquote { border-left: 4px solid #ddd; padding-left: 10px; color: #555; margin: 6px 0; }
  `;
  container.appendChild(style);

  // 4. Generate PDF
  const options = {
    margin: 0.5,
    filename: "markdown.pdf",
    image: { type: "jpeg", quality: 0.98 },
    html2canvas: { scale: 2 },
    jsPDF: { unit: "in", format: "a4", orientation: "portrait" },
  };

  html2pdf()
    .set(options)
    .from(container)
    .outputPdf("blob")
    .then((pdfBlob) => {
      const blobUrl = URL.createObjectURL(pdfBlob);
      window.open(blobUrl); // open PDF in new tab
    });
};
