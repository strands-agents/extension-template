<div align="center">
  <div>
    <a href="https://strandsagents.com">
      <img src="https://strandsagents.com/latest/assets/logo-github.svg" alt="Strands Agents" width="55px" height="105px">
    </a>
  </div>
  <h1>Strands Agents Extension Template</h1>
  <h2>Build and publish custom components for Strands Agents.</h2>
  <p>
    <a href="https://strandsagents.com/">Documentation</a> ◆
    <a href="https://github.com/strands-agents/sdk-python">Python SDK</a> ◆
    <a href="https://github.com/strands-agents/sdk-typescript">TypeScript SDK</a> ◆
    <a href="https://github.com/strands-agents/tools">Tools</a> ◆
    <a href="https://strandsagents.com/latest/community/community-packages/">Community Packages</a>
  </p>
</div>

This monorepo contains starter templates for building custom Strands Agents extensions in two languages. Each template gives you skeletons for the major extension points, an interactive setup script that customizes the project for your package, and CI/publish workflows wired up to PyPI or npm.

| Language   | Directory                  | Package registry | SDK                                                      |
|------------|----------------------------|------------------|----------------------------------------------------------|
| Python     | [`python/`](./python)      | PyPI             | [`strands-agents`](https://pypi.org/project/strands-agents/) |
| TypeScript | [`typescript/`](./typescript) | npm           | [`@strands-agents/sdk`](https://www.npmjs.com/package/@strands-agents/sdk) |

## Getting started

1. Click **Use this template** on GitHub to create your own repository.
2. Clone it locally and decide which language you're targeting.
3. Open the corresponding subdirectory and follow its README:
   - Python → [`python/README.md`](./python/README.md)
   - TypeScript → [`typescript/README.md`](./typescript/README.md)

You can keep both subprojects in the same repo if your package ships SDKs in both languages, or delete the directory you don't need.

## What's in each template

Both templates expose the same five Strands extension points so you can pick whichever fits your use case:

| Component            | Purpose                                                |
|----------------------|--------------------------------------------------------|
| Tool                 | Add capabilities to agents using the `tool` primitive  |
| Model provider       | Integrate custom LLM APIs                              |
| Plugin               | Bundle hooks and tools into a composable package       |
| Session manager      | Persist conversations across restarts                  |
| Conversation manager | Control context window and message history            |

The interactive setup script in each subdirectory removes the components you don't select, renames everything to your package name, and wires up `pyproject.toml` / `package.json` accordingly.

## Releases and tags

Releases are scoped per language so the two halves of this monorepo can ship independently:

| Tag prefix    | Workflow                                        | Publishes to |
|---------------|-------------------------------------------------|--------------|
| `python-v*`   | [`publish-python.yml`](.github/workflows/publish-python.yml)         | PyPI         |
| `typescript-v*` | [`publish-typescript.yml`](.github/workflows/publish-typescript.yml) | npm          |

Once you've run the setup script for your language of choice, you can drop the dual-prefix scheme and use the standard `v*` form if you'd rather not carry the monorepo conventions into your own repo.

## License

Apache 2.0 — see [LICENSE](LICENSE) for details.
