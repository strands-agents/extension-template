import { describe, it, expect } from 'vitest'
import { TemplatePlugin } from '../src/plugin.js'

describe('TemplatePlugin', () => {
  it('exposes a stable name', () => {
    const plugin = new TemplatePlugin()
    expect(plugin.name).toBe('template-plugin')
  })

  it('contributes tools via getTools', () => {
    const plugin = new TemplatePlugin()
    expect(plugin.getTools()).toHaveLength(1)
  })
})
