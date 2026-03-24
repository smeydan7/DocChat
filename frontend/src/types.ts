export type SourceChunk = {
  document_id: string;
  chunk_index: number;
  text: string;
};

export type AskResponse = {
  answer: string;
  sources: SourceChunk[];
};
