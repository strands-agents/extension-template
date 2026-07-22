import { describe, it, expect } from 'vitest'
import type { Storage } from '@strands-agents/sdk'
import { TemplateStorage } from '../src/storage.js'

describe('TemplateStorage', () => {
  it('satisfies the Storage interface', () => {
    const storage: Storage = new TemplateStorage({ connectionString: 'memory://' })
    expect(typeof storage.write).toBe('function')
    expect(typeof storage.read).toBe('function')
    expect(typeof storage.delete).toBe('function')
    expect(typeof storage.list).toBe('function')
  })

  // TODO: Add round-trip write/read tests once the storage backend is implemented.
})
