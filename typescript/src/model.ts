/**
 * Model Provider Implementation.
 *
 * Model providers connect agents to LLM APIs by extending the {@link Model} base
 * class. Implement {@link TemplateModel.stream} to translate between Strands stream
 * events and your provider's wire protocol.
 *
 * @example
 * ```ts
 * import { Agent } from '@strands-agents/sdk'
 * import { TemplateModel } from 'strands-template'
 *
 * const model = new TemplateModel({ apiKey: process.env.API_KEY!, modelId: 'my-model' })
 * const agent = new Agent({ model })
 * ```
 */

import {
  Model,
  type BaseModelConfig,
  type Message,
  type ModelStreamEvent,
  type StreamOptions,
} from '@strands-agents/sdk'

export interface TemplateModelConfig extends BaseModelConfig {
  /** API key for the upstream provider. */
  apiKey: string
}

export class TemplateModel extends Model<TemplateModelConfig> {
  private _config: TemplateModelConfig

  constructor(config: TemplateModelConfig) {
    super()
    this._config = { ...config }
  }

  override updateConfig(modelConfig: Partial<TemplateModelConfig>): void {
    this._config = { ...this._config, ...modelConfig }
  }

  override getConfig(): TemplateModelConfig {
    return { ...this._config }
  }

  // eslint-disable-next-line require-yield -- skeleton; remove once you implement stream()
  override async *stream(_messages: Message[], _options?: StreamOptions): AsyncIterable<ModelStreamEvent> {
    // TODO: Implement streaming.
    //
    // Yield ModelMessageStartEvent → one or more ModelContentBlockStartEvent /
    // ModelContentBlockDeltaEvent / ModelContentBlockStopEvent triples →
    // ModelMessageStopEvent → optional ModelMetadataEvent.
    //
    // See @strands-agents/sdk docs and the BedrockModel implementation in the SDK
    // for a worked example.
    throw new Error('Not implemented')
  }
}
