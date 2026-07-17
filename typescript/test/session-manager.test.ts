import { describe, it, expect } from 'vitest'
import type { SnapshotStorage } from '@strands-agents/sdk'
import { TemplateSnapshotStorage } from '../src/session-manager.js'

describe('TemplateSnapshotStorage', () => {
  it('satisfies the SnapshotStorage interface', () => {
    // The type annotation is the real check: it fails to compile (via
    // `npm run type-check`) if the class stops implementing the interface.
    const storage: SnapshotStorage = new TemplateSnapshotStorage({ connectionString: 'in-memory' })
    expect(typeof storage.saveSnapshot).toBe('function')
    expect(typeof storage.loadSnapshot).toBe('function')
  })

  // TODO: Add round-trip save/load tests once the storage backend is implemented.
})
