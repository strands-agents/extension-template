import { describe, it, expect } from 'vitest'
import { SessionManager, type Storage } from '@strands-agents/sdk'
import { TemplateStorage } from '../src/storage.js'

describe('TemplateStorage', () => {
  it('satisfies the Storage interface', () => {
    const storage: Storage = new TemplateStorage({})
    expect(typeof storage.write).toBe('function')
    expect(typeof storage.read).toBe('function')
    expect(typeof storage.delete).toBe('function')
    expect(typeof storage.list).toBe('function')
  })

  it('backs the SDK SessionManager', () => {
    // Fails `npm run type-check` if SessionManager stops accepting a Storage.
    const sessionManager = new SessionManager({ sessionId: 'test-session', storage: new TemplateStorage({}) })
    expect(sessionManager).toBeInstanceOf(SessionManager)
  })

  // TODO: Add round-trip write/read tests once the storage backend is implemented.
})
