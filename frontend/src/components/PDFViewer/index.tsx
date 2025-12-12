interface Props {
  url?: string;
}

export default function PDFViewer({ url }: Props) {
  if (!url) return <p className="text-sm text-gray-400">PDF no generado todavía.</p>;
  return (
    <a className="text-blue-300 underline" href={url} target="_blank" rel="noreferrer">
      Abrir PDF
    </a>
  );
}
