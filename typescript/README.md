<div align="center">
  <div>
    <a href="https://strandsagents.com">
      <img src="https://strandsagents.com/latest/assets/logo-github.svg" alt="Strands Agents" width="55px" height="105px">
    </a>
  </div>
  <h1>Strands Agents Extension Template — TypeScript</h1>
  <h2>Build and publish custom TypeScript components for Strands Agents.</h2>
  <p>
    <a href="https://strandsagents.com/">Documentation</a> ◆
    <a href="https://github.com/strands-agents/sdk-typescript">TypeScript SDK</a> ◆
    <a href="https://strandsagents.com/docs/community/community-packages/">Community Packages</a>
  </p>
</div>

This template helps you build and publish custom components for [Strands Agents](https://github.com/strands-agents/sdk-typescript). Whether you're creating a new tool, model provider, or session storage backend, this directory gives you a starting point with the right structure and conventions.

> This is the TypeScript half of the [extension-template](../README.md) monorepo. For the Python equivalent, see [`../python/`](../python/).

## Getting started

### 1. Create your repository

Click "Use this template" on GitHub to create your own repository. Then clone it locally and switch into this directory:

```bash
git clone https://github.com/yourusername/your-repo-name
cd your-repo-name/typescript
```

### 2. Run the setup script

The setup script customizes the template for your project. It renames files, updates imports, configures `package.json`, and removes components you don't need.

```bash
npm install
npm run setup
```

You'll be prompted for:

- **Package name** — A short identifier like `amazon`, `slack`, or `redis`. This becomes your module name (`strands-amazon`) and npm package name (`strands-amazon`).
- **Components** — Which extension points you want to include (tool, model, etc.).
- **Author info** — Your name, email, and GitHub username for `package.json`.
- **Description** — A one-line description of your package.

### 3. Install dependencies

After the setup script finishes, install peer + dev dependencies:

```bash
npm install
```

## What's in this template

The template includes skeleton implementations for all major Strands extension points.

| File | Component | Purpose |
|------|-----------|---------|
| `src/tool.ts` | Tool | Add capabilities to agents using the `tool` factory |
| `src/model.ts` | Model provider | Integrate custom LLM APIs |
| `src/plugin.ts` | Plugin | Extend agent behavior with hooks and tools in a composable package |
| `src/intervention.ts` | Intervention | Add composable control handlers for authorization, guardrails, and steering |
| `src/session-manager.ts` | Snapshot storage | Persist conversations across restarts (a `SnapshotStorage` impl plugged into the SDK's `SessionManager`) |
| `src/conversation-manager.ts` | Conversation manager | Control context window and message history |
| `src/memory-store.ts` | Memory store | Give agents cross-session knowledge via a search backend |

The setup script will remove components you don't select, so you only keep what you need.

## Implementing your components

Each file contains a minimal skeleton. Here's what to implement:

### Tools

Tools let agents interact with external systems and perform actions. Implement your callback inside `src/tool.ts`. Use a Zod schema for typed/validated input or a JSON schema for untyped input.

- [Custom tools](https://strandsagents.com/docs/user-guide/concepts/tools/custom-tools/) — Documentation
- See the `tool` factory in `@strands-agents/sdk` for full options.

### Plugins

Plugins provide a composable way to extend agent behavior by bundling hooks and tools into a single package. Implement `initAgent` to register hooks and `getTools` to contribute tools.

- [Plugins](https://strandsagents.com/docs/user-guide/concepts/plugins/) — Documentation
- The SDK's `SessionManager` and `vended-plugins/skills` are good worked examples.

### Interventions

Intervention handlers provide composable control layers for agents. Override lifecycle methods (like `beforeToolCall`) to intercept events and return typed decisions: proceed, deny, guide, confirm, or transform. Use them for authorization checks, guardrails, and human-in-the-loop approval.

- [Interventions](https://strandsagents.com/docs/user-guide/concepts/agents/interventions/) — Documentation
- The SDK's `vended-interventions` (Cedar authorization, HITL, steering) are worked examples.

### Model providers

Model providers connect agents to LLM APIs by extending the `Model` base class. Implement `stream()` to translate between Strands stream events and your provider's wire protocol.

- The SDK's `BedrockModel` (`@strands-agents/sdk/models/bedrock`) is the canonical reference implementation.

### Session storage

Session persistence lives behind the `SnapshotStorage` interface — implement it to add new backends (S3, Redis, custom DB). The SDK's `FileStorage` is a worked example.

- [Session management](https://strandsagents.com/docs/user-guide/concepts/agents/session-management/) — Documentation

### Conversation managers

Conversation managers control the context window and how message history grows over time. Override `reduce()` to mutate `agent.messages` in place when the context window is at risk.

- The SDK ships `SlidingWindowConversationManager` and `SummarizingConversationManager` as references.

### Memory stores

Memory stores give agents cross-session knowledge. A `MemoryManager` searches one or more stores to recall facts and, for writable stores, writes new ones. Implement `search()` to back memory with your own store — a vector database, a managed search service, or any system that retrieves entries by relevance. For writes, implement whichever sinks fit your backend. `add()` for adding an extracted memory. For discrete-entry backend (e.g. a vector DB), only implement this method. `addMessages()` for ingesting raw conversation turns to extract server-side. Only implement this for backends that support server side extraction. Store identity and behavior (`name`, `description`, `maxSearchResults`, `writable`, `extraction`) come from config via `MemoryStoreConfig`, matching the SDK's own stores; extend `TemplateMemoryStoreConfig` with any backend-specific fields.

- The SDK's `BedrockKnowledgeBaseStore` is a worked `MemoryStore` implementation.

## Testing

Run all checks (format, lint, type-check, test):

```bash
npm run check
```

Or run them individually:

```bash
npm test            # Run tests with vitest
npm run lint        # Run ESLint
npm run type-check  # Run tsc --noEmit
npm run format      # Format with Prettier
```

## Publishing to npm

You can publish manually or through GitHub Actions.

### Option 1: GitHub release (recommended)

The included workflow automatically publishes to npm when you create a GitHub release with a tag prefixed `typescript-v` (e.g. `typescript-v0.1.0`). The prefix lets the monorepo distinguish python and typescript releases.

1. Create an environment named `npm` in your GitHub repository (Settings → Environments). Add required reviewers if you want publishes gated behind approval.
2. Add an `NPM_TOKEN` secret to that environment (Account Settings → Access Tokens on npm, scope: Automation).
3. Bump the `version` in `package.json` (or use `npm version`) — the workflow publishes the version that's currently in `package.json`.
4. Create a release on GitHub with a tag like `typescript-v0.1.0`.
5. The workflow runs checks, builds, and publishes.

**Note:** If you create a release without configuring the environment and token, the workflow will fail. Set this up before your first release.

### Option 2: Manual publish

```bash
npm run check         # format, lint, type-check, test
npm run build         # tsc -> dist/
npm publish --access public
```

## Naming conventions

Follow these conventions so your package fits the Strands ecosystem:

| Item | Convention | Example |
|------|------------|---------|
| npm package | `strands-{name}` | `strands-amazon` |
| Model class | `{Name}Model` | `AmazonModel` |
| Plugin class | `{Name}Plugin` | `AmazonPlugin` |
| Intervention class | `{Name}Intervention` | `CedarIntervention` |
| Snapshot storage | `{Name}SnapshotStorage` | `RedisSnapshotStorage` |
| Conversation manager | `{Name}ConversationManager` | `SummarizingConversationManager` |
| Memory store | `{Name}MemoryStore` | `RedisMemoryStore` |
| Tool factory output | `{descriptiveName}` (camelCase) | `searchWeb`, `sendEmail` |

## Get featured

Help others discover your package by adding the `strands-agents` topic to your GitHub repository. You can also submit your package to be featured on the Strands website. See [Get Featured](https://strandsagents.com/docs/community/get-featured/) for details.

## Resources

- [Strands Agents documentation](https://strandsagents.com/)
- [TypeScript SDK repository](https://github.com/strands-agents/sdk-typescript)
- [Community packages](https://strandsagents.com/docs/community/community-packages/)

## License

Apache 2.0 — see [LICENSE](../LICENSE) for details.
