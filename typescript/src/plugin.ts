/**
 * Plugin Implementation.
 *
 * Plugins provide a composable way to extend agent behavior by bundling hooks and
 * tools into a single object. Implement {@link Plugin.initAgent} to register hooks
 * and (optionally) {@link Plugin.getTools} to contribute tools.
 *
 * @example
 * ```ts
 * import { Agent } from '@strands-agents/sdk'
 * import { TemplatePlugin } from 'strands-template'
 *
 * const agent = new Agent({ plugins: [new TemplatePlugin()] })
 * ```
 */

import { BeforeToolCallEvent, tool, type LocalAgent, type Plugin, type Tool } from '@strands-agents/sdk'
import { z } from 'zod'

const templatePluginTool = tool({
  name: 'template_plugin_tool',
  description: 'Brief description of what your plugin tool does.',
  inputSchema: z.object({
    param1: z.string().describe('Description of parameter 1.'),
  }),
  callback: (_input) => {
    // TODO: Implement your tool logic.
    throw new Error('Not implemented')
  },
})

export class TemplatePlugin implements Plugin {
  readonly name = 'template-plugin'

  initAgent(agent: LocalAgent): void {
    agent.addHook(BeforeToolCallEvent, (_event) => {
      // TODO: Implement your hook logic.
    })
  }

  getTools(): Tool[] {
    return [templatePluginTool]
  }
}
