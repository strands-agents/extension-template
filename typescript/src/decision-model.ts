/**
 * Decision Model Implementation.
 *
 * Decision models answer closed questions (yes/no or one of a fixed set of
 * choices) over agent state by extending the {@link DecisionModel} base class.
 * Implement {@link TemplateDecisionModel._ask} to call your provider's decision API.
 *
 * @example
 * ```ts
 * import { TemplateDecisionModel } from 'strands-template'
 *
 * const decisions = new TemplateDecisionModel({ apiKey: process.env.API_KEY! })
 * const result = await decisions.ask('A customer needs a refund today.', {
 *   urgent: { question: 'Is this urgent?', choices: 'boolean' },
 * })
 * ```
 */

import { DecisionModel, type DecisionInput, type DecisionResult, type Question } from '@strands-agents/sdk'

export interface TemplateDecisionModelConfig {
  /** API key for the upstream provider. */
  apiKey: string
}

export class TemplateDecisionModel extends DecisionModel {
  constructor(private readonly _config: TemplateDecisionModelConfig) {
    super()
  }

  protected override async _ask<const Q extends Record<string, Question>>(
    _state: DecisionInput,
    _questions: Q
  ): Promise<DecisionResult<Q>> {
    // TODO: Send the state and questions to your provider and map its response.
    //
    // Return one answer per question key: a boolean for `choices: 'boolean'`,
    // one of the listed choices otherwise, or `new Uncertain()` when the
    // question allows it. Set `metadata.latencyMs` from the provider call and
    // `usage` when the provider reports token counts.
    //
    // See the SDK's TypeSafeDecisionModel for a worked example.
    throw new Error('Not implemented')
  }
}
