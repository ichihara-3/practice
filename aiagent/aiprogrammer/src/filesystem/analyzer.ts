import { globby, type GlobEntry } from 'globby'; 
import fs from 'fs/promises';
import path from 'path';
import { z } from 'zod';
import hljs from 'highlight.js'; // highlight.js をインポート

// Zodスキーマ定義
export const FileMetaSchema = z.object({
  path: z.string(),
  type: z.enum(['file', 'directory']),
  size: z.number().optional(), 
  modified: z.date().optional(),
  language: z.string().optional(), 
});

export type FileMeta = z.infer<typeof FileMetaSchema>;

// 拡張子と言語のマッピング (必要に応じて拡張)
const extensionToLanguageMap: Record<string, string> = {
  '.js': 'JavaScript',
  '.jsx': 'JavaScript',
  '.ts': 'TypeScript',
  '.tsx': 'TypeScript',
  '.py': 'Python',
  '.java': 'Java',
  '.cs': 'C#',
  '.go': 'Go',
  '.rb': 'Ruby',
  '.php': 'PHP',
  '.html': 'HTML',
  '.css': 'CSS',
  '.scss': 'SCSS',
  '.less': 'LESS',
  '.json': 'JSON',
  '.yaml': 'YAML',
  '.yml': 'YAML',
  '.md': 'Markdown',
  '.sh': 'Shell',
  '.sql': 'SQL',
  // ... 他の言語を追加
};

/**
 * ファイルパスから拡張子を取得し、対応する言語名を返す。
 * マップにない場合は undefined を返す。
 */
function getLanguageFromExtension(filePath: string): string | undefined {
  const ext = path.extname(filePath).toLowerCase();
  return extensionToLanguageMap[ext];
}

/**
 * ファイルの内容と拡張子から言語を推測する
 * 1. ファイルの先頭部分を読み込み、highlight.js で言語を推測
 * 2. 推測結果の信頼度が高ければその言語名を返す
 * 3. 失敗または信頼度が低い場合は拡張子ベースの判定にフォールバック
 */
async function detectLanguage(filePath: string): Promise<string | undefined> {
  const MAX_READ_BYTES = 2048; // 読み込む最大バイト数
  let contentBasedLanguage: string | undefined;

  try {
    // ディレクトリの場合は処理しない
    const stats = await fs.stat(filePath);
    if (stats.isDirectory()) {
      return undefined;
    }

    const handle = await fs.open(filePath, 'r');
    const buffer = Buffer.alloc(MAX_READ_BYTES);
    const { bytesRead } = await handle.read(buffer, 0, MAX_READ_BYTES, 0);
    await handle.close();

    if (bytesRead > 0) {
      const content = buffer.toString('utf-8', 0, bytesRead);
      const result = hljs.highlightAuto(content); 

      if (result.language && result.relevance > 10) { 
         contentBasedLanguage = result.language;
         const normalizedLang = Object.entries(extensionToLanguageMap).find(
            ([, lang]) => lang.toLowerCase() === contentBasedLanguage?.toLowerCase()
         )?.[1];
         if (normalizedLang) {
            // console.log(`Content detected: ${filePath} -> ${normalizedLang} (relevance: ${result.relevance})`);
            return normalizedLang;
         }
         // マップにないが検出された場合はそのまま返す (大文字始まりにする)
         const finalLang = contentBasedLanguage.charAt(0).toUpperCase() + contentBasedLanguage.slice(1);
        // console.log(`Content detected (unmapped): ${filePath} -> ${finalLang} (relevance: ${result.relevance})`);
         return finalLang;
      }
      // console.log(`Content detection low relevance: ${filePath} (lang: ${result.language}, relevance: ${result.relevance})`);
    }
  } catch (error) {
    // ファイル読み込みエラーなどは無視し、拡張子ベースの判定に進む
    // console.warn(`Could not read file for language detection: ${filePath}`, error);
  }

  // コンテンツベースで特定できなかった場合、拡張子ベースで判定
  const extLang = getLanguageFromExtension(filePath);
  // if (extLang) {
  //    console.log(`Extension fallback: ${filePath} -> ${extLang}`);
  // } else {
  //    console.log(`No language detected for: ${filePath}`);
  // }
  return extLang;
}


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
    dot: true,
    onlyFiles: false,
  });

  // map 内で非同期処理 (detectLanguage) を行うため Promise.all を使用
  const results = await Promise.all(entries.map(async (entry): Promise<FileMeta | null> => { // null を返す可能性
    try {
        const isDirectory = entry.stats?.isDirectory() ?? false;
        // detectLanguage を呼び出して言語を判定 (ディレクトリの場合は直接 undefined)
        const language = isDirectory ? undefined : await detectLanguage(entry.path);

        if (!entry.stats) {
          console.warn(`Stats missing for entry: ${entry.path}`);
          // stats がない場合は基本的な情報のみ (type は推測)
          return FileMetaSchema.parse({
              path: entry.path,
              type: isDirectory ? 'directory' : 'file', // entry の情報があれば使う
              language,
          });
        }
        return FileMetaSchema.parse({
          path: entry.path,
          type: isDirectory ? 'directory' : 'file',
          size: isDirectory ? undefined : entry.stats.size,
          modified: entry.stats.mtime,
          language,
        });
    } catch (error) {
        // 個々のファイル処理でエラーが発生しても全体を止めない
        console.error(`Error processing entry ${entry.path}:`, error);
        return null; // エラーが発生したエントリは結果から除外
    }
  }));
  // null をフィルタリングして返す
  return results.filter((result): result is FileMeta => result !== null);
}
