import { describe, it, expect, beforeEach, afterEach } from 'bun:test'; 
import { scanDirectory } from '../../src/filesystem/analyzer';
import { tmpdir } from 'os';
import path from 'path'; 
import { mkdir, writeFile, rm } from 'fs/promises'; 

describe('ファイルシステム解析', () => {
  let testDir: string;

  beforeEach(async () => {
    testDir = path.join(tmpdir(), `test-scan-${Date.now()}`); 
    await mkdir(testDir, { recursive: true });
    await writeFile(path.join(testDir, 'test1.txt'), 'test'); 
    await mkdir(path.join(testDir, 'subdir'), { recursive: true }); 
    await writeFile(path.join(testDir, 'subdir', 'test2.js'), '// js'); 
    await writeFile(path.join(testDir, '.gitignore'), 'ignored.txt'); 
    await writeFile(path.join(testDir, 'ignored.txt'), 'ignored'); 
  });

  afterEach(async () => {
    await rm(testDir, { recursive: true, force: true });
  });

  it('ディレクトリ走査が正しく動作する', async () => {
    const result = await scanDirectory(testDir);
    const paths = result.map(f => path.basename(f.path)); 
    console.log("Detected paths:", paths); 

    const expectedItems = ['.gitignore', 'test1.txt', 'subdir', 'test2.js'];

    expect(result.length).toBe(expectedItems.length);
    expectedItems.forEach(item => {
        const found = result.find(f => path.basename(f.path) === item); 
        expect(found).toBeDefined(); 
        if (item === 'subdir') {
            expect(found?.type).toBe('directory');
        } else {
            expect(found?.type).toBe('file');
        }
    });
    expect(result.some(f => path.basename(f.path) === 'ignored.txt')).toBeFalse(); 
  });

  it('ignorePatterns オプションが機能する', async () => {
    const result = await scanDirectory(testDir, { ignorePatterns: ['**/test1.txt'] });
    const paths = result.map(f => path.basename(f.path)); 
    console.log("Detected paths (ignored):", paths);

    const expectedItems = ['.gitignore', 'subdir', 'test2.js'];

    expect(result.length).toBe(expectedItems.length);
    expectedItems.forEach(item => {
        const found = result.find(f => path.basename(f.path) === item); 
        expect(found).toBeDefined();
        if (item === 'subdir') {
            expect(found?.type).toBe('directory');
        } else {
            expect(found?.type).toBe('file');
        }
    });
    expect(result.some(f => path.basename(f.path) === 'test1.txt')).toBeFalse(); 
  });
});
