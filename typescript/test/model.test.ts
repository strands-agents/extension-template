import { describe, it, expect } from 'vitest'
import { TemplateModel } from '../src/model.js'

describe('TemplateModel', () => {
  it('stores config passed to the constructor', () => {
    const model = new TemplateModel({ apiKey: 'test-key', modelId: 'test-model' })
    const config = model.getConfig()
    expect(config.apiKey).toBe('test-key')
    expect(config.modelId).toBe('test-model')
  })

  it('merges updates via updateConfig', () => {
    const model = new TemplateModel({ apiKey: 'k1', modelId: 'm1' })
    model.updateConfig({ modelId: 'm2' })
    expect(model.getConfig().modelId).toBe('m2')
    expect(model.getConfig().apiKey).toBe('k1')
  })
})
