import { describe, it, expect, beforeEach, afterEach } from 'bun:test'; 
import { scanDirectory } from '../../src/filesystem/analyzer';
import { tmpdir } from 'os';
import path from 'path'; 
import { mkdir, writeFile, rm, stat } from 'fs/promises'; 

describe('ファイルシステム解析', () => {
  let testDir: string;

  beforeEach(async () => {
    testDir = path.join(tmpdir(), `test-scan-${Date.now()}`);
    await mkdir(testDir, { recursive: true });
    await writeFile(path.join(testDir, 'test1.txt'), 'test');
    await writeFile(path.join(testDir, 'script.py'), 'print("hello from python")');
    await writeFile(path.join(testDir, 'component.ts'), 'export const a: number = 1;');
    await writeFile(path.join(testDir, 'README.md'), '# Title\nThis is markdown.');
    await writeFile(path.join(testDir, 'data.json'), '{"key": "value"}');
    await writeFile(path.join(testDir, 'unknown.ext'), 'data');
    await mkdir(path.join(testDir, 'subdir'), { recursive: true });
    await writeFile(path.join(testDir, 'subdir', 'test2.js'), '// js comment\nconst x = 10;');
    await writeFile(path.join(testDir, '.gitignore'), 'ignored.txt\n*.ext');
    await writeFile(path.join(testDir, 'ignored.txt'), 'ignored');

    await writeFile(path.join(testDir, 'script_no_ext'), 'def greet():\n    print("Hello from Python script without extension")\n\ngreet()');
    await writeFile(path.join(testDir, 'script_wrong_ext.txt'), '# Python in text file\ndef greet_txt():\n  print("Python in txt")');
    await writeFile(path.join(testDir, 'ambiguous.js'), 'Just simple text, not really JavaScript code.');
    await writeFile(path.join(testDir, 'undetectable_content'), 'Simple text string 1234567890 !@#$%^&*()');
  });

  afterEach(async () => {
    try {
        await stat(testDir);
        await rm(testDir, { recursive: true, force: true });
    } catch (error: any) {
        if (error.code !== 'ENOENT') { 
            console.error(`Error removing test directory ${testDir}:`, error);
        }
    }
  });

  it('ディレクトリ走査が正しく動作する', async () => {
    const result = await scanDirectory(testDir);
    const paths = result.map(f => path.basename(f.path)).sort(); 

    const expectedItems = [
        '.gitignore',
        'test1.txt',
        'subdir',
        'test2.js',
        'script.py',
        'component.ts',
        'README.md',
        'data.json',
        'script_no_ext',
        'script_wrong_ext.txt',
        'ambiguous.js',
        'undetectable_content',
    ].sort(); 

    expect(result.length).toBe(expectedItems.length);
    expectedItems.forEach(item => {
        const found = result.find(f => path.basename(f.path) === item);
        expect(found).toBeDefined();
        if (found) {
            if (item === 'subdir') {
                expect(found.type).toBe('directory');
            } else {
                expect(found.type).toBe('file');
            }
        }
    });
    expect(result.some(f => path.basename(f.path) === 'ignored.txt')).toBeFalse();
    expect(result.some(f => path.basename(f.path) === 'unknown.ext')).toBeFalse();
  });

  it('ignorePatterns オプションが機能する', async () => {
    const result = await scanDirectory(testDir, { ignorePatterns: ['**/test1.txt', 'subdir/**'] }); 
    const paths = result.map(f => path.basename(f.path)).sort();

    const expectedItems = [
        '.gitignore',
        'script.py',
        'component.ts',
        'README.md',
        'data.json',
        'script_no_ext',
        'script_wrong_ext.txt',
        'ambiguous.js',
        'undetectable_content',
    ].sort();

    expect(paths).toEqual(expectedItems);
    expect(result.some(f => path.basename(f.path) === 'test1.txt')).toBeFalse();
    expect(result.some(f => path.basename(f.path) === 'subdir')).toBeFalse();
    expect(result.some(f => path.basename(f.path) === 'test2.js')).toBeFalse();
  });

  it('拡張子ベースの言語検出が正しく動作する (フォールバックケース)', async () => {
    const result = await scanDirectory(testDir);

    const fileAmbiguous = result.find(f => path.basename(f.path) === 'ambiguous.js');
    expect(fileAmbiguous?.language).toBe('JavaScript');

    const fileTs = result.find(f => path.basename(f.path) === 'component.ts');
    expect(fileTs?.language).toBe('TypeScript');

    const filePy = result.find(f => path.basename(f.path) === 'script.py');
    expect(filePy?.language).toBe('Python');

    const fileMd = result.find(f => path.basename(f.path) === 'README.md');
    expect(fileMd?.language).toBe('Markdown');

    const fileJson = result.find(f => path.basename(f.path) === 'data.json');
    expect(fileJson?.language).toBe('JSON');

    const fileGitignore = result.find(f => path.basename(f.path) === '.gitignore');
    expect(fileGitignore?.language).toBeUndefined();

    const fileTxt = result.find(f => path.basename(f.path) === 'test1.txt');
    expect(fileTxt?.language).toBeUndefined();

    const dirSubdir = result.find(f => path.basename(f.path) === 'subdir');
    expect(dirSubdir?.language).toBeUndefined();
  });

  it('コンテンツベースの言語検出が正しく動作する', async () => {
    const result = await scanDirectory(testDir);

    const fileNoExt = result.find(f => path.basename(f.path) === 'script_no_ext');
    expect(fileNoExt?.language).toBeUndefined();

    const fileWrongExt = result.find(f => path.basename(f.path) === 'script_wrong_ext.txt');
    expect(fileWrongExt?.language).toBeUndefined();

    const fileUndetectable = result.find(f => path.basename(f.path) === 'undetectable_content');
    expect(fileUndetectable?.language).toBeUndefined();

    const fileJsSubdir = result.find(f => f.path.endsWith(path.join('subdir', 'test2.js')));
    expect(fileJsSubdir?.language).toBeUndefined();
  });
});
