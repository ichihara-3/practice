import Bun from 'bun';

/**
 * package.json から抽出された依存関係情報を表すインターフェース。
 */
export interface PackageDependencies {
  filePath: string;
  dependencies: Record<string, string>;
  devDependencies: Record<string, string>;
  peerDependencies?: Record<string, string>;
  optionalDependencies?: Record<string, string>;
}

/**
 * 指定されたパスの package.json ファイルを非同期に読み込み、解析します。
 *
 * @param filePath package.json ファイルへの絶対パス。
 * @returns 解析された依存関係情報を含む PackageDependencies オブジェクト、またはエラーの場合は null。
 */
export async function parsePackageJson(filePath: string): Promise<PackageDependencies | null> {
  try {
    const file = Bun.file(filePath);
    if (!(await file.exists())) {
      console.error(`Error: package.json not found at ${filePath}`);
      return null;
    }

    const content = await file.json();

    // content がオブジェクトであることを確認（より厳密な型ガードが望ましい）
    if (typeof content !== 'object' || content === null) {
        console.error(`Error: Invalid JSON content in ${filePath}`);
        return null;
    }

    // 依存関係の抽出（存在しない場合は空オブジェクトをデフォルトとする）
    const dependencies = content.dependencies ?? {};
    const devDependencies = content.devDependencies ?? {};
    const peerDependencies = content.peerDependencies; // オプショナル
    const optionalDependencies = content.optionalDependencies; // オプショナル

    // 他のプロパティも必要に応じて型チェック・抽出

    return {
      filePath,
      dependencies,
      devDependencies,
      ...(peerDependencies && { peerDependencies }), // 条件付きで追加
      ...(optionalDependencies && { optionalDependencies }), // 条件付きで追加
    };
  } catch (error) {
    console.error(`Error parsing package.json at ${filePath}:`, error);
    return null;
  }
}
