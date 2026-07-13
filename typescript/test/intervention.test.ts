import { describe, it, expect } from 'vitest'
import { TemplateIntervention } from '../src/intervention.js'

describe('TemplateIntervention', () => {
  it('exposes a stable name', () => {
    const handler = new TemplateIntervention()
    expect(handler.name).toBe('template-intervention')
  })
})
