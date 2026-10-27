import { describe, it, expect } from 'vitest'
import { TemplateDecisionModel } from '../src/decision-model.js'

describe('TemplateDecisionModel', () => {
  it('rejects until _ask is implemented', async () => {
    const decisions = new TemplateDecisionModel({ apiKey: 'test-key' })
    await expect(
      decisions.ask('A customer needs a refund today.', {
        urgent: { question: 'Is this urgent?', choices: 'boolean' },
      })
    ).rejects.toThrow('Not implemented')
  })
})
