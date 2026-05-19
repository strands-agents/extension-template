import { describe, it, expect } from 'vitest'
import { TemplateConversationManager } from '../src/conversation-manager.js'

describe('TemplateConversationManager', () => {
  it('exposes a stable name', () => {
    const cm = new TemplateConversationManager()
    expect(cm.name).toBe('template-conversation-manager')
  })
})
