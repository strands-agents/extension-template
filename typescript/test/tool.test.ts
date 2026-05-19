import { describe, it, expect } from 'vitest'
import { templateTool } from '../src/tool.js'

describe('templateTool', () => {
  it('exposes the expected name', () => {
    expect(templateTool.name).toBe('template_tool')
  })

  // TODO: Add behavior tests once you implement the callback.
})
