/**
 * Conversation Manager Implementation.
 *
 * Conversation managers control how `agent.messages` is reduced when the context
 * window is at risk of overflowing. Override {@link reduce} to mutate
 * `options.agent.messages` in place and return `true` if any reduction was performed.
 *
 * @example
 * ```ts
 * import { Agent } from '@strands-agents/sdk'
 * import { TemplateConversationManager } from 'strands-template'
 *
 * const agent = new Agent({ conversationManager: new TemplateConversationManager() })
 * ```
 */

import {
  ConversationManager,
  type ConversationManagerOptions,
  type ConversationManagerReduceOptions,
} from '@strands-agents/sdk'

export class TemplateConversationManager extends ConversationManager {
  readonly name = 'template-conversation-manager'

  constructor(options?: ConversationManagerOptions) {
    super(options)
  }

  override async reduce(_options: ConversationManagerReduceOptions): Promise<boolean> {
    // TODO: Mutate `_options.agent.messages` in place and return whether any
    // reduction occurred. When `_options.error` is set this is a reactive call
    // and MUST free up enough room for the next model call to succeed.
    return false
  }
}
