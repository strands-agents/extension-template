/**
 * Intervention Handler Implementation.
 *
 * Intervention handlers provide composable control layers for agents.
 * Override lifecycle methods to intercept events and return typed
 * decisions (proceed, deny, guide, confirm, transform).
 *
 * @example
 * ```ts
 * import { Agent } from '@strands-agents/sdk'
 * import { TemplateIntervention } from 'strands-template'
 *
 * const agent = new Agent({ interventions: [new TemplateIntervention()] })
 * ```
 */

import {
  InterventionHandler,
  InterventionActions,
  type BeforeToolCallEvent,
  type Proceed,
  type Deny,
} from '@strands-agents/sdk'

export class TemplateIntervention extends InterventionHandler {
  readonly name = 'template-intervention'

  // Override any lifecycle methods you need — not just beforeToolCall.

  override beforeToolCall(_event: BeforeToolCallEvent): Proceed | Deny {
    // TODO: Implement your intervention logic.
    return InterventionActions.proceed()
  }
}
