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

import { InterventionHandler, InterventionActions, type BeforeToolCallEvent } from '@strands-agents/sdk'

// The SDK's root entry point doesn't export the action types directly,
// so derive them from the action creators.
type Proceed = ReturnType<typeof InterventionActions.proceed>
type Deny = ReturnType<typeof InterventionActions.deny>

export class TemplateIntervention extends InterventionHandler {
  readonly name = 'template-intervention'

  // Override any lifecycle methods you need — not just beforeToolCall.

  override beforeToolCall(_event: BeforeToolCallEvent): Proceed | Deny {
    // TODO: Implement your intervention logic.
    return InterventionActions.proceed()
  }
}
