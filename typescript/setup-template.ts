#!/usr/bin/env node
/**
 * Template setup script.
 *
 * Run this after cloning the template to customize it for your project. It will:
 *   1. Ask for your project details
 *   2. Ask which components you want to keep
 *   3. Rename files and exports
 *   4. Replace placeholder values throughout the codebase
 *   5. Delete unused components
 *   6. Delete itself when done
 *
 * Usage:
 *   npx tsx setup-template.ts
 * or
 *   npm run setup
 */

import * as fs from 'node:fs'
import * as path from 'node:path'
import * as readline from 'node:readline/promises'
import { stdin as input, stdout as output } from 'node:process'
import { fileURLToPath } from 'node:url'

// ---------------------------------------------------------------------------
// Component registry
// ---------------------------------------------------------------------------

interface ComponentSpec {
  name: string
  description: string
  files: string[]
  testFiles: string[]
  exports: string[]
}

const COMPONENTS: Record<string, ComponentSpec> = {
  tool: {
    name: 'Tool',
    description: 'Add capabilities to agents using the tool factory',
    files: ['tool.ts'],
    testFiles: ['tool.test.ts'],
    exports: ['templateTool'],
  },
  model: {
    name: 'Model Provider',
    description: 'Integrate custom LLM APIs',
    files: ['model.ts'],
    testFiles: ['model.test.ts'],
    exports: ['TemplateModel', 'TemplateModelConfig'],
  },
  plugin: {
    name: 'Plugin',
    description: 'Extend agent behavior with hooks and tools in a composable package',
    files: ['plugin.ts'],
    testFiles: ['plugin.test.ts'],
    exports: ['TemplatePlugin'],
  },
  session_manager: {
    name: 'Session Storage',
    description: 'Persist conversations across restarts',
    files: ['session-manager.ts'],
    testFiles: ['session-manager.test.ts'],
    exports: ['TemplateSnapshotStorage', 'TemplateSnapshotStorageConfig'],
  },
  conversation_manager: {
    name: 'Conversation Manager',
    description: 'Control context window and message history',
    files: ['conversation-manager.ts'],
    testFiles: ['conversation-manager.test.ts'],
    exports: ['TemplateConversationManager'],
  },
}

const SRC_DIR = 'src'
const TEST_DIR = 'test'

interface ProjectInfo {
  packageNameInput: string
  kebabName: string
  camelName: string
  pascalName: string
  selected: string[]
  authorName: string
  authorEmail: string
  githubUsername: string
  description: string
}

// ---------------------------------------------------------------------------
// String-case helpers
// ---------------------------------------------------------------------------

function toKebabCase(name: string): string {
  return name
    .replace(/[\s_]+/g, '-')
    .replace(/([a-z\d])([A-Z])/g, '$1-$2')
    .replace(/([A-Z]+)([A-Z][a-z])/g, '$1-$2')
    .toLowerCase()
}

function toCamelCase(name: string): string {
  const words = name.split(/[-_\s]+/).filter(Boolean)
  return words[0]!.toLowerCase() + words.slice(1).map((w) => w[0]!.toUpperCase() + w.slice(1).toLowerCase()).join('')
}

function toPascalCase(name: string): string {
  return name
    .split(/[-_\s]+/)
    .filter(Boolean)
    .map((w) => w[0]!.toUpperCase() + w.slice(1).toLowerCase())
    .join('')
}

// ---------------------------------------------------------------------------
// Generic file + string helpers
// ---------------------------------------------------------------------------

function applyReplacements(value: string, replacements: Record<string, string>): string {
  let out = value
  for (const [oldStr, newStr] of Object.entries(replacements)) {
    out = out.split(oldStr).join(newStr)
  }
  return out
}

function replaceInFile(filepath: string, replacements: Record<string, string>): void {
  const content = fs.readFileSync(filepath, 'utf8')
  fs.writeFileSync(filepath, applyReplacements(content, replacements), 'utf8')
}

// ---------------------------------------------------------------------------
// Interactive prompter
// ---------------------------------------------------------------------------

class Prompter {
  private readonly _rl: readline.Interface

  constructor() {
    this._rl = readline.createInterface({ input, output })
  }

  async ask(question: string, defaultValue = ''): Promise<string> {
    const suffix = defaultValue ? ` [${defaultValue}]` : ''
    const answer = (await this._rl.question(`${question}${suffix}: `)).trim()
    return answer || defaultValue
  }

  close(): void {
    this._rl.close()
  }
}

// ---------------------------------------------------------------------------
// Project info gathering
// ---------------------------------------------------------------------------

async function selectComponents(prompter: Prompter): Promise<string[]> {
  console.log('\nWhich components do you want to include?\n')

  const keys = Object.keys(COMPONENTS)
  keys.forEach((key, i) => {
    const c = COMPONENTS[key]!
    console.log(`  ${i + 1}. ${c.name} - ${c.description}`)
  })

  const selection = await prompter.ask('\nEnter numbers separated by commas (e.g., 1,2)', '1')
  const selected: string[] = []
  for (const part of selection.split(',')) {
    const idx = Number.parseInt(part.trim(), 10) - 1
    if (Number.isInteger(idx) && idx >= 0 && idx < keys.length) {
      selected.push(keys[idx]!)
    }
  }

  if (selected.length === 0) {
    console.error('❌ No valid components selected')
    process.exit(1)
  }

  return selected
}

async function gatherProjectInfo(prompter: Prompter): Promise<ProjectInfo> {
  const packageNameInput = await prompter.ask("Package name (e.g., 'google', 'aws', 'slack')")
  if (!packageNameInput) {
    console.error('❌ Package name is required')
    process.exit(1)
  }

  const kebabName = toKebabCase(packageNameInput)
  const pascalName = toPascalCase(packageNameInput)
  const camelName = toCamelCase(packageNameInput)

  console.log(`\n  npm package: strands-${kebabName}`)
  console.log(`  Classes:     ${pascalName}Model, ${pascalName}Plugin, etc.`)
  console.log(`  Tool:        ${camelName}Tool`)

  const selected = await selectComponents(prompter)
  const selectedNames = selected.map((k) => COMPONENTS[k]!.name)
  console.log(`\n  Selected: ${selectedNames.join(', ')}`)

  console.log()
  const authorName = await prompter.ask('Author name', 'Your Name')
  const authorEmail = await prompter.ask('Author email', 'your.email@example.com')
  const githubUsername = await prompter.ask('GitHub username', 'yourusername')
  const description = await prompter.ask('Package description', `Strands Agents components for ${packageNameInput}`)

  console.log('\n' + '='.repeat(50))
  const confirm = await prompter.ask('\nProceed with setup? (y/n)', 'y')
  if (confirm.toLowerCase() !== 'y') {
    console.log('Setup cancelled.')
    process.exit(0)
  }

  return {
    packageNameInput,
    kebabName,
    camelName,
    pascalName,
    selected,
    authorName,
    authorEmail,
    githubUsername,
    description,
  }
}

function buildReplacements(info: ProjectInfo): Record<string, string> {
  const { kebabName, camelName, pascalName, authorName, authorEmail, githubUsername, description } = info
  return {
    // Package name
    'strands-template': `strands-${kebabName}`,
    // Module file names. Order matters: do this before TemplateXxx replacements
    // so the file names in the index.ts get rewritten too.
    'session-manager': `${kebabName}-session-manager`,
    'conversation-manager': `${kebabName}-conversation-manager`,
    // Class names
    TemplateModelConfig: `${pascalName}ModelConfig`,
    TemplateModel: `${pascalName}Model`,
    TemplatePlugin: `${pascalName}Plugin`,
    TemplateSnapshotStorageConfig: `${pascalName}SnapshotStorageConfig`,
    TemplateSnapshotStorage: `${pascalName}SnapshotStorage`,
    TemplateConversationManager: `${pascalName}ConversationManager`,
    // Tool function name
    templateTool: `${camelName}Tool`,
    // Plugin name string in initializer
    'template-plugin': `${kebabName}-plugin`,
    'template-conversation-manager': `${kebabName}-conversation-manager`,
    template_tool: `${camelName.replace(/([A-Z])/g, '_$1').toLowerCase()}_tool`,
    // Author/repo metadata
    'Your Name': authorName,
    'your.email@example.com': authorEmail,
    yourusername: githubUsername,
    'Your package description': description,
  }
}

// ---------------------------------------------------------------------------
// Component file operations
// ---------------------------------------------------------------------------

function processSelectedFiles(selected: string[], replacements: Record<string, string>): void {
  const filesToProcess: string[] = ['package.json', 'README.md']
  for (const key of selected) {
    const info = COMPONENTS[key]!
    for (const filename of info.files) filesToProcess.push(path.join(SRC_DIR, filename))
    for (const filename of info.testFiles) filesToProcess.push(path.join(TEST_DIR, filename))
  }

  for (const filepath of filesToProcess) {
    if (fs.existsSync(filepath)) {
      replaceInFile(filepath, replacements)
      console.log(`  ✓ Updated ${filepath}`)
    }
  }
}

function deleteUnusedComponents(selected: string[]): void {
  for (const [key, info] of Object.entries(COMPONENTS)) {
    if (selected.includes(key)) continue

    for (const filename of info.files) {
      const p = path.join(SRC_DIR, filename)
      if (fs.existsSync(p)) {
        fs.unlinkSync(p)
        console.log(`  ✓ Removed ${p}`)
      }
    }
    for (const filename of info.testFiles) {
      const p = path.join(TEST_DIR, filename)
      if (fs.existsSync(p)) {
        fs.unlinkSync(p)
        console.log(`  ✓ Removed ${p}`)
      }
    }
  }
}

function renameSelectedFiles(selected: string[], replacements: Record<string, string>): void {
  // Re-derive the new file name from replacements (e.g. session-manager.ts ->
  // <kebab>-session-manager.ts).
  const renameIn = (dir: string, filename: string): void => {
    const oldPath = path.join(dir, filename)
    const newPath = path.join(dir, applyReplacements(filename, replacements))
    if (oldPath !== newPath && fs.existsSync(oldPath)) {
      fs.renameSync(oldPath, newPath)
      console.log(`  ✓ Renamed ${oldPath} → ${newPath}`)
    }
  }

  for (const key of selected) {
    const info = COMPONENTS[key]!
    for (const filename of info.files) renameIn(SRC_DIR, filename)
    for (const filename of info.testFiles) renameIn(TEST_DIR, filename)
  }
}

function writeIndexFile(selected: string[], replacements: Record<string, string>): void {
  const lines: string[] = []
  lines.push('/**')
  lines.push(' * Strands Package.')
  lines.push(' */')
  lines.push('')

  for (const key of selected) {
    const info = COMPONENTS[key]!
    const moduleName = info.files[0]!.replace(/\.ts$/, '')
    const newModuleName = applyReplacements(moduleName, replacements)
    const renamed = info.exports.map((e) => applyReplacements(e, replacements))

    if (renamed.length === 1) {
      lines.push(`export { ${renamed[0]} } from './${newModuleName}.js'`)
    } else {
      const value = renamed[0]!
      const types = renamed.slice(1).map((t) => `type ${t}`)
      lines.push(`export { ${value}, ${types.join(', ')} } from './${newModuleName}.js'`)
    }
  }

  lines.push('')
  const indexPath = path.join(SRC_DIR, 'index.ts')
  fs.writeFileSync(indexPath, lines.join('\n'), 'utf8')
  console.log(`  ✓ Wrote ${indexPath}`)
}

// ---------------------------------------------------------------------------
// Monorepo cleanup
// ---------------------------------------------------------------------------

function removeTemplateOnlyFiles(): void {
  // These live at the repo root (one level up from typescript/) since this is
  // a monorepo template.
  const cleanupTargets = ['../CODE_OF_CONDUCT.md', '../CONTRIBUTING.md', '../NOTICE']
  for (const target of cleanupTargets) {
    if (fs.existsSync(target)) {
      fs.rmSync(target, { recursive: true, force: true })
      console.log(`  ✓ Removed ${target}`)
    }
  }
}

function stripMonorepoFromReadme(): void {
  const readmePath = 'README.md'
  if (!fs.existsSync(readmePath)) return
  const lines = fs.readFileSync(readmePath, 'utf8').split('\n')
  const out: string[] = []
  // The "Run the setup script" section walks users through a script that has
  // self-deleted by the time they read this README, so drop it and renumber
  // the next heading.
  let skipSetupSection = false
  for (const line of lines) {
    if (line.startsWith('### 2. Run the setup script')) {
      skipSetupSection = true
      continue
    }
    if (skipSetupSection) {
      if (line.startsWith('### ')) {
        skipSetupSection = false
        out.push(line.replace(/^### 3\. /, '### 2. '))
      }
      continue
    }
    if (line.includes('This is the TypeScript half of the')) continue
    if (line.includes('Apache 2.0 — see [LICENSE](../LICENSE)')) {
      out.push('Apache 2.0 — see [LICENSE](LICENSE) for details.')
      continue
    }
    let next = line
    // The hoist puts the package at the repo root, so the typescript/ subdir
    // referenced in the clone instructions no longer exists.
    next = next.replace(/cd your-repo-name\/typescript/g, 'cd your-repo-name')
    // Without the setup script, this preamble no longer makes sense.
    next = next.replace(
      /After the setup script finishes, install peer \+ dev dependencies:/g,
      'Install peer and dev dependencies:',
    )
    next = next.replace(
      /tag prefixed `typescript-v` \(e\.g\. `typescript-v0\.1\.0`\)/g,
      'tag prefixed `v` (e.g. `v0.1.0`)',
    )
    next = next.replace(/ The prefix lets the monorepo distinguish python and typescript releases\./g, '')
    next = next.replace(/`typescript-v0\.1\.0`/g, '`v0.1.0`')
    out.push(next)
  }
  fs.writeFileSync(readmePath, out.join('\n'), 'utf8')
  console.log(`  ✓ De-monorepoized ${readmePath}`)
}

function hoistWorkflows(): void {
  const workflowsDir = '../.github/workflows'

  const ciSrc = path.join(workflowsDir, 'ci-typescript.yml')
  if (fs.existsSync(ciSrc)) {
    let ci = fs.readFileSync(ciSrc, 'utf8')
    ci = ci.replace('name: CI - TypeScript', 'name: CI')
    ci = ci.replace(/\n {4}paths:\n(?: {6}- .+\n)+/g, '\n')
    ci = ci.replace(/\ndefaults:\n {2}run:\n {4}working-directory: typescript\n/, '\n')
    ci = ci.split('typescript/package-lock.json').join('package-lock.json')
    const ciDst = path.join(workflowsDir, 'ci.yml')
    fs.writeFileSync(ciDst, ci, 'utf8')
    fs.unlinkSync(ciSrc)
    console.log(`  ✓ Renamed ${ciSrc} → ${ciDst}`)
  }

  const pubSrc = path.join(workflowsDir, 'publish-typescript.yml')
  if (fs.existsSync(pubSrc)) {
    let pub = fs.readFileSync(pubSrc, 'utf8')
    pub = pub.replace('name: Publish TypeScript to npm', 'name: Publish to npm')
    pub = pub.replace(/\n# Triggered when[^\n]*\n(?:# [^\n]*\n)*/, '\n')
    pub = pub.replace(/ {2}check-tag:\n(?: {4}[^\n]*\n|\n)+?(?=\n {2}[a-z])/, '')
    pub = pub.replace(/ {4}needs: check-tag\n {4}if: [^\n]+\n/, '')
    pub = pub.replace(/\ndefaults:\n {2}run:\n {4}working-directory: typescript\n/, '\n')
    pub = pub.split('typescript/package-lock.json').join('package-lock.json')
    const pubDst = path.join(workflowsDir, 'publish.yml')
    fs.writeFileSync(pubDst, pub, 'utf8')
    fs.unlinkSync(pubSrc)
    console.log(`  ✓ Renamed ${pubSrc} → ${pubDst}`)
  }
}

function hoistToRoot(): void {
  const srcRoot = path.resolve('.')
  const dstRoot = path.resolve('..')
  for (const entry of fs.readdirSync(srcRoot)) {
    const src = path.join(srcRoot, entry)
    const dst = path.join(dstRoot, entry)
    if (fs.existsSync(dst)) {
      fs.rmSync(dst, { recursive: true, force: true })
    }
    fs.renameSync(src, dst)
  }
  process.chdir(dstRoot)
  fs.rmdirSync(srcRoot)
  console.log('  ✓ Hoisted typescript/ contents to repo root')
}

async function dropMonorepoSibling(prompter: Prompter): Promise<boolean> {
  console.log()
  const dropSibling = await prompter.ask(
    'Drop the Python half and hoist this package to the repo root? (y/n)',
    'y',
  )
  if (dropSibling.toLowerCase() !== 'y') return false

  const siblingTargets = [
    '../python',
    '../.github/workflows/ci-python.yml',
    '../.github/workflows/publish-python.yml',
    '../README.md',
  ]
  for (const target of siblingTargets) {
    if (fs.existsSync(target)) {
      fs.rmSync(target, { recursive: true, force: true })
      console.log(`  ✓ Removed ${target}`)
    }
  }

  stripMonorepoFromReadme()
  hoistWorkflows()
  hoistToRoot()
  return true
}

// ---------------------------------------------------------------------------
// Final cleanup
// ---------------------------------------------------------------------------

function prunePackageJson(): void {
  const pkgPath = 'package.json'
  if (!fs.existsSync(pkgPath)) return
  const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8')) as {
    scripts?: Record<string, string>
    devDependencies?: Record<string, string>
  }
  if (pkg.scripts && 'setup' in pkg.scripts) {
    delete pkg.scripts.setup
  }
  if (pkg.devDependencies && 'tsx' in pkg.devDependencies) {
    delete pkg.devDependencies.tsx
  }
  fs.writeFileSync(pkgPath, JSON.stringify(pkg, null, 2) + '\n', 'utf8')
  console.log('  ✓ Pruned setup-only entries from package.json')
}

function removeSelfScript(hoisted: boolean): void {
  // After hoisting the cwd has changed and the import.meta.url path has been
  // moved, so resolve via cwd instead.
  const scriptPath = hoisted ? path.resolve('setup-template.ts') : fileURLToPath(import.meta.url)
  if (fs.existsSync(scriptPath)) {
    fs.unlinkSync(scriptPath)
    console.log('  ✓ Removed setup-template.ts')
  }
}

function printNextSteps(hoisted: boolean): void {
  console.log('\n✅ Setup complete!\n')
  if (hoisted) {
    console.log(
      '⚠️  Your shell is still in the now-deleted typescript/ directory. Run `cd ..` before continuing.\n',
    )
  }
  console.log('Next steps:')
  console.log('  1. Review the generated files')
  console.log('  2. Install dependencies: npm install')
  console.log('  3. Run checks: npm run check')
  console.log('  4. Start implementing your components')
  console.log()
}

// ---------------------------------------------------------------------------
// Entry point
// ---------------------------------------------------------------------------

async function main(): Promise<void> {
  const prompter = new Prompter()
  try {
    console.log('\n\u{1F527} Strands Template Setup\n')
    console.log('This will customize the template for your project.\n')

    const info = await gatherProjectInfo(prompter)
    const replacements = buildReplacements(info)

    console.log('\n⏳ Setting up project...\n')
    processSelectedFiles(info.selected, replacements)

    console.log('\n\u{1F5D1}️  Removing unused components...')
    deleteUnusedComponents(info.selected)

    renameSelectedFiles(info.selected, replacements)
    writeIndexFile(info.selected, replacements)

    console.log('\n\u{1F9F9} Cleaning up...')
    removeTemplateOnlyFiles()

    const hoisted = await dropMonorepoSibling(prompter)

    prunePackageJson()
    removeSelfScript(hoisted)

    printNextSteps(hoisted)
  } finally {
    prompter.close()
  }
}

main().catch((err) => {
  console.error(err)
  process.exit(1)
})
