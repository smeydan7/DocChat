export type SourceChunk = {
  document_id: string;
  chunk_index: number;
  text: string;
};

export type AskResponse = {
  answer: string;
  sources: SourceChunk[];
};

export type UploadResponse = {
  document_id: string;
  file_name: string;
  chunk_count: number;
  message: string;
};
