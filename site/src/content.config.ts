import { defineCollection } from 'astro:content';
import { z } from 'astro:content';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { parseFlashcardFile } from './lib/parseFlashcards';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const flashcardsDir = path.resolve(__dirname, '..', '..', 'flashcards');

const cardSchema = z.object({
  question: z.string(),
  answer: z.string(),
  explanation: z.string().optional(),
  guid: z.string()
});

const paperSchema = z.object({
  slug: z.string(),
  paper_title: z.string(),
  paper_url: z.string(),
  cards: z.array(cardSchema),
  cardCount: z.number()
});

const papers = defineCollection({
  loader: async () => {
    const entries: Record<string, any> = {};

    // Read all .md files from flashcards directory
    const files = fs.readdirSync(flashcardsDir).filter(f => f.endsWith('.md'));

    for (const file of files) {
      const slug = file.replace(/\.md$/, '');
      const filePath = path.join(flashcardsDir, file);
      const content = fs.readFileSync(filePath, 'utf-8');

      try {
        const parsed = parseFlashcardFile(slug, content);
        entries[slug] = parsed;
      } catch (error) {
        console.error(`Error parsing ${file}:`, error);
      }
    }

    return entries;
  },
  schema: paperSchema
});

export const collections = { papers };
