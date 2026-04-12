import { parse as parseYaml } from 'yaml';

export interface Card {
  question: string;
  answer: string;
  explanation?: string;
  guid: string;
}

export interface Paper {
  slug: string;
  paper_title: string;
  paper_url: string;
  cards: Card[];
  cardCount: number;
}

/**
 * Parse a flashcard markdown file in Obsidian callout format
 */
export function parseFlashcardFile(slug: string, rawContent: string): Paper {
  // Extract frontmatter
  const frontmatterMatch = rawContent.match(/^---\n([\s\S]*?)\n---/);
  let paper_title = '';
  let paper_url = '';

  if (frontmatterMatch) {
    const frontmatter = parseYaml(frontmatterMatch[1]) as Record<string, any>;
    paper_title = frontmatter.paper_title || '';
    paper_url = frontmatter.paper_url || '';
  }

  // Remove frontmatter from content
  const bodyStart = frontmatterMatch ? frontmatterMatch[0].length : 0;
  const body = rawContent.substring(bodyStart).trim();

  // Split cards by --- separator
  const cardBlocks = body.split('\n---\n').filter(block => block.trim());

  // Parse each card block
  const cards: Card[] = cardBlocks.map(cardBlock => parseCard(cardBlock.trim()));

  return {
    slug,
    paper_title,
    paper_url,
    cards,
    cardCount: cards.length
  };
}

function parseCard(blockContent: string): Card {
  let question = '';
  let answer = '';
  let explanation: string | undefined;
  let guid = '';

  // Extract GUID from HTML comment
  const guidMatch = blockContent.match(/<!--\s*guid:\s*([^\s>]+)\s*-->/);
  if (guidMatch) {
    guid = guidMatch[1];
  }

  // Remove GUID comment from content
  const contentWithoutGuid = blockContent.replace(/<!--\s*guid:\s*[^\s>]+\s*-->/g, '').trim();

  // Parse callout blocks
  // Match [!question] block
  const questionMatch = contentWithoutGuid.match(/^>\s*\[!question\]\n((?:>.*\n?)*)/m);
  if (questionMatch) {
    question = extractCalloutContent(questionMatch[1]);
  }

  // Match [!answer]- block
  const answerMatch = contentWithoutGuid.match(/^>\s*\[!answer\]-\n((?:>.*\n?)*)/m);
  if (answerMatch) {
    answer = extractCalloutContent(answerMatch[1]);
  }

  // Match [!explanation]- block
  const explanationMatch = contentWithoutGuid.match(/^>\s*\[!explanation\]-\n((?:>.*\n?)*)/m);
  if (explanationMatch) {
    explanation = extractCalloutContent(explanationMatch[1]);
  }

  // Convert Obsidian image syntax to markdown
  question = convertImageSyntax(question);
  answer = convertImageSyntax(answer);
  if (explanation) {
    explanation = convertImageSyntax(explanation);
  }

  return {
    question,
    answer,
    explanation: explanation || undefined,
    guid
  };
}

/**
 * Extract content from blockquote lines (lines starting with > )
 */
function extractCalloutContent(blockContent: string): string {
  return blockContent
    .split('\n')
    .map(line => {
      // Remove leading > and optional space
      return line.replace(/^>\s?/, '');
    })
    .join('\n')
    .trim()
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'");
}

/**
 * Convert Obsidian wiki-link image syntax ![[filename]] to markdown ![filename](/media/filename)
 * Also handle standard markdown ![](url) syntax (leave external URLs unchanged)
 */
function convertImageSyntax(content: string): string {
  // Convert ![[image.png]] to ![image.png](/media/image.png)
  return content.replace(/!\[\[([^\]]+)\]\]/g, (match, filename) => {
    return `![${filename}](/media/${filename})`;
  });
}
