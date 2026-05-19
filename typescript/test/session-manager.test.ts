import { describe, it, expect } from 'vitest'
import { TemplateSnapshotStorage } from '../src/session-manager.js'

describe('TemplateSnapshotStorage', () => {
  it('can be constructed with a config', () => {
    const storage = new TemplateSnapshotStorage({ connectionString: 'in-memory' })
    expect(storage).toBeInstanceOf(TemplateSnapshotStorage)
  })

  // TODO: Add round-trip save/load tests once the storage backend is implemented.
})
