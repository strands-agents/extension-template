/**
 * Storage Implementation.
 *
 * Storage backends persist raw bytes under string keys. The SDK uses the
 * {@link Storage} interface for session snapshots, context offloading, and any
 * construct that needs durable key-value persistence. To add a session
 * backend, implement Storage and pass it to the SDK's {@link SessionManager}.
 *
 * @example
 * ```ts
 * import { Agent, SessionManager } from '@strands-agents/sdk'
 * import { TemplateStorage } from 'strands-template'
 *
 * const sessionManager = new SessionManager({
 *   sessionId: 'my-session',
 *   storage: new TemplateStorage({}),
 * })
 * const agent = new Agent({ sessionManager })
 * ```
 */

import type { Storage } from '@strands-agents/sdk'

// eslint-disable-next-line @typescript-eslint/no-empty-object-type
export interface TemplateStorageConfig {
  // TODO: Add backend-specific fields your storage needs.
}

export class TemplateStorage implements Storage {
  constructor(private readonly _config: TemplateStorageConfig) {}

  async write(_key: string, _data: Uint8Array): Promise<void> {
    // TODO: Persist the data to your backend.
    throw new Error('Not implemented')
  }

  async read(_key: string): Promise<Uint8Array | null> {
    // TODO: Read from your backend, return null if not found.
    throw new Error('Not implemented')
  }

  async delete(_key: string): Promise<void> {
    // TODO: Delete from your backend. No-op if key does not exist.
    throw new Error('Not implemented')
  }

  async list(_query: string): Promise<string[]> {
    // TODO: Return keys matching the prefix, sorted ascending.
    throw new Error('Not implemented')
  }
}
