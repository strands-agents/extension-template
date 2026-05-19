/**
 * Session Storage Implementation.
 *
 * In the TypeScript SDK, session persistence is split into two pieces:
 *
 * 1. {@link SessionManager} — the SDK-provided plugin that listens for hook events
 *    and decides when to snapshot. You generally don't subclass this.
 * 2. {@link SnapshotStorage} — the pluggable backend (filesystem, S3, custom DB,
 *    etc.) that actually persists snapshots. **Implement this** to add a new
 *    storage target.
 *
 * @example
 * ```ts
 * import { Agent, SessionManager } from '@strands-agents/sdk'
 * import { TemplateSnapshotStorage } from 'strands-template'
 *
 * const session = new SessionManager({
 *   sessionId: 'my-session',
 *   storage: { snapshot: new TemplateSnapshotStorage({ ... }) },
 * })
 * const agent = new Agent({ sessionManager: session })
 * ```
 */

import type { Snapshot, SnapshotLocation, SnapshotManifest, SnapshotStorage } from '@strands-agents/sdk'

export interface TemplateSnapshotStorageConfig {
  /** Connection string, base path, bucket name, or whatever your backend needs. */
  connectionString: string
}

export class TemplateSnapshotStorage implements SnapshotStorage {
  constructor(private readonly _config: TemplateSnapshotStorageConfig) {}

  async saveSnapshot(_params: {
    location: SnapshotLocation
    snapshotId: string
    isLatest: boolean
    snapshot: Snapshot
  }): Promise<void> {
    // TODO: Persist the snapshot at the given location/snapshotId.
    throw new Error('Not implemented')
  }

  async loadSnapshot(_params: { location: SnapshotLocation; snapshotId?: string }): Promise<Snapshot | null> {
    // TODO: Return the snapshot at the given location, or null if not found.
    throw new Error('Not implemented')
  }

  async listSnapshotIds(_params: {
    location: SnapshotLocation
    limit?: number
    startAfter?: string
  }): Promise<string[]> {
    // TODO: Return immutable snapshot IDs in chronological order.
    throw new Error('Not implemented')
  }

  async deleteSession(_params: { sessionId: string }): Promise<void> {
    // TODO: Remove all snapshots and metadata for the given session.
    throw new Error('Not implemented')
  }

  async loadManifest(_params: { location: SnapshotLocation }): Promise<SnapshotManifest> {
    // TODO: Load the manifest, or return a freshly-initialized one if none exists yet.
    throw new Error('Not implemented')
  }

  async saveManifest(_params: { location: SnapshotLocation; manifest: SnapshotManifest }): Promise<void> {
    // TODO: Persist the manifest.
    throw new Error('Not implemented')
  }
}
