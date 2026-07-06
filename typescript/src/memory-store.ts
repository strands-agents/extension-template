/**
 * Memory Store Implementation.
 *
 * Memory stores give an agent cross-session knowledge: a {@link MemoryManager}
 * searches them to recall facts and, when writable, writes new ones.
 *
 * @example
 * ```ts
 * import { Agent, MemoryManager } from '@strands-agents/sdk'
 * import { TemplateMemoryStore } from 'strands-template'
 *
 * const store = new TemplateMemoryStore({ name: 'notes' })
 * const agent = new Agent({ memoryManager: new MemoryManager({ stores: [store] }) })
 * ```
 */

import type {
  AddMessagesContext,
  ExtractionConfig,
  JSONValue,
  MemoryEntry,
  MemoryStore,
  MemoryStoreConfig,
  MessageData,
  SearchOptions,
} from '@strands-agents/sdk'

export interface TemplateMemoryStoreConfig extends MemoryStoreConfig {
  /** TODO: replace with a backend-specific fields your store needs (e.g. namespace, index name). */
  customField?: string
}

export class TemplateMemoryStore implements MemoryStore {
  readonly name: string
  readonly description?: string
  readonly maxSearchResults?: number
  readonly writable: boolean
  readonly extraction?: boolean | ExtractionConfig

  constructor(config: TemplateMemoryStoreConfig) {
    this.name = config.name
    if (config.description !== undefined) this.description = config.description
    if (config.maxSearchResults !== undefined) this.maxSearchResults = config.maxSearchResults
    this.writable = config.writable ?? false
    if (config.extraction !== undefined) this.extraction = config.extraction
  }

  async search(_query: string, _options?: SearchOptions): Promise<MemoryEntry[]> {
    // TODO: Query your backend and map each hit to a MemoryEntry, ordered by relevance.
    throw new Error('Not implemented')
  }

  async add(_content: string, _metadata?: Record<string, JSONValue>): Promise<unknown> {
    // Write one discrete entry. Can be implemented alongside addMessages.
    throw new Error('Not implemented')
  }

  async addMessages(_messages: MessageData[], _context?: AddMessagesContext): Promise<unknown> {
    // Ingest raw conversation turns for server-side extraction. Not implemented for vector-DB-style backends.
    throw new Error('Not implemented')
  }
}
