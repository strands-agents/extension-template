import { describe, it, expect } from 'vitest'
import { TemplateMemoryStore } from '../src/memory-store.js'

describe('TemplateMemoryStore', () => {
  it('stores config passed to the constructor', () => {
    const store = new TemplateMemoryStore({ name: 'notes', description: 'scratch notes' })
    expect(store.name).toBe('notes')
    expect(store.description).toBe('scratch notes')
  })

  it('reads writable from config, defaulting to false', () => {
    expect(new TemplateMemoryStore({ name: 'notes', writable: true }).writable).toBe(true)
  })
})
