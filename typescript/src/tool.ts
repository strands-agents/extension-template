/**
 * Tool Implementation.
 *
 * Tools let agents interact with external systems and perform actions.
 * The {@link tool} factory accepts either a Zod schema (typed + validated input)
 * or a JSON schema (untyped) plus a callback that runs when the agent invokes it.
 *
 * @example
 * ```ts
 * import { Agent } from '@strands-agents/sdk'
 * import { templateTool } from 'strands-template'
 *
 * const agent = new Agent({ tools: [templateTool] })
 * ```
 */

import { tool } from '@strands-agents/sdk'
import { z } from 'zod'

const inputSchema = z.object({
  param1: z.string().describe('Description of parameter 1.'),
})

export const templateTool = tool({
  name: 'template_tool',
  description: 'Brief description of what your tool does.',
  inputSchema,
  callback: (_input: z.infer<typeof inputSchema>) => {
    // TODO: Implement your tool logic.
    throw new Error('Not implemented')
  },
})
