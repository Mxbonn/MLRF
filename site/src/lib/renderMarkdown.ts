import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkMath from 'remark-math';
import remarkBreaks from 'remark-breaks';
import remarkRehype from 'remark-rehype';
import rehypeKatex from 'rehype-katex';
import rehypeStringify from 'rehype-stringify';

let processor: any = null;

function getProcessor() {
  if (!processor) {
    processor = unified()
      .use(remarkParse)
      .use(remarkMath)
      .use(remarkBreaks)
      .use(remarkRehype, { allowDangerousHtml: true })
      .use(rehypeKatex)
      .use(rehypeStringify, { allowDangerousHtml: true });
  }
  return processor;
}

/**
 * Render markdown to HTML with math support
 * Called at build time for flashcard content
 */
export async function renderMarkdown(md: string): Promise<string> {
  try {
    const processor = getProcessor();
    const result = await processor.process(md);
    return String(result);
  } catch (error) {
    console.error('Markdown rendering error:', error);
    return md; // Fallback to raw markdown on error
  }
}
