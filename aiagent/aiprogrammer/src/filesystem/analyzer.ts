import { globby, type GlobEntry } from 'globby'; 
import fs from 'fs/promises';
import path from 'path';
import { z } from 'zod';

// Zodスキーマ定義
export const FileMetaSchema = z.object({
  path: z.string(),
  type: z.enum(['file', 'directory']),
  size: z.number().optional(), 
  modified: z.date().optional(),
  language: z.string().optional(), 
});

export type FileMeta = z.infer<typeof FileMetaSchema>;

/**
 * ディレクトリを再帰的に走査しファイルメタデータを収集
 */
export async function scanDirectory(
  rootPath: string,
  options: { ignorePatterns?: string[] } = {}
): Promise<FileMeta[]> {
  const entries: GlobEntry[] = await globby(['**/*'], {
    cwd: rootPath,
    gitignore: true,
    ignore: options.ignorePatterns,
    absolute: true,
    stats: true,
    objectMode: true, 
    dot: true, // ドットファイルも検索対象に含める
    onlyFiles: false, // ディレクトリも結果に含めることを明示
  });

  return entries.map((entry) => {
    if (!entry.stats) {
      console.warn(`Stats missing for entry: ${entry.path}`);
      return FileMetaSchema.parse({
          path: entry.path,
          type: 'file', 
      });
    }
    return FileMetaSchema.parse({
      path: entry.path,
      type: entry.stats.isDirectory() ? 'directory' : 'file',
      size: entry.stats.size,
      modified: entry.stats.mtime,
    });
  });
}
